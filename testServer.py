from SMTPServer import SMTPServer

host = '192.168.0.184'  # 示例IP地址；根据需要更改
port = 25  # 示例端口；根据需要更改
smtp_server = SMTPServer(host=host, port=port)
smtp_server.start_server()