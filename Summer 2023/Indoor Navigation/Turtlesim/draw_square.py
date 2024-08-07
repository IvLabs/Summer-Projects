#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

turtle_pos = None

def pose_callback(pos : Pose):
    global turtle_pos
    turtle_pos = pos

def move_to_target(target):
    global turtle_pos

    rospy.init_node('turtle_controller')
    sub = rospy.Subscriber('/turtle1/pose', Pose, callback = pose_callback)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if turtle_pos is not None:

            distance = ((target[0] - turtle_pos.x) ** 2 + (target[1] - turtle_pos.y) ** 2) ** 0.5
            target_angle = math.atan2(target[1] - turtle_pos.y, target[0] - turtle_pos.x)
            angle_diff = target_angle - turtle_pos.theta

            # To get smaller angle, otherwise always clockwise
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            elif angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            cmd = Twist()
            cmd.angular.z = 1.5 * angle_diff
            pub.publish(cmd)

            if angle_diff < 0.0005:
                cmd.linear.x = 0.5 * distance
                pub.publish(cmd)

            if distance < 0.005:
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                pub.publish(cmd)
                break

        rate.sleep()

if __name__ == '__main__':
    a = int(input("Enter length of side of square: "))
    move_to_target([5.544445 + a, 5.544445])
    move_to_target([5.544445 + a, 5.544445 + a])
    move_to_target([5.544445, 5.544445 + a])
    move_to_target([5.544445, 5.544445])