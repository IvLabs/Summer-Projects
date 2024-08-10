#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
#import math


def MoveCircle():
    global vel,pub,rate
    k=0
    vel.linear.x=k
    
    while not rospy.is_shutdown():
        vel.linear.x=k
        vel.angular.z=4
        pub.publish(vel)
        k+=0.5
        rate.sleep()
        #print(k)
    vel.linear.x=0
    vel.angular.z=0
    pub.publish(vel)



def main():
    global vel,pub,rate
    rospy.init_node("Spiral",anonymous=True)
    pub=rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size=10)
    print("PUblisher Established")
    rate=rospy.Rate(1)

    vel=Twist()
    MoveCircle()
    
if __name__=='__main__':
    main()