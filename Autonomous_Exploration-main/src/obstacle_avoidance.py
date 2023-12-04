#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

count1, count2 = 0,0

def scan_callback(data):
    global count1,count2
    sum_centre, sum_left, sum_right = 0,0,0
    # left region of turtlebot is defined in 41 to 180 indices
    for i in range(41,180) : 
        sum_left += data.ranges[i]
    # right region in 540 to 680 indices
    for j in range(540,680) :
        sum_right += data.ranges[j]
    # central region in 0-40 and 680-719 indices 
    for k in range(41):
        sum_centre += data.ranges[k]
    for l in range(680,719):
        sum_centre += data.ranges[l]
    
    #taking average values of ranges in each region
    forward_safe_distance = sum_centre/40
    left_safe_distance = sum_left/70
    right_safe_distance = sum_right/70

    #safe distance from obstacle is taken 0.9
    if forward_safe_distance > 0.9 and left_safe_distance > 0.9 and right_safe_distance > 0.9 :
        msg.linear.x = 0.15
        msg.angular.z = 0
        rate.sleep()
   
    elif forward_safe_distance < 0.9 and left_safe_distance > 0.9 and right_safe_distance > 0.9 :
        msg.linear.x = 0
        msg.angular.z = -0.5
        rate.sleep()
     
    else:
        #turn is taken after 5 counts, to avoid jerking
        if left_safe_distance > right_safe_distance :
            count1 += 1
            count2 = 0
            if count1 >= 5:
                msg.linear.x = 0
                msg.angular.z = -0.5
                rate.sleep()

                if forward_safe_distance > 0.9 and left_safe_distance > 0.9 and right_safe_distance > 0.9 :
                    count1 = 0
                    msg.linear.x = 0.15
                    msg.angular.z = 0
        elif left_safe_distance < right_safe_distance :
            count2 += 1
            count1 = 0
            if count2 >= 5:
                msg.linear.x = 0
                msg.angular.z = 0.5
                rate.sleep()
       
                if forward_safe_distance > 0.9 and left_safe_distance > 0.9 and right_safe_distance > 0.9 :
                    count2 = 0
                    msg.linear.x = 0.15
                    msg.angular.z = 0
    pub.publish(msg)

if __name__ == '__main__':
    msg = Twist()
    msg.linear.x = 0
    msg.linear.y = 0
    msg.linear.z = 0
    msg.angular.x = 0
    msg.angular.y = 0
    msg.angular.z = 0
    rospy.init_node('final_obstacle_avoidance')
    pub = rospy.Publisher("/cmd_vel_mux/input/navi", Twist, queue_size=20)
    sub = rospy.Subscriber("/scan", LaserScan, scan_callback)
    rate = rospy.Rate(30)
    rospy.spin()