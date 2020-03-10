import socket
import time
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((HOST, PORT))
        break
    except:continue

s.sendall(b'm')
s.setblocking(0)

sum=0
while True:
    try:
        data=s.recv(4096)
        data_variable = pickle.loads(data)
        for i in data_variable:
            print(i)
            sum+=i
            time.sleep(2)
        break
    except:continue

print(sum)
'''while True:
    try:
        s.send(str(sum).encode('utf-8'))
        break
    except:6

        continue
'''
while True:
    try:
        s.send(str(sum).encode('utf-8'))
        break
    except:continue

s.close()
