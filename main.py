import os
from socket import *


#http://192.168.0.17:12000/test.html
TEST_DATE = "Tue, 28 Jul 2026 18:14:00 GMT"
TEST_VERSION = "HTTP/1.1"

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

not_found = ( "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "Connection: close\r\n"
    "\r\n"
    "<html><body><h1>404 Not Found</h1></body></html>"
)

response_200 = ( "HTTP/1.1 200 OK\r\n"
    f"Last-Modified: {TEST_DATE}\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "Connection: close\r\n"
    "\r\n"
    "<html><body><h1>200 OK - File Successfully Served</h1></body></html>"
)

#checks if you message has been modified 
def check_if_modified(msg, date):

    split_msg = msg.split("\r\n")
    modified_since = None

    #searches for the if-modified-since header
    for line in split_msg:
        
        if line.lower().startswith("if-modified-since:"):
            # Split exactly once at the first colon to isolate the date string
            parts = line.split(":", 1)
            if len(parts) == 2:
                modified_since = parts[1].strip()
            break  # Found it
            
    
    if modified_since and modified_since == date:
        return True

    return False

#checks the Http version
#returns true if version is different
def check_version(msg,version):

    #extracts the html version
    msg_version = msg.split("\r\n", 1)[0].split(" ")[-1]

    if version != msg_version:
        return True

        
    return False


#returns (true,file name) if file is in directory
def check_file(msg):
    #extracts the file name
    request = msg.split("\r\n",1)[0]
    file_name = request.split(" ")[1]
    file_name = file_name.lstrip("/")

    #checks if file is in current directory
    if os.path.exists(file_name) and os.path.isfile(file_name):
        return (True,file_name)

    return (False,"Not Found")


def hol_blocking():
    print("In progress")

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(1)
    print("server is listening")
    

    
    while True:
        connectionSocket, addr = serverSocket.accept()
        #assume we are only getting GET requests
        message = connectionSocket.recv(1024).decode()
        if not message.strip():
            connectionSocket.close()
            continue

        #check if the we are using the same Http version
        if check_version(message,TEST_VERSION):
            connectionSocket.send(not_supported.encode())
            connectionSocket.close()
            continue

        #check if modified by a date that we send        
        if check_if_modified(message,TEST_DATE):
            connectionSocket.send(not_modified.encode())
            connectionSocket.close()
            continue

        #check if file is present in the directory.
        #if True sends 200 ok with file. 
        #if False sends 404 not found
        (in_directory, name) = check_file(message)
        if in_directory:
            with open(name, "r", encoding= "utf-8") as file:
                file_content = file.read()

            response_200 = (
                            "HTTP/1.1 200 OK\r\n"
                            f"Last-Modified: {TEST_DATE}\r\n"
                            "Content-Type: text/html; charset=utf-8\r\n"
                            f"Content-Length: {len(file_content.encode('utf-8'))}\r\n" # Tells browser file size
                            "Connection: close\r\n"
                            "\r\n"
                            f"{file_content}"
                            )
            connectionSocket.send(response_200.encode('utf-8'))
            connectionSocket.close()
            continue

        else:
            connectionSocket.send(not_found.encode())
            connectionSocket.close()
            continue

        


main()
