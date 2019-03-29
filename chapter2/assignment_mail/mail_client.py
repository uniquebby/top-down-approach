from socket import *
import base64
msg = "\r\n this is a test mail for my learning computer networking"
endmsg = "\r\n.\r\n"
subject = "learning computer networking"
contenttype = "text/plain"
# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver = "smtp.163.com"#Fill in start   #Fill in end
# Sender and reciever
fromaddress = "15367145356@163.com"
toaddress = "852352700@qq.com"

# Auth information (Encode with base64)
username = 'MTUzNjcxNDUzNTZAMTYzLmNvbQ=='
password = 'bHk4NjExMTExMQ=='
# Create socket called clientSocket and establish a TCP connection with mailserver
#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))
#Fill in end
recv = clientSocket.recv(1024)
print (recv)
if recv[:3] != '220':
    print ('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024)
print (recv1)
if recv1[:3] != '250':
    print ('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
# Auth
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')

clientSocket.sendall((username + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '334'):
	print('334 reply not received from server')

clientSocket.sendall((password + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '235'):
	print('235 reply not received from server')
    
 # Send MAIL FROM command and print server response.
clientSocket.sendall(('MAIL FROM: <' + fromaddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')   
	
# Send RCPT TO command and print server response.
clientSocket.sendall(('RCPT TO: <' + toaddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')

# Send DATA command and print server response.
clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '354'):
	print('354 reply not received from server')
# Fill in end

# Send message data.
# Fill in start
message = 'from:' + fromaddress + '\r\n'
message += 'to:' + toaddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contenttype + '\t\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

# Fill in end 

# Message ends with a single period.
# Fill in start
clientSocket.sendall(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
	print('250 reply not received from server')
# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.sendall('QUIT\r\n'.encode())
# Fill in end
#close connection
clientSocket.close()
