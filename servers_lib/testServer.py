from SMTPserver import SMTPServer

host = '163.123.183.116'  # 示例IP地址；根据需要更改
port = 25  # 示例端口；根据需要更改
smtp_server = SMTPServer(host=host, port=port)
smtp_server.start_server()