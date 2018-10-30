#!/usr/bin/env python 

import ipdb
import sys
import rospy
import random
from simple_robot_msgs.msg import TemperatureReading,VictimFound


def tempCallback(msg,args):
    victim_found_pub = args
    # I set the threshold to 37
    threshold = 37
    # check if temperature recorded from the sensor is greater than the set thrreshold
    if msg.temperature >= threshold:
        string_msg = VictimFound()
        string_msg.sensor = 'VICTIM FOUND by thermal sensor!'
        victim_found_pub.publish(string_msg)



def fusionNode():
    rospy.init_node('fusion_node')
    # topic to post if a victim is found by some sensor
    victim_found_pub = rospy.Publisher('/data_fusion/victim_found',VictimFound,queue_size=10)
    rate = rospy.Rate(1)
    
    while not rospy.is_shutdown():
        # subscribe to the thermal sensor
        Sub_to_sensor = rospy.Subscriber('/sensors/temperature',TemperatureReading,tempCallback,(victim_found_pub))
        rate.sleep()


    return




if __name__ == "__main__":
    try:
        fusionNode()
    except rospy.ROSInterruptException:
        pass
