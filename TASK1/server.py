import socket
from threading import Thread
import pickle
import time
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
s.setblocking(0)

minion_list=[]
connection_address=[]
i=0

total_minions=input("ENTER NO. OF MINIONS")
total_minions=int(total_minions)
total_minions+=1
while True:
    if i==total_minions:
        break
    try:
        conn, addr = s.accept()
        data=conn.recv(1024)
        if data.decode('utf-8')=='c':
            print(data.decode('utf-8'))
            client=conn
            client_address=addr

        elif data.decode('utf-8')=='m':
            minion_list.append(conn)
            connection_address.append(addr)
            print('Connected by', addr)
            print(data.decode('utf-8'))
        i=i+1
    except:
        continue

total=0
while True:
    try:
        data=client.recv(1024)
        total=int(data.decode('utf-8'))
        break
    except:
        continue

total_minions=total_minions-1
l=[]
total_args=0

while True:
    if total_args==total:
        break
    try:
        data=client.recv(5)
        x=int(data.decode('utf-8'))
        print(x)
        l.append(x)
        total_args+=1
    except:
        continue

for i in range(0,total_minions):
    minion_list[i].setblocking(0)

client.setblocking(0)

def minion_send(l,x):
    data=pickle.dumps(l)
    while True:
        try:
            minion_list[x].send(data)
            break
        except:
            continue

threads=[]
i=0
minion_count=0

while i<total_args:
    if (total_args%total_minions)!=0:
        step=int((total_args+total_minions-total_args%total_minions)/total_minions)
    else:
        step=int(total_args/total_minions)
    if i+step>total_args:
        step=total_args-i
    t1=Thread(target=minion_send,args=(l[i:i+step],minion_count))
    threads.append(t1)
    t1.start()
    i=i+step
    minion_count+=1

for t in threads:
    t.join()

l=[]
thread1=[]
i=0

for i in range(0,total_minions):
    minion_list[i].setblocking(0)
    l.append(0)

def minion_take(x):
    while True:
        try:
            data=minion_list[x].recv(2048)
            if not data:
                continue
            l[x]=int(data.decode('utf-8'))
            break
        except:
            continue

i=0
while i<total_minions:
    t=Thread(target=minion_take,args=(i,))
    thread1.append(t)
    i+=1
    t.start()

for k in thread1:
    k.join()

sum=0
for i in l:
    print(i)
    sum+=i

print(sum)
time.sleep(1)
while True:
    try:
        client.sendall(str(sum).encode('utf-8'))
        break
    except:
        continue
s.close()
