#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16

import dynamic_reconfigure.client
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "the square is: %d ", data.data**2)
    
def manipulator():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('manipulator', anonymous=True)

    rospy.Subscriber("/task1/numbers", Int16, callback) ## Here I put the topic

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    manipulator()







