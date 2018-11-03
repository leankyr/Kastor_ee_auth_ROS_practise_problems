#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist,Pose2D,Point
from sensor_msgs.msg import LaserScan,Range
from math import cos,sin
import tf
from visualization_msgs.msg import Marker
def usage():
    return "%s [x y]"%sys.argv[0]


def publish_markers(marker_pub,pose_x,pose_y,rot_z,rot_w):
    msg = Marker()
    msg.header.frame_id = "base_footprint"
    msg.header.stamp = rospy.Time(0)
    msg.ns = "lines"
    msg.action = msg.ADD
    msg.type = msg.CUBE
    msg.id = 0
    #msg.scale.x = 1.0
    #msg.scale.y = 1.0
    #msg.scale.z = 1.0
    # I guess I have to take into consideration resolution too
    msg.pose.position.x = pose_x*0.05;
    msg.pose.position.y = pose_y*0.05;
    msg.pose.position.z = 0;
    msg.pose.orientation.x = 0.0;
    msg.pose.orientation.y = 0.0;
    msg.pose.orientation.z = rot_z*0.05;
    msg.pose.orientation.w = rot_w*0.05;
    msg.scale.x = 0.1;
    msg.scale.y = 0.1;
    msg.scale.z = 0.1;
    msg.color.a = 1.0; # Don't forget to set the alpha!
    msg.color.r = 0.0;
    msg.color.g = 1.0;
    msg.color.b = 0.0;

    marker_pub.publish(msg)
    return

def obstacle_avoid(msg,args):
    scan_ = msg
    pub = args[0]
    rate = args[1]
    marker_pub = args[2]
    try:
    # Always put transform listener in try except block

        (trans,rot) = listener.lookupTransform('base_footprint', 'map', rospy.Time(0))

        ##!!! WEIRD BUG HAVE TO PUT MINUS IN FRONT OF POSE_X !!!!###
        ## maybe I got the vice Versa transform lul ## 
        publish_markers(marker_pub,-trans[0],-trans[1],rot[2],rot[3])
        # print (-trans[0])
        # print (-trans[1])

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        pass

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




    #sub = rospy.Subscriber(pose_topic_, Pose2D ,print_pose)
    marker_pub = rospy.Publisher('Marker_pub_topic',Marker,queue_size = 10)
    pub = rospy.Publisher(speeds_topic_ , Twist , queue_size = 10)
    rospy.init_node('obst_avoid',anonymous=True)
    rate = rospy.Rate(10)
    listener = tf.TransformListener()
    while not rospy.is_shutdown():
        rospy.Subscriber(laser_topic_ , LaserScan , obstacle_avoid ,(pub,rate,marker_pub))
        rospy.spin()

#    obstacle_avoid()

