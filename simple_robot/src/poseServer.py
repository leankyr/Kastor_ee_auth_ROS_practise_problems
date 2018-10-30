#!/usr/bin/env python

import sys
import rospy
import random
import actionlib

# import all the msgs to use the action
from simple_robot_msgs.msg import GetRobotPoseAction,GetRobotPoseResult


class poseServer(object):
    # messages that are used to publish feedback result
    # These are the class variables
    result = GetRobotPoseResult()

#### Below is the constructor of the class ####

    def __init__(self):
        self._action_name = '/slam/get_robot_pose' # I could possibly give the name through a yaml file
        # Above I set name of topic
        self._as = actionlib.SimpleActionServer(self._action_name, GetRobotPoseAction, execute_cb=self.posePublisherCallback, auto_start = False)   # as stands for action server
        self._as.start()

    def posePublisherCallback(self,goal):
        # helper variables
        rospy.loginfo('Got in Callback!!')
        r = rospy.Rate(1)
        self.result.x = random.randrange(0,10)
        self.result.y = random.randrange(0,10)

        self._as.set_succeeded(self.result)






if __name__ == "__main__":
    try:
        rospy.init_node('robot_pose_server')
        # server must have the same name as the class
        server = poseServer()
        # rospy.get_name() passes the name of the node to the class
        rospy.loginfo(rospy.get_name())
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
