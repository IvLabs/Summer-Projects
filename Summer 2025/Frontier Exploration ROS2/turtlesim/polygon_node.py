#!usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from geometry_msgs.msg import Twist

class polygonTrajectoryNode (Node):

    def __init__ (self):

        super().__init__("polygon_node")
        self.sides = float(input("Enter number of sides of polygon: "))
        self.get_logger().info("Polygon Trajectory has started")
        self.angle_rotate = ((2.0)*math.pi)/self.sides
        self.cmd_vel_pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.create_timer(1.0,self.goForward)
        self.create_timer(2.0,self.rotate_cw)

    def goForward (self):

        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 0.0
        self.cmd_vel_pub.publish(msg)
        
    def rotate_cw (self):

        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = self.angle_rotate
        self.cmd_vel_pub.publish(msg)


def main (args = None):
    rclpy.init(args=args)
    node = polygonTrajectoryNode()
    rclpy.spin(node)
    rclpy.shutdown()