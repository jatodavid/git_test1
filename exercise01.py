from socket import socket

def handel(connfd):
    request = connfd.recv(1024)
    if not request:
        return
    print(request.decode())
    # 组织响应
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"

    with open("my.html") as f:
        response+=f.read()
    connfd.send(response.encode())

def main():
    sock = socket()
    sock.bind(("0.0.0.0", 1784))
    sock.listen(5)
    # 等待浏览器连接
    while True:
        connfd, addr = sock.accept()
        print("connect from ", addr)
        handel(connfd)
        connfd.close()

if __name__ == '__main__':
    main()