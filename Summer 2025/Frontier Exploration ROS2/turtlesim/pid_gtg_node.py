#!/usr/bin/env python3
import rclpy
from rclpy.node import Node #rclpy library ke node module se Node class import kar liya
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class PID_GTG_Node (Node):

    def __init__ (self):

        super().__init__("pid_gtg_node")

        self.goal_x = float(input("Enter X Coordinate of Goal: "))
        self.goal_y = float(input("Enter Y Coordinate of Goal: "))

        self.cmd_vel_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.pose_sub = self.create_subscription (Pose, "/turtle1/pose", self.pose_callback, 10)

        self.current_x = None
        self.current_y = None
        self.current_theta = None

        self.prev_dist_error = 0.0
        self.prev_angle_error = 0.0

        self.dist_integral = 0.0
        self.angle_integral = 0.0

        self.create_timer (0.5, self.goToGoalPID)

    def pose_callback (self, msg: Pose):

        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

        # PID:
        # P = Kp * error                    DEALS WITH CURRENT ERROR
        # I = Ki * integral(error * dt)     DEALS WITH ACCUMULATED PAST ERRORS
        # D = Kd * (d(error) / dt)          DEALS WITH RATE OF CHANGE IN ERRORS

    def goToGoalPID (self):

        if (self.current_x == None or self.current_y == None or self.current_theta == None):
            return

        msg = Twist()

        dt = 0.5
        _Kp = 1.0
        _Ki = 0.002
        _Kd = 0.2

        self.del_x = self.goal_x - self.current_x
        self.del_y = self.goal_y - self.current_y
        self.target_theta = self.normalize_angle(math.atan2(self.del_y, self.del_x))

        # DISTANCE PID

        self.current_dist_error = math.sqrt((self.del_x**2) + (self.del_y**2))
        self.dist_integral += self.current_dist_error*dt

        self.dist_prop_error = _Kp * self.current_dist_error
        self.dist_integral_error = _Ki * self.dist_integral 
        self.dist_derivative_error = _Kd * ((self.current_dist_error - self.prev_dist_error)/dt)

        self.corrected_lin_vel = self.dist_prop_error + self.dist_integral_error + self.dist_derivative_error
        #msg.linear.x = self.corrected_lin_vel

        self.prev_dist_error = self.current_dist_error

        # ANGLE PID

        self.current_angle_error = self.target_theta - self.current_theta
        self.angle_integral += self.current_angle_error * dt
        
        self.angle_prop_error = _Kp * self.current_angle_error
        self.angle_integral_error = _Ki * self.angle_integral
        self.angle_derivative_error = _Kd * ((self.current_angle_error - self.prev_angle_error)/dt)

        self.corrected_ang_vel = self.angle_prop_error + self.angle_derivative_error + self.angle_integral_error
        #msg.angular.z = self.corrected_ang_vel

        self.prev_angle_error = self.current_angle_error

        # if (self.current_dist_error < 0.1):
        #     msg.linear.x = 0.0
        #     msg.angular.z = 0.0

        if (abs(self.current_angle_error) > 0.05):
            msg.linear.x = 0.0
            msg.angular.z = min (self.corrected_ang_vel, 1.0)

        elif (self.current_dist_error > 0.05):
           msg.linear.x = min (self.corrected_lin_vel, 2.0)
           msg.angular.z = 0.0 

        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.cmd_vel_pub.publish(msg)


    def normalize_angle (self, angle):

        while (angle > math.pi):
            angle -= 2*(math.pi)

        while (angle < -math.pi):
            angle += 2*(math.pi)

        return angle


def main (args = None):

    rclpy.init(args = args)

    node = PID_GTG_Node()
    rclpy.spin(node)

    rclpy.shutdown()