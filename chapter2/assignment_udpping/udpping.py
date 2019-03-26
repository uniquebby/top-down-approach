from socket import *
import time

#create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)
#assign server name and port
server_name = '124.16.114.185'
server_port = 12000
#set timeout
client_socket.settimeout(1)

for i in range(8):
    send_time = time.time()
    send_message = ('ping %d' %(i+1)).encode()
    try:
        client_socket.sendto(send_message, (server_name, server_port))
        responsemesg, server_addr = client_socket.recvfrom(1024)
        rtt = time.time() - send_time
        print('sequence %d: reply from %s RTT=%.3f' % (i+1, server_name, rtt))
    except Exception as e:
        print('sequence %d: request time out' % (i+1))

client_socket.close()
