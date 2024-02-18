from socket import *

hostname = "163.123.183.116"
port = 25

clinet = socket(AF_INET, SOCK_STREAM)
clinet.connect((hostname,port))
while True:
    message = input("Please enter command:")
    clinet.send(message.encode())

    reply = clinet.recv(1024).decode()
    print("The server reply:  "+reply)

clinet.close()