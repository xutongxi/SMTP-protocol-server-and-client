from socket import *

hostname = "163.123.183.116"
port = 12345

clinet = socket(AF_INET, SOCK_STREAM)
clinet.connect((hostname,port))

message = input("HELO")
clinet.send(message.encode())

reply = clinet.recv(1024).decode()
print("The server reply:  "+reply)

clinet.close()
