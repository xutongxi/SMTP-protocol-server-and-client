from readline import replace_history_item
import  socket
#from urllib import request
import asyncore
import time

class Devnull:
    def write(self, msg): pass
    def flush(self): pass


#当程序中的某些地方试图使用 DEBUGSTREAM 写入数据时，实际上什么也不会发生，就像向 /dev/null 写入数据一样，数据会被忽略。这在调试时可以用来禁用调试输出，而不必修改大量代码。
DEBUGSTREAM = Devnull()

SMTP_PORT = 25
DATA_SIZE_DEFAULT = 1024


class   SMTPServer(asyncore.dispatcher):
    

    def handleClient(connectionSocket):
        welcome_msg = "220 Welcome to My SMTP Server\r\n"
        connectionSocket.send(welcome_msg.encode())

        expectedCommand = ["HELO", "MAIL", "RCPT", "DATA", "QUIT"]
        currentCommandIndex = 0

        while True:
            request = connectionSocket.recv(1024).decode()
            if not request:
                break
            if not request.startswith(expectedCommand[currentCommandIndex]):
                errorMsg = "503 Bad sequence of commands\r\n"
                connectionSocket.send(errorMsg.encode())
                break
            if request.startswith("HELO"):
                response = "250 OK\r\n"
            elif request.startswith("MAIL"):
                response = "250 OK\r\n"
            elif request.startswith("RCPT"):
                while request.startswith("RCPT"):
                    response = "250 OK\r\n"
                    connectionSocket.send(response.encode())
                    request = connectionSocket.recv(1024).decode()
                continue
            elif request.startswith("DATA"):
                response = "354 End data with <CR><LF>.<CR><LF>\r\n"
            elif request.startswith("QUIT"):
                response = "221 Goodbye\r\n"
                break
            else:
                response = "500 Command not recognized\r\n"

            connectionSocket.send(response.encode())
            currentCommandIndex +=1
        connectionSocket.close()

    def _init_(self, localAddr, remoteAddr, dataSizeLimit = DATA_SIZE_DEFAULT, map = none, enableSMTPUTF8 = False, decodeData = False):
        self.localAddr = localAddr
        self.remoteAddr = remoteAddr
        self.dataSizeLimit = dataSizeLimit
        self.enableSMTPUTF8 = enableSMTPUTF8
        self.decodeData = decodeData
        
        try:
            serverSocket = socket.getaddrinfo(*localAddr, type=socket.SOCK_STREAM)
            self.create_socket(serverSocket[0][0], serverSocket[0][1])
            self.set_reuse_addr()
            self.bind(localAddr)
            self.listen(5)
            
        except:
            self.close()
            raise
        else:
            print('%s started at %s \n\t Local addr: %s \n\t Remote addr: %s' %(self.__class__.__name__, time.ctime(time.time()),localAddr, remoteAddr), file=DEBUGSTREAM)

        while True:
            connectionSocket, address = self.accept()
            print(f"Connection from {address}")
            self.handleClient(connectionSocket)








