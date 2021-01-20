from socket import *
from select import select
import re


class WebServer:
    def __init__(self,host="",port=0,html=""):
        self.host=host
        self.port=port
        self.html=html
        self.address=(host,port)
        self.sock=self.__create_socket()
    def __create_socket(self):
        sock=socket()
        sock.bind(self.address)
        sock.setblocking(False)
        sock.listen(5)
        return sock

    def do_request(self,data,connfd):
        temp=re.findall('\s/(\S+)\.html',data)
        if len(temp)>0:
            filename=self.html+"/"+temp[0]+".html"
            print("filename_:"+filename)
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            with open(filename) as f:
                response += f.read()
                connfd.send(response.encode())


    def handle(self,data,rlist,connfd):
        if not data:
            rlist.remove(connfd)  # 不再监控
            connfd.close()
            return
        print(data)
        self.do_request(data,connfd)
        #connfd.send(b"OK")

    def myselect(self):
        # 设置要监控的IO
        rlist = [self.sock]  # 初始监控
        wlist = []
        xlist = []
        # 循环接收客户端连接
        while True:
            rs, ws, xs = select(rlist, wlist, xlist)
            # 逐个取值，分情况讨论
            for r in rs:
                if r is self.sock:  # 判断对象是否为同一个 is
                    connfd, addr = r.accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    rlist.append(connfd)
                else:
                    # 连接套接字就绪
                    data = r.recv(1024).decode()
                    self.handle(data,rlist,r)

    def start(self):
        self.myselect()


if __name__ == '__main__':
    httpd=WebServer(host="0.0.0.0",port=8008,html="./static")
    httpd.start()