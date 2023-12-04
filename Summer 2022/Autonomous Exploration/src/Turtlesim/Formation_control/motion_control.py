#!/usr/bin/env python3

import turtlesim.srv
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def posecallback(msg):
    global pose
    pose = msg

rospy.init_node("motion_control")
rospy.wait_for_service("kill")
kill = rospy.ServiceProxy("kill", turtlesim.srv.Kill)
kill("turtle1")
rospy.wait_for_service("spawn")
spawner = rospy.ServiceProxy("spawn", turtlesim.srv.Spawn)
spawner(4.5,4.5,0,"turtle1")
pub = rospy.Publisher("/turtle1/cmd_vel", Twist , queue_size=10)
pose_sub = rospy.Subscriber("turtle1/pose", Pose, posecallback)

#This turtle is being controlled by teleop
