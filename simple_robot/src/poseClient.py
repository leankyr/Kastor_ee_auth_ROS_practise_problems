#!/usr/bin/env python

import sys
import rospy
import random
import actionlib

# import all the msgs to use the action
from simple_robot_msgs.msg import GetRobotPoseGoal, GetRobotPoseAction,GetRobotPoseResult,VictimFound



def callback(msg):
    result = robotPoseClient()
    rospy.loginfo('Victim Found! Robot Pose = (<%d> <%d>),Sensor used for identification: %s', result.x, result.y, msg.sensor)

def robotPoseClient():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('/slam/get_robot_pose', GetRobotPoseAction )

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()
    goal = GetRobotPoseGoal()
    
    client.send_goal(goal)
    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A FibonacciResult




if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('pose_client')
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            sub_to_vitim_found = rospy.Subscriber('data_fusion/victim_found',VictimFound,callback)
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
        # print("program interrupted before completion", file=sys.stderr)

