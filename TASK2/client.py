import socket
import pickle
import sys, select
#PICKLE USED FOR SENDING AND RECEIVING USER DEFINED DATA TYPE
#SYS,SELECT USED FOR TAKING TIME CONTROLLED INPUT FROM THE USER

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((HOST, PORT))
        print("Connection Established")
        break
    except:continue


class Person():
    def __init__(self,origin,destination,direction):
        self.origin=origin
        self.destination=destination
        self.direction=direction

while True:
    try:
        data=s.recv(1024)
        if data.decode('utf')=='y':
#INPUT TO BE PUT UNDER 1 SECOND
            print("ENTER Y TO SEND INPUT IN 1 SEC")
            i, o, e = select.select( [sys.stdin], [], [],2)
            if (i):
                if sys.stdin.readline().strip()=='Y' or sys.stdin.readline().strip()=='y':
                    x=input("ENTER START")
                    y=input("ENTER DIRECTION")
                    z=input("ENTER DESTINATION")
                    if y=='U':
                        y=1
                    else:
                        y=-1
                    data=pickle.dumps(Person(int(x),int(z),int(y)))
                    while True:
                        try:
                            s.sendall(data)
                            break
                        except:
                            continue
                else :
                    while True:
                        try:
                            data=pickle.dumps('n')
                            s.sendall(data)
                            break
                        except:
                            continue
            else:
                while True:
                    try:
                        data=pickle.dumps('n')
                        s.sendall(data)
                        break
                    except:
                        continue


    except:
        continue

s.close()
