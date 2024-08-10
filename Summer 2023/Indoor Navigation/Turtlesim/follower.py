#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

target = None
turtle2_pos = None

def pose_1_callback(pos : Pose):
    global target
    target = pos

def pose_2_callback(pos : Pose):
    global turtle2_pos
    turtle2_pos = pos

def follow():
    global turtle2_pos
    global target

    rospy.init_node('turtle_controller')
    sub1 = rospy.Subscriber('/turtle1/pose', Pose, callback = pose_1_callback)
    sub2 = rospy.Subscriber('/turtle2/pose', Pose, callback = pose_2_callback)
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if turtle2_pos is not None and target is not None:

            distance = ((target.x - turtle2_pos.x) ** 2 + (target.y - turtle2_pos.y) ** 2) ** 0.5
            target_angle = math.atan2(target.y - turtle2_pos.y, target.x - turtle2_pos.x)
            angle_diff = target_angle - turtle2_pos.theta

            # To get smaller angle, otherwise always clockwise
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            cmd = Twist()
            cmd.linear.x = 0.5 * distance
            cmd.angular.z = 1.5 * angle_diff
            pub.publish(cmd)

        rate.sleep()

follow()