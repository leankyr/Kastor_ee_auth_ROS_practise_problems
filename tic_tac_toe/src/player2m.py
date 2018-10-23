#!/usr/bin/env python

import sys
import rospy
import random
from tic_tac_toe.msg import table, moveMessage
import time
from std_msgs.msg import String


def show_table(table):
    print table[0],' ',table[1],' ',table[2]
    print table[3],' ',table[4],' ',table[5]
    print table[6],' ',table[7],' ',table[8]
    print







def publish_move():
    pub_move = rospy.Publisher('/player2_moves',moveMessage,queue_size = 10)
    move = moveMessage()
    move.x = random.randrange(1,4)
    move.y = random.randrange(1,4)
    #move.x = int(raw_input('give x: '))
    #move.y = int(raw_input('give y: '))
    rospy.loginfo('move is :' + str(move.x) + ' ' + str(move.y))
    pub_move.publish(move)
    return 'Player2 move Published'

def msg_callback(msg):
    rospy.loginfo(msg.data)
    rospy.loginfo('GAME OVER')
    rospy.signal_shutdown('game is over!!')




def table_callback(msg):
    rospy.loginfo('I am in table CallBack of Player2!!')
    show_table(msg.table)
    #show_table(msg.table)

def player2m():
    rospy.init_node('player2m')
    rate = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        sub_to_table = rospy.Subscriber('/table_topic',table,table_callback)
        sub_to_msgs = rospy.Subscriber('/player2_msgs',String,msg_callback)

        rospy.loginfo(publish_move())
        rate.sleep() 


if __name__ == "__main__":
    try:
        player2m()
    except rospy.ROSInterruptException:
        pass

