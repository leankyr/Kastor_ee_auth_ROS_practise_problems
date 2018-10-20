#!/usr/bin/env python
# license removed for brevity
import rospy
import random
from std_msgs.msg import Int16

def streamer():
    pub = rospy.Publisher('/task1/numbers', Int16, queue_size=10)
    rospy.init_node('streamer', anonymous=True)
    rate = rospy.Rate(rospy.get_param("freq")) # 10hz
    while not rospy.is_shutdown():
	number = random.randint(1,101)
        hello_str = "the number is:" + str(number)

        rospy.loginfo(hello_str)
        pub.publish(number)
        rate.sleep()

if __name__ == '__main__':
    try:
        streamer()
    except rospy.ROSInterruptException:
        pass























