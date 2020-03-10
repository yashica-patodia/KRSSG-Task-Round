import math
import socket
from threading import Thread
import pickle
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
s.setblocking(0)

while True:
    try:
        conn, addr = s.accept()
        break
    except:
        continue
conn.setblocking(0)


MAX=100
FLOORS=20
U=1
D=-1
REST=0
import time

class Person():
    def __init__(self,origin,destination,direction):
        self.origin=origin
        self.destination=destination
        self.direction=direction

class Lift():
    def __init__(self,current_floor,destination):
        self.state=REST
        self.current_floor=current_floor
        self.destination=destination
        self.in_lift=[]
        self.path=0
        self.assigned=[]

class System():
    def __init__(self):
        self.lift1=Lift(0,0)
        self.lift2=Lift(0,0)
        self.waiting=[]
        self.time=0
        self.count=0

    def Time(self):
        self.time+=1
        time.sleep(1)
        while True:
            try:
                conn.sendall(b'y')
                break
            except:
                continue

        while True:
            try:
                data=conn.recv(4096)
                data_variable = pickle.loads(data)
                if data_variable=='n':
                    break
                else:
                    print("DATA RECEIVED")
                    self.waiting.append(data_variable)
                    self.count+=1
                    break
            except:
                continue
        print("TIME: ",self.time)

    def button_pressed(self,a,b,direction):
        p=Person(a,b,direction)
        self.waiting.append(p)
        self.count+=1


    def nearest_floor(self):
        if self.count==0:
            return

        if len(self.lift1.assigned)==0 and len(self.lift1.in_lift)==0:
            self.lift1.state=REST

        if len(self.lift2.assigned)==0 and len(self.lift2.in_lift)==0:
            self.lift2.state=REST


    #ONLY CALLED IF BOTH LIFTS ARE AT REST
        if len(self.waiting)>=2:
            #LIFT1
            if self.lift1.state==REST:
                distance=MAX
                for i in self.waiting:
                    if distance>abs(self.lift1.current_floor-i.origin):
                        near_floor=i.origin
                        self.lift1.destination=i.destination
                        #ADD FOR 0 CONDITION
                        if i.origin-self.lift1.current_floor==0:
                            self.lift1.state=REST
                        else:
                            self.lift1.state=int(abs(self.lift1.current_floor-i.origin)/(i.origin-self.lift1.current_floor))
                        distance=abs(self.lift1.current_floor-i.origin)

                for i in self.waiting:
                    if i.origin==near_floor and i.destination==self.lift1.destination:
                        self.lift1.assigned.append(i)
                        self.waiting.remove(i)
                        break

                self.update()

            if(len(self.waiting)!=0):
                #LIFT 2
                if self.lift2.state==REST:
                    near_floor=0
                    distance=MAX
                    for i in self.waiting:
                        if distance>abs(self.lift2.current_floor-i.origin):
                            near_floor=i.origin
                            self.lift2.destination=i.destination
                            if i.origin-self.lift2.current_floor==0:
                                self.lift2.state=REST
                            else:
                                self.lift2.state=int(abs(self.lift2.current_floor-i.origin)/(i.origin-self.lift2.current_floor))
                            distance=abs(self.lift2.current_floor-i.origin)



                    for i in self.waiting:
                        if i.origin==near_floor and i.destination==self.lift2.destination:
                            self.lift2.assigned.append(i)
                            self.waiting.remove(i)
                            break
                    self.update()

                if len(self.lift2.assigned)==0:
                    self.lift2.state=REST



        elif len(self.waiting)==1:
            if self.lift2.state==REST or self.lift1.state==REST:
                i = self.waiting[0]
                if abs(self.lift2.current_floor-i.origin)>abs(self.lift1.current_floor-i.origin):
                    self.lift1.destination=i.destination
                    self.lift1.state=int(abs(self.lift1.current_floor-i.origin)/(i.origin-self.lift1.current_floor))
                    self.lift1.assigned.append(i)
                    self.waiting.remove(i)

                else:
                    self.lift2.destination=i.destination
                    self.lift2.state=int(abs(self.lift2.current_floor-i.origin)/(i.origin-self.lift2.current_floor))
                    self.lift2.assigned.append(i)
                    self.waiting.remove(i)

                self.update()

            if len(self.lift2.assigned)==0:
                self.lift2.state=REST

            if len(self.lift1.assigned)==0:
                self.lift1.state=REST

    def move_lift(self):
        if self.lift1.state==REST and self.lift2.state==REST and len(self.waiting)!=0:
            self.nearest_floor()

        if self.count==0:
            return

        self.Time()

        self.lift1.current_floor+=self.lift1.state
        self.lift1.path+=abs(self.lift1.state)

        self.lift2.current_floor+=self.lift2.state
        self.lift2.path+=abs(self.lift2.state)

        self.pickCheck()
        self.dropcheck()

        if self.count==0:
            return
        else:
            self.move_lift()

    def pickCheck(self):
        for i in self.lift1.assigned:
            if i.origin==self.lift1.current_floor:
                self.lift1.in_lift.append(i)
                self.lift1.assigned.remove(i)
                self.lift1.destination=i.destination
                self.lift1.state=i.direction
                print("LIFT 1 PICKS PERSON FROM FLOOR ",i.origin)
                break

        for i in self.lift2.assigned:
            if i.origin==self.lift2.current_floor:
                self.lift2.in_lift.append(i)
                self.lift2.assigned.remove(i)
                self.lift2.destination=i.destination
                self.lift2.state=i.direction
                print("LIFT 2 PICKS PERSON FROM FLOOR ",i.origin)
                break

    def dropcheck(self):
        i=0
        while i<len(self.lift1.in_lift):
            if self.lift1.in_lift[i].destination==self.lift1.current_floor:
                print("LIFT 1 DROPS PERSON AT FLOOR ",self.lift1.in_lift[i].destination)
                self.lift1.in_lift.pop(i)
                self.count-=1
            else:
                i+=1
        i=0
        while i<len(self.lift2.in_lift):
            if self.lift2.in_lift[i].destination==self.lift2.current_floor:
                print("LIFT 2 DROPS PERSON AT FLOOR ",self.lift2.in_lift[i].destination)
                self.lift2.in_lift.pop(i)
                self.count-=1
            else:
                i+=1
        self.state_change()

    def state_change(self):
        distance=MAX
        for i in self.lift1.in_lift:
            if distance>abs(i.destination-self.lift1.current_floor):
                self.lift1.destination=i.destination
                self.lift1.state=(self.lift1.destination-self.lift1.current_floor)/abs(self.lift1.destination-self.lift1.current_floor)
                distance=abs(i.destination-self.lift1.current_floor)

        distance=MAX
        for i in self.lift2.in_lift:
            if distance>abs(i.destination-self.lift2.current_floor):
                self.lift2.destination=i.destination
                self.lift2.state=(self.lift2.destination-self.lift2.current_floor)/abs(self.lift2.destination-self.lift2.current_floor)
                distance=abs(i.destination-self.lift2.current_floor)

        if len(self.lift1.assigned)==0 and len(self.lift1.in_lift)==0:
            self.lift1.state=REST

        if len(self.lift2.assigned)==0 and len(self.lift2.in_lift)==0:
            self.lift2.state=REST

        if self.count==0:
            return

    def  update(self):
        if len(self.lift1.assigned)==0 and len(self.lift1.in_lift)==0:
            self.lift1.state=REST

        if len(self.lift2.assigned)==0 and len(self.lift2.in_lift)==0:
            self.lift2.state=REST

        if self.lift1.state!=REST:
            for i in self.waiting:
                if i.direction==self.lift1.assigned[0].direction and i.origin<=max(self.lift1.current_floor,self.lift1.destination) and i.origin>=min(self.lift1.current_floor,self.lift1.destination):
                    self.lift1.assigned.append(i)
                    self.waiting.remove(i)

        if self.lift2.state!=REST:
            for i in self.waiting :
                if i.direction==self.lift2.assigned[0].direction and i.origin<=max(self.lift2.current_floor,self.lift2.destination) and i.origin>=min(self.lift2.current_floor,self.lift2.destination):
                    self.lift2.assigned.append(i)
                    self.waiting.remove(i)

        if self.count==0:
            return

if __name__ =="__main__":
    system=System()
    n=input("ENTER NO.OF INITIAL INPUTS")
    for i in range(0,int(n)):
        x=input("ENTER START")
        y=input("ENTER DIRECTION")
        z=input("ENTER DESTINATION")
        if y=='U' or y=='u':
            y=1
        elif y=='D'or y=='d':
            y=-1
        system.button_pressed(int(x),int(z),int(y))
    system.move_lift()
    print("PATH1: ",system.lift1.path)
    print("PATH1: ",system.lift2.path)
