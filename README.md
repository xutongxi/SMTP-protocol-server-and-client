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
