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