import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((HOST, PORT))
        break
    except:continue

s.sendall(b'c')

n=input("ENTER NO. OF ELEMENTS")
s.sendall(n.encode('utf-8'))
for x in range(0,int(n)):
    i=input("ENTER NUMBER")
    s.sendall(i.encode('utf-8'))
    #s.sendall(b'Hello, world')
s.setblocking(0)

while True:
    try:
        sum=s.recv(1024)
        print(int(sum.decode('utf-8')))
        break
    except:
        continue

s.close()
