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
        rospy.init_node('wall',anonymous = True)
        self.msg = LaserScan()
        self.a = 0
        self.b = 0
        self.c = 0
        self.i = 0
        self.j = 0
        self.m = 0
        self.n = 0
        self.t = 0
        self.s = 0
        self.v = 0
        self.e = 0
        self.l = []
        self.l1 = []
        self.l2 = []
        self.l3 = []
        self.sub = rospy.Subscriber('/laser/scan',LaserScan,self.update,queue_size = 5)
        self.j1 = rospy.Publisher('joint1_vel_controller/command',Float64,queue_size=10)
        self.j2 = rospy.Publisher('joint2_vel_controller/command',Float64,queue_size=10)
        self.j3 = rospy.Publisher('joint3_vel_controller/command',Float64,queue_size=10)
        self.j4 = rospy.Publisher('joint4_vel_controller/command',Float64,queue_size=10)
    def update(self,data):
        self.msg = data
        self.j = self.j + 1
        self.l = self.msg.ranges
        self.g = min(self.l[0:10])
        self.h = min(self.l[81:90])
        self.s = min(self.l[0:90])
        self.v = min(self.l[36:72])
        self.l1 = self.l[0:38]
        self.l2 = self.l[75:105]
        self.l3 = self.l[145:180]
        self.a = min(self.l1)
        self.b = min(self.l2)
        self.c = min(self.l3)
        self.e = min(self.l[81:99])

    def expr(self):
        while self.j == 1 or self.j== 0:
            self.m = self.a
            self.n = self.c
            self.t = self.s + 0.5
        if self.e < 1.411:
            v = -4000
            w = -4000
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(v)
            self.j4.publish(w)
        elif self.t - 0.3 <= self.v <= self.t + 0.3 and self.b > 1.411:
            v = 9000
            w = -9000
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(v)
            self.j4.publish(w)
        elif self.v > self.t + 0.5 and self.b > 1.411:
            v = 4000
            w = 4000
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(v)
            self.j4.publish(w)
        elif self.v < self.t - 0.5 and self.b < 1.411:
            v = -4000
            w = -4000
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(w)
            self.j4.publish(v)
        else:
            v = 9000
            w = -9000
            self.j1.publish(v)
            self.j2.publish(w)
            self.j3.publish(v)
            self.j4.publish(w)
if __name__ == '__main__':
    try:
        a = Wall()
        while not rospy.is_shutdown():
            a.expr()
            rospy.sleep(0.5)
    except rospy.ROSInterruptException:
        pass


