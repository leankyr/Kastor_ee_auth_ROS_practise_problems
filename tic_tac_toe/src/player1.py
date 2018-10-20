#!/usr/bin/env python

import sys
import rospy
from tic_tac_toe.srv import *


def show_table(table):
    print table[0],' ',table[1],' ',table[2]
    print table[3],' ',table[4],' ',table[5]
    print table[6],' ',table[7],' ',table[8]


def get_response(player,x,y):
    rospy.wait_for_service('move_implement')
    try:
        move_calc = rospy.ServiceProxy('move_implement', move)
        resp = move_calc(player,x,y)

        return resp.Message,resp.table
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        player = sys.argv[0]
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print usage()
        sys.exit(1)

    # Functions Implementing Stuff
    mes,table = get_response(player,x,y)
    print mes
    show_table(table)
