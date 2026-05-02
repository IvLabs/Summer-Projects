#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SpiralTrajectoryNode (Node):

    def __init__ (self):
        super().__init__("spiral_node")
        self.get_logger().info("Spiral Trajectory has Commenced.")
        self.cmdVelPublisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.timer_for_circle = self.create_timer (0.5,self.circularTrack)
        self.starting_vel = 1.0

    def circularTrack (self):
        msg2 = Twist()
        msg2.linear.x = self.starting_vel
        msg2.angular.z = 1.0
        self.starting_vel += 0.05

        self.cmdVelPublisher.publish(msg2)


def main (args=None):
    rclpy.init(args=args)
    node = SpiralTrajectoryNode()
    rclpy.spin(node)
    rclpy.shutdown()