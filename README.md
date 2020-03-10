# KRSSG-Task-Round

## Task 1:
### Implementation of Socket Programming and MultiThreading
        Approach-I used TCP to send and recieve data and used the socket module avaiable in python to implement 
        the same and for multithreading i used the threading module         

        
        Running:-
        1.Run the server python script and enter the minion workforce size(x)
        2.In a different Terminal run the Client python script
        3.Open x terminals and run the minion script in each of them

## Task 2:
### Implementation of working of a Dual Elevator System using FSM(Finite State Machine) with dynamic input and initial input 
        
        Approach-Implemented finite state machines for the lift encounter problem using basic knowledge of classes in python
        and tried to use inheritance wherever possible.For Dynamic input I added a function for the flow of time and used 
        socket programming learnt in Task1 for sending and receiving data from The client side to the lift system side 
        
        Running:-
        1.Run the lift python script
        2.Run the client python script in another Terminal
        3.Enter an input for number of initial inputs(>0) in the lift and Enter Y during the 
        execution of code in the client terminal to add dynamic input 
        
        Input Format-INITIAL FLOOR DIRECTION(U/D) TARGET FLOOR
        
        
## Task 3:
### Path Planning using RRT*_Connect and mimicing it on ROS TurtleSim\
         Approach-Implemented the RRT* version of RRT_connect.Used ROS,file handling and used P of PID
         (Coudn't find other coeffs) for path following of turtlesim
         and for dynamic path planning 
             
         Prerequisites:
         1.OpenCV
         2.ROS Kinetic
               
         Compilation For Task3a:
         1. Use make rrt*_connect and run the created executable
         
         Setup for task 3b and 3c:
         1.Create a catkin workspace and add the Task folder in the src directory.
         2.Run the catkin_make command in the workspace and source the package name from the setup.bash 
         file in the devel directory by running the command 'source devel/setup.bash'
         3.add the 'task.png' image to the catkin workspace
         3.Open turtlesim_node using rosrun
         4.Use 'rosrun task listener' and 'rosrun task listener.py file to run the scripts 
         5.For Task 3c spawn another turtle at x=5.44,y=2 and run the scripts again 
         
## Task 4:
        Observed features of the PPo agent and the environment noted in a .txt file
        
        
        

                               
                
                
        
