#!/usr/bin/env python

import sys
import rospy
import random
from tic_tac_toe.msg import table, moveMessage
import time

def show_table(table):
    print table[0],' ',table[1],' ',table[2]
    print table[3],' ',table[4],' ',table[5]
    print table[6],' ',table[7],' ',table[8]


def publish_move():
    pub_move = rospy.Publisher('/player1_moves',moveMessage,queue_size = 10)
    move = moveMessage()
    move.x = random.randrange(1,4)
    move.y = random.randrange(1,4)
    #move.x = int(raw_input('give x: '))
    #move.y = int(raw_input('give y: '))
    rospy.loginfo('move is :' + str(move.x) + ' ' + str(move.y))
    pub_move.publish(move)
    return 'move Published'


def table_callback(msg):
    rospy.loginfo('I am in table CallBack!!')
    show_table(msg.table)
    #show_table(msg.table)

def player1m():
    rospy.init_node('player1m')
    rate = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        sub_to_table = rospy.Subscriber('/table_topic',table,table_callback)
        rospy.loginfo(publish_move())
        rate.sleep()
    


if __name__ == "__main__":
    try:
        player1m()
    except rospy.ROSInterruptException:
        pass

