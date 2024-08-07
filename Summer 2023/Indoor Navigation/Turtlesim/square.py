#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math
SPEED=1

def move_straight(side):
    global vel,pub,rate
    vel.linear.x=SPEED
    
    dist_travel=0
    t0=rospy.Time.now().to_sec()
    while dist_travel<side:
        pub.publish(vel)
        t1=rospy.Time.now().to_sec()
        dist_travel=SPEED*(t1-t0)
        rate.sleep()
    vel.linear.x = 0
    pub.publish(vel)

def rotate90():
    vel.angular.z=2
    angle_travel=0
    t0=rospy.Time.now().to_sec()
    while angle_travel<((math.pi/2)):
        pub.publish(vel)
        t1=rospy.Time.now().to_sec()
        angle_travel=2*(t1-t0)
        rate.sleep()
    vel.angular.z = 0
    pub.publish(vel)



def main():
    global vel,pub,rate
    rospy.init_node("square",anonymous=True)
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
    print("PUblisher Established")
    #rospy.init_node("square",anonymous=True)
    rate=rospy.Rate(200)

    vel=Twist()
    side=2

    rotations=0
    while rotations<4:
        move_straight(side)
        rotate90()
        rotations+=1

if __name__=='__main__':
    main()