#!/usr/bin/env python3
from typing import List
import rospy
from rospy.core import is_shutdown
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
from math import inf 
import time

class Wall():
    def __init__(self):
        rospy.init_node('follow',anonymous=True)
        self.msg = LaserScan()
        self.i = None
        self.l = []
        self.m = None
        self.check = []
        self.c = 0
        self.j = 0
        self.k = 1
        self.h = []
        self.g = 0
        self.sub = rospy.Subscriber('/laser/scan',LaserScan,self.update,queue_size = 5)
        self.j1 = rospy.Publisher('joint1_vel_controller/command',Float64,queue_size=10)
        self.j2 = rospy.Publisher('joint2_vel_controller/command',Float64,queue_size=10)
        self.j3 = rospy.Publisher('joint3_vel_controller/command',Float64,queue_size=10)
        self.j4 = rospy.Publisher('joint4_vel_controller/command',Float64,queue_size=10)
    def update(self,data):
        self.j = self.j + 1
        self.msg = data
        self.l = self.msg.ranges
        self.m = min(self.l)
        self.i = self.l.index(self.m)
        self.check = self.l[self.i-5:self.i+5]
        self.zone = self.l[171:180]
        self.a = min(self.zone)
        self.h = self.l[0:180]
        self.g = min(self.h)
        time.sleep(1)  

    def expr(self):
        time.sleep(1)
        while self.j == 1 or self.j== 0:
            self.c = self.m
        if self.c - 0.4 <= self.m <= self.c + 0.7:
            v = 5
            w = -5
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(v)
            self.j4.publish(w)
        elif self.a > self.c + 0.7 and self.l[97] == inf :
            t1 = time.time() + 31.5
            while time.time() < t1:
                v = -10
                w = -10
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w)
            t2 = time.time() + (2*self.c + 1.1)/0.097
            while time.time() < t2:
                v = 5
                w = -5
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w)
            t3 = time.time() + 27.5
            if time.time() < t3:
                v = -10
                w = -10
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w)
            else:
                v = 5
                w = -5
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w)
        elif self.g < self.c - 0.6:
            t4 = time.time() + 1.1/0.097
            while time.time() < t4:
                v = -5
                w = 5
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w)
            t5 = time.time() + 6
            while time.time() < t5:
                v = 10
                w = 10
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w)
            else:
                v = 5
                w = -5
                self.j1.publish(v)
                self.j2.publish(w)
                self.j3.publish(v)
                self.j4.publish(w) 
        else:
            v = 10
            w = -10
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(v)
            self.j4.publish(w)  
if __name__ == '__main__':
    try:
        a = Wall()
        while not rospy.is_shutdown():
            a.expr()
            time.sleep(1)
    except rospy.ROSInterruptException:
        pass

