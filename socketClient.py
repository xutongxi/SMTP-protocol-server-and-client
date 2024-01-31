from socket import *

hostname = "192.168.191.205"
port = 12345

clinet = socket(AF_INET, SOCK_STREAM)
clinet.connect((hostname,port))

message = input("Please enter command:")
clinet.send(message.encode())

reply = clinet.recv(1024).decode()
print("The server reply:  "+reply)

clinet.close()