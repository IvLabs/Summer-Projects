#!/usr/bin/env python


import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class Turtled:
    def __init__(self):
        rospy.init_node("GoTogoal1", anonymous=True)
        self.pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        self.rate = rospy.Rate(10)
        self.vel = Twist()
        print("Publisher Established")
        self.sub = rospy.Subscriber("/turtle1/pose", Pose, self.poseCallback)
        self.Pose = Pose()

    def poseCallback(self, pose):
        self.Pose.x = round(pose.x,4)
        self.Pose.y = round(pose.y,4)
        self.Pose.theta = round(pose.theta,4)
        # print("Callback>>", self.Pose.x, self.Pose.y)

    def dist(self, x2, y2):
        return math.sqrt(pow((x2 - self.Pose.x), 2) + pow((y2 - self.Pose.y), 2))

    def goToGoal(self, pt, dist_tol):
        print("Going to Goal")
        x2, y2 = pt

        while self.dist(x2, y2) > dist_tol:
            self.vel.linear.x = .5 * self.dist(x2, y2)
            self.vel.angular.z = 4 *(
                math.atan2((y2 - self.Pose.y), (x2 - self.Pose.x)) - self.Pose.theta
            )
            self.pub.publish(self.vel)
            self.rate.sleep()

        self.vel.linear.x = 0
        self.vel.angular.z = 0
        print("Goal Reached")
        self.pub.publish(self.vel)
        rospy.spin()


if __name__ == "__main__":
    tsim = Turtled()
    tsim.goToGoal((1,7), .5)
