#!/usr/bin/env python3

import rospy
import time
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import time


        



class velcoms():
    
    
    
    def __init__(self) :
        rospy.init_node("nav", anonymous=True)
        self.todo=[5]
        self.done=[]
        self.x = -1
        self.arr=[]
        #self.d = 0
        cmd_vel_topic = "/cmd_vel"
        self.velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        self.velocity = Twist()
        self.rate = rospy.Rate(10)
        info = rospy.Subscriber("aruco", String, self.callback)

        self.run()

        
        
    
    def callback(self,a):
        
        print("callbacked")
        self.arr=eval(a.data)
        #print(self.arr)
        if len(self.arr)<=0:
            self.x=-1
            self.d=0
            
        for i in self.arr:
            if i[0]==self.todo[0]:
                self.x=self.todo[0]
                self.d=i[1]
                print(self.x,i)
        print("mkh")
        print(self.arr)
        





    def move_straight(self,z):
        t0 = rospy.Time.now().to_sec()
        D=0
        
        while self.x !=self.todo[0] and D < self.d-self.z:
            print("found,moving strt")
            self.velocity.linear.x = 0.1
            self.velocity_publisher.publish(self.velocity)
            t1 = rospy.Time.now().to_sec()
            D = 0.5 * (t1 - t0)
            print(self.x,self.d,D)
        
        self.velocity.linear.x = 0
        self.velocity_publisher.publish(self.velocity)

        #return self.d-z
        
    
    def run(self):
        
        print('<<>><<>><<>>')
        time.sleep(10)

        
        if len(self.arr)>0:
            print(self.arr)
        
            self.move_straight(20)
            self.x=self.todo.pop[0]
            print("found")
                    

        else:
            self.rot360()
            if self.x>=0:
                self.move_straight(20)
                print("found")
        
    
    def goto(self):
        pass

    def rot360(self):
        yaw=0
        t0 = rospy.Time.now().to_sec()
        

        while self.x!=self.todo[0] and yaw<3.14:
            
            print("not found",self.x)
            #print("found,rotating",yaw)
            self.velocity.angular.z = 0.1
            self.velocity_publisher.publish(self.velocity)
            t1 = rospy.Time.now().to_sec()
            yaw = 0.1 * (t1 - t0)

            
        self.velocity.angular.z = 0
        self.velocity_publisher.publish(self.velocity)

        self.run()
        

    def move_90deg(self):
        theta=0
        t0 = rospy.Time.now().to_sec()
        while theta<1.57:
            print("found,rotating",theta)
            self.velocity.angular.z = 0.1
            self.velocity_publisher.publish(self.velocity)
            t1 = rospy.Time.now().to_sec()
            theta = 0.1 * (t1 - t0)
        print("Loop broken")
        self.velocity.angular.z = 0
        self.velocity_publisher.publish(self.velocity)

if __name__ == "__main__":
    try:
        main=velcoms()
        rospy.spin()
        

    except rospy.ROSInterruptException:
        rospy.loginfo("node_terminated")
