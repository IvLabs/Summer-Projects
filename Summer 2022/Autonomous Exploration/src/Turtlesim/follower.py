#!/usr/bin/env python3

import rospy
import turtlesim.srv
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

def posecallback1(msg1):
    global pose1
    pose1 = msg1
    x1 = round(pose1.x,4)
    y1 = round(pose1.y,4)
    theta1 = pose1.theta

def posecallback2(msg2):
    global pose2
    pose2 = msg2
    x2 = round(pose2.x,4)
    y2 = round(pose2.y,4)
    theta2 = pose2.theta

rospy.init_node("follower", anonymous=True)
pub1 = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
pose_sub = rospy.Subscriber("/turtle1/pose",Pose,posecallback1)
rospy.wait_for_service("spawn")
spawner = rospy.ServiceProxy("spawn", turtlesim.srv.Spawn)
spawner(8,2,0,"turtle2") #spawning turtle2
pub2 = rospy.Publisher("/turtle2/cmd_vel", Twist, queue_size=10)
pose_sub2 = rospy.Subscriber("/turtle2/pose",Pose,posecallback2)
rate = rospy.Rate(30)
pose1 = Pose()
pose2 = Pose()
pose2.x = 8 #defining initial co-ordinates of the turtle2
pose2.y = 2

vel = Twist()
distance = math.sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2) #linear error
angle = math.atan2(pose1.y - pose2.y, pose1.x - pose2.x) #angular error
lin_vel = 1.5 * distance
ang_vel = 6 * (angle - pose2.theta)
vel.linear.x = lin_vel
vel.angular.z = ang_vel
pub2.publish(vel)
while not rospy.is_shutdown():
    while distance > 0.1: #distance of 0.1 between the two turtles
        distance = math.sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2)
        angle = math.atan2(pose1.y - pose2.y, pose1.x - pose2.x)
        lin_vel = 1.5 * distance
        ang_vel = 6 * (angle - pose2.theta)
        vel.linear.x = lin_vel
        vel.angular.z = ang_vel        
        pub2.publish(vel)
        rate.sleep()
    vel.linear.x = 0
    vel.angular.z = 0        
    pub2.publish(vel)
    distance = math.sqrt((pose1.x - pose2.x) ** 2 + (pose1.y - pose2.y) ** 2)
    angle = math.atan2(pose1.y - pose2.y, pose1.x - pose2.x)
rospy.spin()


