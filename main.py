import os
from socket import *




def main():
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(1)
    print("server is listening")

    while True:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(1024).decode()
        #decide how to deal with Http requests 
        connectionSocket.close()


main()
