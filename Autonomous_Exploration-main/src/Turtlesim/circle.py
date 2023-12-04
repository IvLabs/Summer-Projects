#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys

def circle(lin_vel,ang_vel):
    rospy.init_node('circle',anonymous=True) # Inititalizing a node
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10) #Publishing on topic /cmd_vel
    rate = rospy.Rate(10) 
    vel = Twist()

    while True:
        vel.linear.x = lin_vel
        vel.linear.y = 0.0
        vel.linear.z = 0.0

        vel.angular.x = 0.0
        vel.angular.y = 0.0 
        vel.angular.z = ang_vel
        rospy.loginfo("Radius = {}".format(lin_vel//ang_vel))

        pub.publish(vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        circle(float(sys.argv[1]),float(sys.argv[2])) #Enter the lin_vel and ang_vel while running the code
    except rospy.ROSInternalException:
        pass

