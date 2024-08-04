#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    rospy.init_node('turtle_controller')
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
    
    radius = int(input("Enter radius of circle: "))

    while not rospy.is_shutdown():
        cmd = Twist()
        for i in range(3):
            cmd.linear.x = radius
            cmd.angular.z = math.pi
            pub.publish(cmd)
            rospy.sleep(0.5)
        break