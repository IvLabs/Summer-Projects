#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CircularTrajectoryNode(Node):

    def __init__ (self):
        super().__init__("circle_node")
        self.cmd_vel_pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.create_timer(0.5,self.timer_callback)
        self.get_logger().info("Circular Trajectory has Commenced.")

    def timer_callback (self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.cmd_vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CircularTrajectoryNode()
    rclpy.spin(node)
    rclpy.shutdown()