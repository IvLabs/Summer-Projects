#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

dist = 0.7
def callback(msg):
    if msg.ranges[0] > dist and msg.ranges[30] > dist and msg.ranges[330] > dist: #checking at 0, 30, 330 degrees
        vel.linear.x = 0.4
        vel.angular.z = 0
    else :
        vel.linear.x = 0
        vel.angular.z = 0.5
        if msg.ranges[0] > dist and msg.ranges[30] > dist and msg.ranges[330] > dist:
            vel.linear.x = 0.4
            vel.angular.z = 0 
    pub.publish(vel)

rospy.init_node("obs",anonymous=True)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
vel = Twist()
sub = rospy.Subscriber("/scan", LaserScan, callback)
rospy.spin()