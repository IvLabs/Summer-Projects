#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class turtleFollowerNode (Node):

    # TURTLE1 -> MOVES
    # TURTLE2 -> FOLLOWES

    def __init__ (self):

        super().__init__("turtle_follower")
        self.cmd_vel_pub_turtle2 = self.create_publisher (Twist, "/turtle2/cmd_vel", 10)
        self.pose_sub_turtle1 = self.create_subscription (Pose, "/turtle1/pose", self.pose_callback_turtle1, 10)
        self.pose_sub_turtle2 = self.create_subscription (Pose, "/turtle2/pose", self.pose_callback_turtle2, 10)

        # CURRENT PARAMETERS:

        self.turtle1_x = None
        self.turtle1_y = None

        # GOAL PARAMETERS:

        self.turtle2_x = None
        self.turtle2_y = None
        self.turtle2_theta = None 

        self.create_timer (0.5, self.turtleFollower)

    def pose_callback_turtle1 (self, msg: Pose):

        self.turtle1_x = msg.x
        self.turtle1_y = msg.y

    def pose_callback_turtle2 (self, msg: Pose):

        self.turtle2_x = msg.x
        self.turtle2_y = msg.y
        self.turtle2_theta = msg.theta

    def normalize_angle (self, angle):

        while (angle > math.pi):
            angle -= 2*math.pi

        while (angle < -math.pi):
            angle+= 2*math.pi

        return angle

    def turtleFollower (self):

        if (self.turtle1_x == None or self.turtle1_y == None or self.turtle2_x == None or self.turtle2_y == None or self.turtle2_theta == None):
            return

        msg = Twist()

        self.del_x = self.turtle1_x - self.turtle2_x
        self.del_y = self.turtle1_y - self.turtle2_y
        self.target_theta = self.normalize_angle(math.atan2(self.del_y, self.del_x))

        self.distance_error = math.sqrt((self.del_x**2) + (self.del_y**2))
        self.angle_error = self.target_theta - self.turtle2_theta

        # USING P CONTROLLER: 

        if (abs(self.angle_error) > 0.1):

            msg.linear.x = 0.0
            msg.angular.z = min (1.5 * self.angle_error, 1.0)

        elif (self.distance_error > 0.1):

            msg.linear.x = min (1.5 * self.distance_error, 2.0)
            msg.angular.z = 0.0

        else:

            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.cmd_vel_pub_turtle2.publish(msg)



def main (args = None):

    rclpy.init(args = args)

    node = turtleFollowerNode()
    rclpy.spin(node)

    rclpy.shutdown()