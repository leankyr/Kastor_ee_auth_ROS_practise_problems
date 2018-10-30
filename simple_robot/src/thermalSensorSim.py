#!/usr/bin/env python

import ipdb
import sys
import rospy
import random
from simple_robot_msgs.msg import TemperatureReading
#import simple_robot_msgs
def thermal_node_sim():
    rospy.init_node('thermal_node_sim')
    temperature_pub = rospy.Publisher('/sensors/temperature',TemperatureReading,queue_size=10)
    #rate of publishing
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        temp_msg = TemperatureReading()
        # generate random temperatures
        temp_msg.temperature = random.randrange(20,41)
        # publish them
        temperature_pub.publish(temp_msg)
        rate.sleep()




if __name__ == "__main__":
    try:
        thermal_node_sim()
    except rospy.ROSInterruptException:
        pass
