#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist,Pose2D,Point
from sensor_msgs.msg import LaserScan,Range
from math import cos,sin

def usage():
    return "%s [x y]"%sys.argv[0]

def obstacle_avoid(msg,args):
    scan_ = msg
    pub = args[0]
    rate = args[1]

    linear = 0
    angular = 0

    for i in range(0,len(scan_.ranges)):
        real_dist = scan_.ranges[i]
        linear -= cos(scan_.angle_min + i * scan_.angle_increment)/(1.0 + real_dist * real_dist)
        angular -= sin(scan_.angle_min + i * scan_.angle_increment)/(1.0 + real_dist * real_dist)

    # Twist cmd
    # print "I got out of for loop!! "
    linear /= len(scan_.ranges)
    angular /= len(scan_.ranges)

   # print ("linear vel is: " + str(linear))
   # print ("angular vel is: " + str(angular))   


    if (linear > 0.2):  # all these are 0.2 at stable vesrion
        linear = 0.2
    elif(linear < -0.2):
        linear = -0.2

    msg = Twist()
    msg.linear.x =  0.1 + linear

    #msg.linear.y =  0.1 + linear
    msg.angular.z = angular
    pub.publish(msg)

def print_pose(msg):
    pose_ = msg 

    print("I am in print pose Fun")
    print("x is:",pose_.x)
    print("y is:",pose_.y)
    print("theta is:",pose_.theta)
    return

if __name__ == "__main__":
#    if len(sys.argv) == 3:
    laser_topic_ = "/robot0/laser_0"
    speeds_topic_ = "/robot0/cmd_vel"
    pose_topic_ = "/initial_pose"
#    laser_topic_ = "/robot1/scan"
 #   speeds_topic_ = "/robot1/mobile_base/commands/velocity"


    print "laser topic is: %s"%(laser_topic_)  ## Two ways to do the same thing! 
    print("speed topic is: " + speeds_topic_)
 #   else:
 #       print usage()
 #       sys.exit(1) 

    sub = rospy.Subscriber(pose_topic_, Pose2D ,print_pose)
    pub = rospy.Publisher(speeds_topic_ , Twist , queue_size = 10)
    rospy.init_node('obst_avoid',anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber(laser_topic_ , LaserScan , obstacle_avoid ,(pub,rate) )
    rospy.spin()

#    obstacle_avoid()

