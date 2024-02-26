# smtpclient library usage documentation:
Using the interface provided by smtplib, you can apply the smtp protocol based on RFC5321 to transmit emails to the local smtp server.

## First you need to introduce the smtpclient library
import smtpclient

## Secondly, you need to create a client object
### smtp = smtpclient.client_SMTP(local_smtpserver_address,server_port,[local_host_hostname,source_address], time_out)
If the creation is successful, "connect success" will be returned, indicating that the socket link has been successfully established with the server.
An exception will be thrown if it fails or times out.

## In the third step, you can choose to send the email directly through the encapsulated sendmail function, or follow the SMTP protocol to send the corresponding email step by step.

### 1
#### class smtpclient.sendmail(sender, recps, msg)

sender is source email address based on a string, for example: "source@mail.com"
recps is a list of recipients in the form ["1@1.1", "2@2.2...."]

msg is the content sent by email, such as: 

msg="""\
From: sender@example.com

To: recipient@example.com

Subject: Test email

This is the body of the email.
"""

After the sending is completed, send the quit command to delete the object and disconnect the socket.

class smtpclient.send_quit()
### 2
#### Send emails according to the basic sequence of HELO MAIL RCPT DATA QUIT, which can be interspersed with commands such as noop rset vrfy

class smtpclient.send_helo():
send helo command

class smtpclient.send_ehlo():
send ehlo command

class smtpclient.send_mail(sender):
sender is source email address based on a string, for example: "source@mail.com"

class smtpclient.send_rcpt(recp):
sender is traget email address based on a string, for example: "traget@mail.com"

class smtpclient.send_data(msg):
msg is the content sent by email

class smtpclient.send_quit():
delete the object and disconnect the socket

class smtpclient.send_vrfy(address):
test if address is valid or not

class smtpclient.send_rset():
change to the state after send helo

class smtpclient.send_noop():
test if the connection is ok or not


