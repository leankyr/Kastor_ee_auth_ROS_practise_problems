#!/usr/bin/env python

import sys
import rospy
from tic_tac_toe.msg import table
from tic_tac_toe.srv import move
#from std_msgs.msg import String


if __name__ == "__main__":
    tic_tac_toe_server()

