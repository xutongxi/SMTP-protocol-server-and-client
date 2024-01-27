# achieve smtp  protocol

#----------------------------------server api
#SMTP 实例是对 SMTP 连接的封装，实现所有SMTP代码
#     客户端函数
#class smtp_client.SMTP(host='', port=0, local_hostname=None,source_address=None)
#后续可进行超时时间的编码：浮点数或None，定义连接到SMTP服务器的超时时间。

#     服务器端函数
#创建对象调用后可以对端口进行监听
#reply 220响应 服务器准备就绪

#reply 554响应 服务器不接受服务，等待客户端回复quit

#客户端顺序出错时reply “503错误的命令顺序”

#reply220后接收HELO命令 回复250

#对EHLO返回command not recognized


#接收Mail from命令返回250 OK回复
#如果不能接受（则返回失败原因）例如reverse path不可用
#无先前 503

#接收rcpt命令 rcpt路径，检验rcpt地址是否可达，
#可达情况下，存储路径并返回250
#不可交付返回550 无此类用户
#无先前 503

#接收data命令
#（不为仅包含“.”（句点或句号）的行）接受，SMTP服务器返回354中间回复，将所有后续行（包括但不包括邮件结束数据指示符）视为邮件文本
    #成功接收并存储文本结尾后，回复250 OK.
#（为仅包含“.”（句点或句号）的行）
    #回复250 OK.
# 非data命令
    #503 554

