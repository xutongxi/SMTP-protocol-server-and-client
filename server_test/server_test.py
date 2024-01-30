import asyncore
from smtpd import SMTPServer

class MySMTPHandler(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print(f"Received message from {mailfrom} to {rcpttos}")
        print("Message:")
        print(data.decode('utf-8'))
        print("End of message\n")

if __name__ == "__main__":
    smtp_server = MySMTPHandler(('163.123.183.116', 25), None)
    print("SMTP server is running...")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("\nSMTP server stopped.")
