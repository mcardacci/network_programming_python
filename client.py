import socket

s=socket.socket()
host=socket.gethostname()
port=17327

s.connect((host,port))
print s.recv(1024)
s.close()