"""
http请求和响应演示

"""

from socket import *

file=open("my.html","rb")
text=""
while True:
    data=file.read(1024)
    if not data:
        text+=data.decode()

sock=socket()
sock.bind(("0.0.0.0",1784))
sock.listen(5)

connfd,addr=sock.accept()
print("connect from ",addr)

request=connfd.recv(1024)
print(request.decode())
response="""HTTP/1.1 200 OK
Content-Type:text/html

hello world
"""



connfd.send(response.encode())

connfd.close()
sock.close()