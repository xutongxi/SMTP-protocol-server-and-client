import socket
import re

SMTP_PORT = 25
CRLF = "\r\n" #line terminator
bianry_CRLF = b"\r\n" #binary form
max_text = 1000
max_read = 1100

class ResponseException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"SMTP response error: {code} {message}")

class client_SMTP:
    tcp_scoket = None#连接的socket
    reply = None#备用存储回复消息
    communicat_log = None#等待以后扩展
    host = None#远程IP地址
    port = SMTP_PORT#远程端口
    timeout = None#断时间
    esmtp = False#是否支持使用esmtp
    esmtp_support = {}
    responce = None
    encode = None#发送命令的编码形式
    #remote_host(host, port) 本地服务器地址 fqdn本机域名地址  source_address为本机地址
    def __init__(self, remote_host, port, local_host_hostname=None, source_address=None, time_out = 10):
        self.timeout = time_out
        self.host = remote_host
        self.port = port
        self.encode = 'ascii' #or utf-8 if have time
        fqdn = socket.getfqdn()
        self.source_address = source_address#(ip, port)
        if local_host_hostname is not None:
            self.local_host_hostname = local_host_hostname
        elif '.' in fqdn:
            self.local_host_hostname = fqdn
        else:
            self.local_host_hostname = socket.gethostbyname(socket.getfqdn())
            self.local_host_hostname = result = '[{}]'.format(self.local_host_hostname)
        (reply_code,reply_msg) = self.connect()
        if reply_code != b'220':
            #self.close()
            raise ResponseException(reply_code,reply_msg)
        else:
            print("connect success")
        
    def connect(self, host = None, port = None):
        if not host:
            host = self.host
        if not port:
            port = self.port
        self.tcp_scoket = socket.create_connection((host, port), self.timeout,self.source_address)
        #analysis for the server reply
        return self.get_reply()# a touple with code and Possible msg
        
        
    def get_reply(self):#注意得到的(reply_code, result_msgs)为二进制形式
        reply_list = []
        reply_code = b''
        if self.reply is None:
            self.reply = self.tcp_scoket.makefile('rb')#create reply file in binary form 必要时需要在后续转化成ascii阅读
        reply_msg = self.reply.readline(max_read)
        while 1:
            if len(reply_msg) > max_text:
                self.close()
                raise ResponseException(500, "Line too long.")#longer than 512 this point is 1000 byte
            reply_code = reply_msg[0:3]
            reply_list.append(reply_msg[4:].strip(b' \t\r\n'))#\t is not necessary in protocol but avoid some server support
            if reply_msg[3:4] != b"-":
                break
            else:
                reply_msg = self.reply.readline(max_read)
        result_msgs = b""
        for line in reply_list:
            result_msgs += line + b"\n"
        return (reply_code, result_msgs)
            
    def send(self, msg):#use socket to send messagge msg type is string
        msg = msg.encode("ascii")
        try:
            self.tcp_scoket.sendall(msg)#better than send
        except socket.error as e:
            print(f"Error sending data: {e}")
            
    def send_cmd_norly(self, cmd, msg = None):#putcmd
        if msg != None:
            cmd = f'{cmd} {msg}{CRLF}'
        else:
            cmd = f'{cmd}{CRLF}'
        self.send(cmd)
            
    def send_cmd(self, cmd, msg = None):#cmd内的'\r'''\n'需要被转换为\\r\\n docmd
        self.send_cmd_norly(cmd, msg)
        return self.get_reply()
        
    def send_helo(self, msg = None):
        if msg == None:
            msg = self.local_host_hostname
        (reply_code, result_msgs) = self.send_cmd('helo', msg)
        return (reply_code, result_msgs)
    
    
    def send_ehlo(self, msg = None):#Reserved ESMTP extensions
        if msg == None:
            msg = self.local_host_hostname
        (reply_code, result_msgs) = self.send_cmd('ehlo', msg)
        return (reply_code, result_msgs)
        
        
    def send_noop(self):
        return self.send_cmd('noop')
    
    def send_rset(self):
        return self.send_cmd("rset")
    
    
    def send_mail(self, sender, option = None):#reserve option for Esmpt's fulture extension
        sender = self.mail_format(sender)
        return self.send_cmd("mail", f'FROM:{sender}')
    
    
    def mail_format(self, address):#address format xxxx@xx.xx to <xxxx@xx.xx>
#         displayname, addr = email.utils.parseaddr(addrstring)
        return f'<{address}>'


    def send_data(self, msg):
        (reply_code, result_msgs) = self.send_cmd('data', None)
        if int(reply_code) != 354:
            raise ResponseException(reply_code, result_msgs)
        else:
            msg = self._quote_periods(self._exchange_EOL(msg))
            if(msg[-2:] != CRLF):
                msg = msg + CRLF
            msg = msg + '.' + CRLF
            self.send(msg)
            (reply_code, result_msgs) = self.get_reply()
            return (reply_code, result_msgs)
                
            
    def _exchange_EOL(self, msg):#_fix_eols
        return  re.sub(r'(?:\r\n|\n|\r(?!\n))', CRLF, msg)#这个函数以后可以更新一下
    def _quote_periods(self, msg):#避免行首产生的.被识别为终止字符
        return re.sub(r'(?m)^\.', '..', msg)
    
    def send_rcpt(self, recp, option = None):#reserve option for Esmpt's fulture extension
        recp = self.mail_format(recp)
        return self.send_cmd("rcpt", f'TO:{recp}')
    
    def send_quit(self):
        respons = self.send_cmd("quit")
        self.close_socket()
        return respons
    
    def close_socket(self):
        sock = self.tcp_scoket
        self.tcp_scoket = None
        if sock:
            sock.close()

    def send_vrfy(self, address):#address format xxxx@xx.xx
        (reply_code, result_msgs) = self.send_cmd("vrfy", address)
        return (reply_code, result_msgs)
    
    def sendmail(self, sender, recps, msg):#sender 为邮件形式的地址xxx@xx.zz具体发送的ip地址（本地服务器）在self中存储
        #recps 的形式为列表化的发送对象，允许向多个邮件发送[1@1.1,2@2.2.....]
        (reply_code, result_msgs) = self.send_helo(self.local_host_hostname)
        if int(reply_code) != 250:
            self.close_socket()
            raise ResponseException(reply_code, result_msgs)
        (reply_code, result_msgs) = self.send_mail(sender)
        if int(reply_code) != 250:
            self.close_socket()
            raise ResponseException(reply_code, result_msgs)
        for recp in recps:
            (reply_code, result_msgs) = self.send_rcpt(recp)
            if int(reply_code) != 250 and reply_code != 251:
                self.close_socket()
                raise ResponseException(reply_code, result_msgs)
        (reply_code, result_msgs) = self.send_data(msg)
        if int(reply_code) != 250:
            self.close_socket()
            raise ResponseException(reply_code, result_msgs)
        return True
    
    def send_newmail(self, sender, recps, msg):
        (reply_code, result_msgs) = self.send_mail(sender)
        if int(reply_code) != 250:
            self.close_socket()
            raise ResponseException(reply_code, result_msgs)
        for recp in recps:
            (reply_code, result_msgs) = self.send_rcpt(recp)
            if int(reply_code) != 250 and int(reply_code) != 251:
                self.close_socket()
                raise ResponseException(reply_code, result_msgs)
        (reply_code, result_msgs) = self.send_data(msg)
        if int(reply_code) != 250:
            self.close_socket()
            raise ResponseException(reply_code, result_msgs)
        return True