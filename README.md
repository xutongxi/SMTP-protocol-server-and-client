# SMTP-protocol-server-and-client
based on python to achieve SMTP protocol

SMTP协议与服务器配置基于Python与Linux，更详细的版本说明会在之后添加

## 服务器功能如下：
1. 设置监听端口，监听SMTP默认端口发送的TCP连接请求
2. 接到请求后按照SMTP协议与客户端进行交互，并尝试接收邮件
3. 如果邮件域名为本机域名，则将邮件保存，然后后续客户端可通过pop3协议获取邮件
4. 如果为其他邮件服务器域名，则与其他服务器通过SMTP协议将邮件发送到其他服务器
   
## 为实现功能，代码结构如下所写
1. 实现sesmtp库以便主函数运行（包括了所有服务器端SMTP协议的功能）
2. 设置主函数，实现SMTP服务器（更详细过程在代码过程中补充）