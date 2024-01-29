import  socket
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

        connectionSocket, address = self.accept()
        command =  connectionSocket.recv(1024).decode
        match command:
            case "HELO":
                reply = "250 Hello, this is my SMTP server"

            case "MAIL":
                reply = "250 OK"

            case "RCPT":
                reply = "250 OK"

            case "DATA":
                reply = "354 End data with <CR><LF>.<CR><LF>"

            case "QUIT":
                reply = "221 Goodbye"

            case _:
                reply = "500 Command not recognized"
        connectionSocket.send(reply.encode())
        








