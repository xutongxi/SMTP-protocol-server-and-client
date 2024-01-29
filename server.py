class SMTPserver(asyncore.dispatcher):
    def process_command(self, command, *args):
        # 处理客户端的命令并返回相应的回复
        if command == "HELO":
            return "250 Hello, this is my SMTP server"
        elif command == "MAIL":
            return "250 OK"
        elif command == "RCPT":
            return "250 OK"
        elif command == "DATA":
            return "354 End data with <CR><LF>.<CR><LF>"
        elif command == "QUIT":
            return "221 Goodbye"
        else:
            return "500 Command not recognized"

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"Received message from: {mailfrom}")
        print(f"Recipients: {rcpttos}")

        # 处理邮件数据
        print(f"Message data:\n{data.decode('utf-8')}")


if __name__ == '__main__':
    # 在本地监听 1025 端口
    server = MySMTPServer(('localhost', 1025), None)
    print("SMTP Server listening on port 1025...")

    try:
        #启动异步事件循环。在这个循环中，程序会一直等待和处理事件，包括接收新的SMTP连接、接收数据等
        asyncore.loop()
    except KeyboardInterrupt:          #捕获键盘中断异常，即用户按下Ctrl+C中断程序的情况。
        print("SMTP Server shutting down...")
        server.close()