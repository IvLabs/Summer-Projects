#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

rospy.init_node("teleop",anonymous=True)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
vel = Twist()
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    key = input()
    if key == "w":
        vel.linear.x = 0.5
        vel.angular.z = 0
        pub.publish(vel)
    if key == "a":
        vel.linear.x = 0.1
        vel.angular.z = -0.2
        pub.publish(vel)
    if key == "s":
        vel.linear.x = 0
        vel.angular.z = 0
        pub.publish(vel)
    if key == "d":
        vel.angular.z = 0.2
        vel.linear.x = 0.1
        pub.publish(vel)
    if key == "x":
        vel.angular.z = 0   
        vel.linear.x = -0.5
        pub.publish(vel)

    pub.publish(vel)
    rate.sleep()
    rospy.spin()

