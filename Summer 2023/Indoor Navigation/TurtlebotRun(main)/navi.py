#!/usr/bin/env python

import rospy
from math import pi,sqrt
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class nav:
    x=0
    def __init__(self):
        rospy.init_node("nav", anonymous=True)
        self.vel = Twist()
        self.todo=[0,2,1]
        self.cmd_vel_topic = "/cmd_vel_mux/input/navi"
        self.info = rospy.Subscriber("aruco", String, self.callback)
        self.vel_pub = rospy.Publisher(self.cmd_vel_topic, Twist, queue_size=10)
        self.rate = rospy.Rate(10)
        self.x = None

    def callback(self, a):
        if a.data:
            self.x = eval(a.data)[0]
            nav.x=self.x
            self.dist = eval(a.data)[1]
            self.centroid = eval(a.data)[2]
            
    
    def zed(self,k):
        while k>=0.01:
            print("Slowing",k)
            self.vel.linear.x=k-0.05
            k-=0.05
            self.vel_pub.publish(self.vel)
            rospy.sleep(.2)
        self.vel.linear.x=0
        self.vel_pub.publish(self.vel)
        

    def select_marker(self):
        '''if len(self.x) > 1:
            del self.x[1:]
            del self.dist[1:]
            del self.centroid[1:]'''
        index=self.x.index(self.todo[0])
        print(index)
        if index>0:
            return index
        
        else:
            return 0

    def marker_config(self, id):
        print("Configured")
        self.cmd = None
        if id == 0 or id == 2:
            self.cmd = "Right"
        elif id == 1 or id == 3:
            self.cmd = "Left"

    def centering(self):
        print("centring",self.centroid,self.i)
        if self.centroid[self.i][0] < 310:
            while self.centroid[self.i][0] < 310:
                self.vel.angular.z = 0.2
                self.vel_pub.publish(self.vel)

        if self.centroid[self.i][0] > 330:
            while self.centroid[self.i][0] > 330:
                self.vel.angular.z = -0.2
                self.vel_pub.publish(self.vel)

        self.vel.angular.z = 0
        self.vel_pub.publish(self.vel)

    def detected(self):
        print(self.todo)
        
        self.i=self.select_marker()
        print("detected", self.dist[self.i])
        self.marker_config(self.x[self.i])
        print(self.cmd)
        
        '''if self.cmd == None:
            print(self.x[0])'''

        if self.dist[self.i] > 70 and self.cmd:
            print("hjjf")
            while self.dist[self.i] > 70 :
                print(self.dist[self.i])
                print("Loop")
                self.vel.linear.x = 0.2
                self.vel_pub.publish(self.vel)
                self.centering()
                self.rate.sleep()
                if self.x[0]==-1:
                  print(self.x)
            print("jbcuysdbfsdbvu",self.dist[self.i])
            self.zed(self.vel.linear.x)

        if self.cmd == "Right":
            print("Right")
            theta = 0
            t1 = rospy.Time.now().to_sec()
            while theta <= pi:
                print("Rotating")
                self.vel.angular.z = -0.2
                self.vel_pub.publish(self.vel)
                t2 = rospy.Time.now().to_sec()
                theta = (t2 - t1) * (-1 * self.vel.angular.z)
                if len(self.todo)>1 and self.todo[1] in self.x :
                    print()
                    del self.todo[0]
                    print(self.todo)
                    self.detected()
                    return
                self.rate.sleep()
            self.vel.angular.z = 0
            self.vel_pub.publish(self.vel)
            t = rospy.Time.now().to_sec()
            d = 0
            while d <= 10:
                self.vel.linear.x = 0.2
                self.vel_pub.publish(self.vel)
                t2 = rospy.Time.now().to_sec()
                d = (t2 - t) * (self.vel.linear.x)
                if len(self.todo)>1 and self.todo[1] in self.x :
                    
                    del self.todo[0]
                    print(self.todo)
                    self.detected()
                    return
                self.rate.sleep()
            self.zed(self.vel.linear.x)

        if self.cmd == "Left":
            print("Left")
            theta = 0
            t1 = rospy.Time.now().to_sec()
            while theta <= pi:
                self.vel.angular.z = 0.2
                self.vel_pub.publish(self.vel)
                t2 = rospy.Time.now().to_sec()
                theta = (t2 - t1) * self.vel.angular.z
                if len(self.todo)>1 and self.todo[1] in self.x :
                    del self.todo[0]
                    self.detected()
                    return
                self.rate.sleep()
            self.vel.angular.z = 0
            self.vel_pub.publish(self.vel)
            t = rospy.Time.now().to_sec()
            d = 0
            while d <= 1:
                self.vel.linear.x = 0.2
                self.vel_pub.publish(self.vel)
                t2 = rospy.Time.now().to_sec()
                d = (t2 - t) * (self.vel.linear.x)
                if len(self.todo)>1 and self.todo[1] in self.x[0] :
                    del self.todo[0]
                    self.detected()
                    return
                self.rate.sleep()
            self.zed(self.vel.linear.x)
        
        del self.todo[0]
        if len(self.todo)>0:
            self.explore()
        

    def explore(self):
        print("Exploring")
        while self.x == None or self.todo[0] not in self.x:
            dist = 0
            ang = 0
            t0 = rospy.Time.now().to_sec()
            while self.x == None or self.todo[0] not in self.x:
                print("Exp,ROtation")
                self.vel.angular.z = 0.2
                self.vel_pub.publish(self.vel)
                t2 = rospy.Time.now().to_sec()
                ang = 0.2 * (t2 - t0)
                if ang >= pi / 2:
                    break
            self.vel.angular.z = 0
            self.vel_pub.publish(self.vel)
            t = rospy.Time.now().to_sec()

            while self.x == None or  self.todo[0] not in self.x:
                print("Exploring, strt")
                self.vel.linear.x = 0.2
                t1 = rospy.Time.now().to_sec()
                d = 0.2 * (t1 - t)
                self.vel_pub.publish(self.vel)
                if d >= 1:
                    break
            self.zed(self.vel.linear.x)
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.vel_pub.publish(self.vel)
        print()

        self.detected()


if __name__ == "__main__":
    try:
        nav = nav()
        nav.explore()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node_terminated")
    