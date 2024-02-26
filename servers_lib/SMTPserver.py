import socket
import dns.resolver
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.message import EmailMessage




class SMTPServer:
    def __init__(self, host='192.168.0.184', port=25):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f'SMTP 服务器已启动在 {self.host}:{self.port}')
            while True:
                client, address = self.server_socket.accept()
                print(f'来自 {address[0]}:{address[1]} 的连接')
                self.handle_client(client)
        except Exception as e:
            print(f'启动服务器时出错: {e}')
        finally:
            self.server_socket.close()

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


    def send_email_via_socket(self,from_addr, to_addrs, message):
        for to_addr in to_addrs:

            # 解析收件人邮箱域的MX记录
            domain = to_addr.split('@')[1]
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_record = sorted(mx_records, key=lambda rec: rec.preference)[0]
            smtp_server = mx_record.exchange.to_text().rstrip('.')


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
            response = server.recv(1024)
            print("RCPT TO response:", response.decode())

            server.send(b"DATA\r\n")
            response = server.recv(1024)  # 读取响应
            print("DATA response:", response.decode())

            # 发送邮件正文，以"\r\n.\r\n"结束
            server.send(f"{message}\r\n.\r\n".encode())
            response = server.recv(1024)  # 读取响应
            print("Email content response:", response.decode())

            server.send(b"QUIT\r\n")  # 结束会话
            response = server.recv(1024)  # 读取响应
            print("QUIT response:", response.decode())

            server.close()

    def handle_client(self,client_socket):
        current_state = 0
        from_addr = ''
        to_addrs = []
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
                    from_addr = params[1:-1]
                    client_socket.send(b"250 OK\r\n")
                    current_state = 2
                elif command == "RCPT TO" and current_state >= 2:
                    to_addr = params[1:-1]
                    to_addrs.append(to_addr)
                    client_socket.send(b"250 OK\r\n")
                    current_state = 3
                elif command == "DATA" and current_state == 3:
                    client_socket.send(b"354 Start mail input; end with <CR><LF>.<CR><LF>\r\n")
                    email_data = ''
                    while True:
                        part = client_socket.recv(1024).decode()
                        email_data += part
                        # 检查是否接收到邮件正文结束标志
                        if email_data.endswith('\r\n.\r\n'):
                            # 移除结束标志，准备处理邮件正文
                            email_data = email_data[:-5]
                            break

                    # 在这里处理接收到的邮件正文
                    # 假设 send_email_via_socket 已正确定义，能够处理接收到的邮件数据
                    self.send_email_via_socket(from_addr, to_addrs, email_data)
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

if __name__ == '__main__':
    host = '192.168.0.184'  # 示例IP地址；根据需要更改
    port = 25  # 示例端口；根据需要更改
    smtp_server = SMTPServer(host=host, port=port)
    smtp_server.start_server()
