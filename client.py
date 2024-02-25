from smtpclient import client_SMTP


def main():
    smtp_server = "192.168.0.184"  # SMTP服务器地址
    sender = "recoqtuw@gmail.com"  # 发件人邮箱
    recipient = "932931207@qq.com" # 收件人邮箱列表
    message = """From: recoqtuw@gmail.com
To: 932931207@qq.com
Subject: SMTP Test

This is a test email message.
"""  # 邮件内容

    # 创建SMTP客户端实例
    smtp_client = client_SMTP(smtp_server, 25)
    try:
        # 发送邮件
        smtp_client.send_helo()

        smtp_client.send_mail(sender)

        smtp_client.send_rcpt(recipient)

        smtp_client.send_data(message)

    except Exception as e:
        print(f"邮件发送过程中发生错误: {e}")
    finally:
        # 关闭SMTP连接
        smtp_client.close_socket()

if __name__ == "__main__":
    main()
