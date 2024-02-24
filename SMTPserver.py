import socket
import dns.resolver
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.message import EmailMessage


def send_email(from_addr, to_addr, data):
    """构建并发送邮件。"""
    """msg = EmailMessage()
    msg.set_content(data)  # 设置邮件正文
    msg['From'] = from_addr
    msg['To'] = to_addr"""
    # 在这里添加更多邮件头部信息，如Subject

    # 使用本地SMTP服务器发送邮件
    with smtplib.SMTP('localhost',1025) as smtp:
        smtp.sendmail(from_addr, to_addr,data.encode('utf-8'))
        print(f"Email sent from {from_addr} to {to_addr}")


def send_email_via_socket(from_addr, to_addr, subject, message):
    # 解析收件人邮箱域的MX记录
    domain = to_addr.split('@')[1]
    mx_records = dns.resolver.resolve(domain, 'MX')
    mx_record = sorted(mx_records, key=lambda rec: rec.preference)[0]
    smtp_server = mx_record.exchange.to_text().rstrip('.')

    # 创建邮件正文，包括头部和消息
    email_content = f"From: {from_addr}\r\nTo: {to_addr}\r\nSubject: {subject}\r\n\r\n{message}"

    # 建立到SMTP服务器的连接
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((smtp_server, 25))  # SMTP标准端口为25

    response = server.recv(1024)  # 读取欢迎消息
    print("Server response:", response.decode())

    # 发送SMTP命令
    server.send(b"HELO 163.123.183.116\r\n")
    response = server.recv(1024)  # 读取响应
    print("HELO response:", response.decode())

    server.send(f"MAIL FROM:<{from_addr}>\r\n".encode())
    response = server.recv(1024)  # 读取响应
    print("MAIL FROM response:", response.decode())

    server.send(f"RCPT TO:<{to_addr}>\r\n".encode())
    response = server.recv(1024)  # 读取响应
    print("RCPT TO response:", response.decode())

    server.send(b"DATA\r\n")
    response = server.recv(1024)  # 读取响应
    print("DATA response:", response.decode())

    # 发送邮件正文，以"\r\n.\r\n"结束
    server.send(f"{email_content}\r\n.\r\n".encode())
    response = server.recv(1024)  # 读取响应
    print("Email content response:", response.decode())

    server.send(b"QUIT\r\n")  # 结束会话
    response = server.recv(1024)  # 读取响应
    print("QUIT response:", response.decode())

    server.close()

def handle_client_connection(client_socket):
    current_state = 0
    from_addr = ''
    to_addr = ''
    email_data = ''
    subject = ''

    client_socket.send(b"220 Welcome to My SMTP Server\r\n")

    while True:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                continue

            if data.upper().startswith("MAIL FROM:"):
                command = "MAIL FROM"
                params = data[len("MAIL FROM:"):].strip()
            elif data.upper().startswith("RCPT TO:"):
                command = "RCPT TO"
                params = data[len("RCPT TO:"):].strip()
            else:
                parts = data.split(maxsplit=1)
                command = parts[0].upper()
                params = parts[1] if len(parts) > 1 else ""

            if command == "QUIT":
                client_socket.send(b"221 Goodbye\r\n")
                break
            elif command in ["HELO", "EHLO"]:
                client_socket.send(b"250 Hello, pleased to meet you\r\n")
                current_state = 1
            elif command == "MAIL FROM" and current_state >= 1:
                from_addr = params
                client_socket.send(b"250 OK\r\n")
                current_state = 2
            elif command == "RCPT TO" and current_state >= 2:
                to_addr = params
                client_socket.send(b"250 OK\r\n")
                current_state = 3
            elif command == "DATA" and current_state == 3:
                client_socket.send(b"354 Start mail input; end with <CR><LF>.<CR><LF>\r\n")
                email_data = ''
                part = client_socket.recv(1024).decode()
                if part.upper().startswith('SUBJECT:'):
                    subject, part = part.split('\n', 1)
                    subject = subject[len('SUBJECT:'):].strip()
                while True:
                    if part.strip() == '.':
                        break
                    email_data += part
                    part = client_socket.recv(1024).decode()
                send_email_via_socket(from_addr, to_addr, subject, email_data)  # 调用发送邮件的函数
                client_socket.send(b"250 OK, message accepted for delivery\r\n")
                current_state = 1  # 重置状态以准备新的邮件事务
            elif command == "RSET":
                from_addr, to_addr, email_data, subject = '', '', '', ''  # 重置邮件信息
                current_state = 0
                client_socket.send(b"250 OK\r\n")
            elif command == "VRFY":
                client_socket.send(b"252 Cannot VRFY user, but will accept message and attempt delivery\r\n")
            elif command == "NOOP":
                client_socket.send(b"250 OK\r\n")
            else:
                client_socket.send(b"500 Syntax error, command unrecognized\r\n")

        except Exception as e:
            print(f"Error: {e}")
            client_socket.send(b"421 Service not available, closing transmission channel\r\n")
            break

    client_socket.close()

def start_smtp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.184', 1025)  # 使用非特权端口
    server_socket.bind(server_address)
    server_socket.listen(5)
    print('SMTP server is listening on {}:{}'.format(*server_address))

    while True:
        client_socket, _ = server_socket.accept()
        handle_client_connection(client_socket)

if __name__ == "__main__":
    start_smtp_server()
