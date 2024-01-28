# SMTP-protocol-server-and-client
based on python to achieve SMTP protocol

SMTP协议与客户端配置基于Python与Linux，更详细的版本说明会在之后添加

## 客户端功能如下
1. 启动后，首先接收用户的邮件名输入（基本配置）
2. 基于用户的输入尝试连接SMTP
3. 连接成功后，进入邮件发送程序、
4. 发送成功后断开连接

## 为实现功能，代码结构如下所写
1. 实现pysmtp库以便主函数运行（包括了所有SMTP协议的功能）
2. 设置主函数，实现SMTP客户端（更详细过程在代码过程中补充）


SMTP协议与服务器配置基于Python与Linux，更详细的版本说明会在之后添加

## 服务器功能如下：
1. 设置监听端口，监听SMTP默认端口发送的TCP连接请求
2. 接到请求后按照SMTP协议与客户端进行交互，并尝试接收邮件
3. 如果邮件域名为本机域名，则将邮件保存，然后后续客户端可通过pop3协议获取邮件
4. 如果为其他邮件服务器域名，则与其他服务器通过SMTP协议将邮件发送到其他服务器

## 为实现功能，代码结构如下所写
1. 实现sesmtp库以便主函数运行（包括了所有服务器端SMTP协议的功能）
2. 设置主函数，实现SMTP服务器（更详细过程在代码过程中补充）


def sendMail(sender_addr, receiver_addr, msg)
    sender_addr是一个字符串，是发送者的邮箱地址
    receiver_addr是一个字符串列表，表示收件人的邮箱地址。如果只有一个字符串就代表只有一个收件人
    msg是消息字符串


def helo(name=''):
    使用 HELO 向 SMTP 服务器表明自己的身份。
    在python的stmp库中，这个方法并不需要明确调用，一般是被sendMail()进行隐式调用

def quit():
    退出链接

def login(user,password):
    登录到一个需要验证的SMTP服务器，参数是认证的用户名和密码

def set_Debuglevel(level):
    设置调试输出级别。 如果 level 的值为 1 或 True ，就会产生连接的调试信息，以及所有发送和接收服务器的信息。 如果 level 的值为 2 ，则这些信息会被加上时间戳

def docmd(cmd)
    向服务器发送一条命令cmd

## docmd函数可以发送的cmd命令有：HLEO, EHLO, MAIL, RCPT, DATA, RSET, VRFY, EXPN, NOOP, QUIT, 

