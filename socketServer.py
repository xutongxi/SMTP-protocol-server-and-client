from socket import *
server = socket(AF_INET, SOCK_STREAM)
server.bind(("192.168.156.1", 12345))

server.listen(5)
print("Server is ready to accept commands....")

conn, addr = server.accept()
command = conn.recv(1024).decode()

print("The command from the client : "+command)

if command == "HELO":
        reply = "250 Hello, this is my SMTP server"



conn.send(reply.encode())

conn.close()