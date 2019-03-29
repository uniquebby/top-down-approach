#coding:utf-8
from socket import *
import socket as soc 
import ssl
import zlib

# 创建socket，绑定到端口，开始监听
tcpSerPort = 10000 
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)
while True:
    # 开始从客户端接收请求
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    message = tcpCliSock.recv(4096).decode()
    # 从请求中解析出filename
    filename = message.split()[1][1:]#split分出port后的部分
    filename1 = filename.replace('/', '\\')#文件名带分隔符无法创建文件
    print(filename)
    fileExist = "false"
    try:
        # 检查缓存中是否存在该文件
        f = open(filename1, "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('File Exists!')
        # 缓存中存在该文件，把它向客户端发送
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        print('Read from cache')
    # 缓存中不存在该文件，异常处理
    except FileNotFoundError:
        print('File Exist: ', fileExist)
        if fileExist == "false":
            # 在代理服务器上创建一个tcp socket
            print('Creating socket on proxyserver')
            #s = ssl.wrap_socket(soc.socket())#建立发https请求的socket
            try:
                # 连接到远程服务器80(http)端口
                s = socket(AF_INET, SOCK_STREAM)
                hostname = filename.partition('/')[0]
                s.connect((hostname, 80))
                print('Socket connected to port 80 of the host')
                url = filename.partition('/')[2]#URL 
                message = message.replace(filename, '', 1)
                message = message.replace('localhost', hostname)
                message = message.replace(':' + str(tcpSerPort) , '')
                message = message.replace('Accept-Encoding: gzip, deflate, br\r\n', '')
                s.send(message.encode())
                # Read the response into buffer
                buf = s.recv(4096).decode('utf8', 'ignore')
                s.close()
                print(buf)
                filename1 = './' + filename1
                tmpf =  open(filename1, 'w')
                #for i in range(len(buf)):
                tmpf.write(buf)
                print(tcpCliSock.send(buf.encode()))
            except Exception as e:
                print(e)
        else:
            # HTTP response message for file not found
            # Do stuff here
            print('File Not Found...Stupid Andy')
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()
