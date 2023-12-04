#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import math

def sq_spiral(side):
    global vel,pub,rate
    rospy.init_node('sq_spiral',anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    rate = rospy.Rate(100)
    vel = Twist()
    rotations = 0
    r = 0
    while rotations < 9: #to stop after 9 side lengths
        sq_spiral_side(side)
        rotations += 1
        r += 1
        if r == 2: # after tracing every two side lenghts increase side length by 0.5
            side += 0.5
            r = 0


def sq_spiral_side(side): #tracing the sides
    t0 = rospy.Time.now().to_sec() #start time
    dist = 0
    linear_speed = 0.7
    vel.linear.x = linear_speed

    while True:
        rospy.loginfo("Turtle moves forward")
        pub.publish(vel)
        rate.sleep()
        t1 = rospy.Time.now().to_sec() #current time
        dist = linear_speed * (t1-t0) #basically distance = speed x time :)
        if dist >= side:
            break
    
    vel.linear.x = 0
    pub.publish(vel)

    turn()

def turn(): #taking a turn after every side
    angular_speed = 0.5
    vel.angular.z = angular_speed
    t0 = rospy.Time.now().to_sec()
    angle = 0
    while True:
        rospy.loginfo("Turtle rotates")
        if angle > (math.pi/2): #90 degree turn
            break
        pub.publish(vel)
        t1 = rospy.Time.now().to_sec()
        angle = (t1-t0) * angular_speed
        rate.sleep()

    vel.angular.z = 0
    pub.publish(vel)

if __name__ == '__main__':
    try:
        sq_spiral(float(sys.argv[1])) #input the initial side length as an argument
    except rospy.ROSInterruptException:
        pass