#!/usr/bin/env python
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Float32MultiArray

time_check=0
from math import pow, atan2, sqrt
import time
import math
flag=0

class TurtleBot:

    def __init__(self):

        rospy.init_node('turtlebot_controller', anonymous=True)


        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=10)
        self.villain_subscriber=rospy.Subscriber('/turtle2/pose',Pose,self.update_v_pose)

        self.velocity2_publisher=rospy.Publisher('/turtle2/cmd_vel',
                                                  Twist, queue_size=10)
        self.warning_publisher=rospy.Publisher('chatter',Float32MultiArray,queue_size=10)

        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)



        self.pose = Pose()

        self.villain_pose=Pose()

        self.rate = rospy.Rate(10)


    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def update_v_pose(self,data):
        self.villain_pose=data
        self.villain_pose.x = round(self.villain_pose.x, 4)
        self.villain_pose.y = round(self.villain_pose.y, 4)

    def distance(self, goal_pose):

        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))

    def linear_vel(self, goal_pose, constant=1.5):

        return constant * self.distance(goal_pose)

    def steering_angle(self, goal_pose):
        if(goal_pose.x==self.pose.x and goal_pose.y>self.pose.y):
            return math.pi/2
        elif(goal_pose.x==self.pose.x and goal_pose.y<self.pose.y):
            return -math.pi/2
        elif(goal_pose.x==self.pose.x and goal_pose.y==self.pose.y):
            return self.pose.theta

        if(goal_pose.y==self.pose.y and goal_pose.x>self.pose.x):
            return 0;
        if(goal_pose.y==self.pose.y and goal_pose.x<self.pose.x):
            return math.pi

        if(abs(atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)-self.pose.theta)<abs(-2*math.pi+atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)-self.pose.theta)):
            return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
        else:
            return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)-2*math.pi



    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

    def move2goal(self,target):
        goal_pose=target
        tolerance=0.05
        Kp1=6
        Ki1=0
        Kd1=0
        error1=self.steering_angle(goal_pose)-self.pose.theta
        prev_error1=error1
        integral1=0.0
        diff1=error1*10

        Kp=1.5
        Ki=0
        Kd=0
        error=self.distance(goal_pose)
        prev_error=error
        integral=0.0
        diff=error*10
        vel_msg=Twist()
        global flag
        flag=0

        while(abs(self.steering_angle(goal_pose)-self.pose.theta)>=tolerance or self.distance(goal_pose) >=tolerance ):
            global flag
            flag=0
            error1=self.steering_angle(goal_pose)-self.pose.theta
            integral1+=error1*0.1
            diff1=(error-prev_error1)*10
            prev_error1=error1
            angular_velocity=Kp1*error1 +Ki1*integral1 +diff1*Kd1

            error=self.distance(goal_pose)
            integral+=error*0.1
            diff=(error-prev_error)*10

            prev_error=error
            linear_velocity=Kp*error +Ki*integral +diff*Kd

            vel_msg.linear.x =linear_velocity
            vel_msg.linear.y=0
            vel_msg.linear.z=0

            vel_msg.angular.x=0
            vel_msg.angular.y=0
            vel_msg.angular.z=angular_velocity
            self.velocity_publisher.publish(vel_msg)
            vel_msg.linear.x =2.544
            vel_msg.angular.z=1
            self.velocity2_publisher.publish(vel_msg)

            self.rate.sleep()

            if(self.distance(self.villain_pose)<2 and int(time.time()-time_check)>2):
                print(int(time.time()-time_check))
                while not rospy.is_shutdown() :
                    try:
                        l=[self.pose.x,self.pose.y,self.villain_pose.x,self.villain_pose.y]
                        warning_message=Float32MultiArray()
                        warning_message.data=l
                        print(self.distance(self.villain_pose))
                        self.warning_publisher.publish(warning_message)
                        global flag
                        flag=1
                        print("SENT")
                        vel_msg.linear.x=0
                    	vel_msg.linear.y=0
                    	vel_msg.linear.z=0

                    	vel_msg.angular.x=0
                    	vel_msg.angular.y=0
                    	vel_msg.angular.z=0

                    	self.velocity_publisher.publish(vel_msg)
                        self.velocity2_publisher.publish(vel_msg)

                        time.sleep(2)
                        global time_check
                        time_check=time.time()
                        break
                    except:continue

            if flag==1:
                break




if __name__ == '__main__':
    try:
        global flag
        count=0
        x = TurtleBot()
        l=[]
        file=open("task.txt")

        l=file.readlines()
        i=0
        s=len(l)
        while (s>0):
            global i
            j=l[i]
            i+=1
            pass
            global count
            count+=1
            coordinate=j.split()
            pos=Pose()
            a=float(coordinate[0])
            b=float(coordinate[1])
            pos.x=a
            pos.y=b
            print("{}".format(count))
            x.move2goal(pos)
            if flag==1:
                global s
                global l
                global file
                file.close()
                file=open("task.txt")
                l=file.readlines()
                s=len(l)
                print(len(l))
                global flag
                flag=0
                global i
                i=0;

    except rospy.ROSInterruptException:
        pass
