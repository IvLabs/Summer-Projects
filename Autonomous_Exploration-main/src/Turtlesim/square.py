#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import math

def square(side):
    global vel,pub,rate
    rospy.init_node('square',anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rate = rospy.Rate(100)
    vel = Twist()
    rotations = 0

    while rotations < 4: #as a square has 4 sides
        square_side(side)
        rotations += 1


def square_side(side): #tracing the sides
    t0 = rospy.Time.now().to_sec()
    dist = 0
    linear_speed = 1
    vel.linear.x = linear_speed

    while True:
        rospy.loginfo("Turtle moves forward")

        pub.publish(vel)
        rate.sleep()
        t1 = rospy.Time.now().to_sec()
        dist = linear_speed * (t1-t0)
        if dist >= side:
            break
    
    vel.linear.x = 0
    pub.publish(vel)
    
    turn()

def turn(): #taking 90 degree turn
    angular_speed = 0.5
    vel.angular.z = angular_speed
    t0 = rospy.Time.now().to_sec()
    angle = 0
    while True:
        rospy.loginfo("Turtle rotates")
        if angle > (math.pi/2):
            break
        pub.publish(vel)
        t1 = rospy.Time.now().to_sec()
        angle = (t1-t0) * angular_speed
        rate.sleep()

    vel.angular.z = 0
    pub.publish(vel)

if __name__ == '__main__':
    try:
        square(float(sys.argv[1])) #input the side length as an argument
    except rospy.ROSInterruptException:
        pass
