#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

def posecallback1(msg1):
    global pose
    pose = msg1
    x = round(pose.x,4)
    y = round(pose.y,4)

rospy.init_node("gotogoal", anonymous=True)
pub = rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
pose_sub = rospy.Subscriber("/turtle1/pose",Pose,posecallback1)
rate = rospy.Rate(30)
pose = Pose()

goal_pose = Pose()
goal_pose.x = float(input("Enter goal x - ")) #input the goal co-ordinates
goal_pose.y = float(input("Enter goal y - "))

vel = Twist()
distance = math.sqrt((goal_pose.x - pose.x) ** 2 + (goal_pose.y - pose.y) ** 2) #linear error
angle = math.atan2(goal_pose.y - pose.y, goal_pose.x - pose.x) #angular error
lin_vel = 1.5 * distance
ang_vel = 6 * (angle - pose.theta)
vel.linear.x = lin_vel
vel.angular.z = ang_vel
pub.publish(vel)

while distance >= 0.1: #tolerance value is taken as 0.1
    distance = math.sqrt((goal_pose.x - pose.x) ** 2 + (goal_pose.y - pose.y) ** 2)
    angle = math.atan2(goal_pose.y - pose.y, goal_pose.x - pose.x)
    lin_vel = 1.5 * distance
    ang_vel = 6 * (angle - pose.theta)
    vel.linear.x = lin_vel
    vel.angular.z = ang_vel        
    pub.publish(vel)
    rate.sleep()
vel.linear.x = 0
vel.angular.z = 0        
pub.publish(vel)
rospy.spin()