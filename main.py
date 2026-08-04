import os
from socket import *


#http://192.168.0.17:12000/test.html

#responses
forbidden = ( "HTTP/1.1 403 Forbidden\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "Connection: close\r\n"
    "\r\n"
    "<html><body><h1>403 Forbidden - Access Denied</h1></body></html>"
)

not_modified = (
    "HTTP/1.1 304 Not Modified\r\n"
    "Connection: close\r\n"
    "\r\n" 
)

not_supported = (
    "HTTP/1.1 505 HTTP Version Not Supported\r\n"
    "Connection: close\r\n"
    "\r\n"
)

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(1)
    print("server is listening")
    print(forbidden)
    while True:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024).decode()
        if not message.strip():
            connectionSocket.close()
            continue
        lines = message.split("\r\n")
        #decide how to deal with Http requests 
        connectionSocket.send(forbidden.encode())
        connectionSocket.close()


main()
