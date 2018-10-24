#!/usr/bin/env python

import sys
import rospy
from tic_tac_toe.msg import table, moveMessage
from std_msgs.msg import String
board = [0]*9



def evaluate_winner():
# Evaluate Rows
    if board[0] == board[1] == board[2] != 0:
        rospy.loginfo ('Winner Found at first row')
        return board[0]
    if board[3] == board[4] == board[5] != 0:
        rospy.loginfo ('Winner Found at second row')
        return board[3]
    if board[6] == board[7] == board[8] != 0:
        rospy.loginfo ('Winner Found at third row')
        return board[6]
# Evaluate Cols
    if board[0] == board[3] == board[6] != 0:
        rospy.loginfo ('Winner Found at first col')
        return board[0]
    if board[1] == board[4] == board[7] != 0:
        rospy.loginfo ('Winner Found at second col')
        return board[1]
    if board[2] == board[5] == board[8] != 0:
        rospy.loginfo ('Winner Found at third col')
        return board[2]
    # Evaluate Diagonals 
    if board[0] == board[4] == board[8] != 0:
        rospy.loginfo ('Winner Found at diag 1')
        return board[0]
    if board[2] == board[4] == board[6] != 0:
        rospy.loginfo ('Winner Found at diag 2')
        return board[2]

    return 0


def shutdown_server(win,m1,m2):
    if win == 1:
        msg1 = String()
        msg2 = String()

        print "HEY I IS ANYONE ALIVE OUT THERE???"
        msg1.data = 'Congrats You Won!!'
        msg2.data = 'You are Unworthy!!'
        m1.publish(msg1)
        m2.publish(msg2)
        print "message published"
    else:
        msg1 = String()
        msg2 = String()

        print "NOOOOOOO"
        msg2.data = 'Congrats You Won!!'
        msg1.data = 'You are Unworthy!!'
        m1.publish(msg1)
        m2.publish(msg2)
        print "message published"

    rospy.loginfo('Sleeping for 10...')
    #rospy.sleep(10)
    rospy.signal_shutdown('game is over!!')



def publish_board(table_pub,m1,m2):
    rospy.loginfo('Publishing board....')
    rospy.loginfo(board)
    msg = table()
    msg.table = board
    rospy.loginfo('Evaluate Winner is %d',evaluate_winner())
    table_pub.publish(msg)
    if evaluate_winner() != 0:
        shutdown_server(evaluate_winner(),m1,m2)


def player1_callback(msg,args):
    
    rospy.loginfo('Got into Player Callback1!!')
    table_pub = args
    pos = 3*(msg.x-1) + msg.y - 1
    board[pos] = 1
    msg_of_table = table()
    msg_of_table.table = board

    table_pub.publish(msg_of_table)



def player2_callback(msg,args):
    rospy.loginfo('Got into Player Callback2!!')
    table_pub = args
    pos = 3*(msg.x-1) + msg.y - 1
    board[pos] = 2
    msg_of_table = table()
    msg_of_table.table = board

    table_pub.publish(msg_of_table)


def tic_tac_toe_server():
    rospy.init_node('m_server',)
    table_pub = rospy.Publisher('/table_topic',table,queue_size=10)
    msgs_to_P1 = rospy.Publisher('player1_msgs',String,queue_size=1)
    msgs_to_P2 = rospy.Publisher('player2_msgs',String,queue_size=1)

    rate = rospy.Rate(0.5)
    while not rospy.is_shutdown():
        publish_board(table_pub,msgs_to_P1,msgs_to_P2)
        Sub_to_play1 = rospy.Subscriber('/player1_moves',moveMessage,player1_callback,(table_pub))
        Sub_to_play2 = rospy.Subscriber('/player2_moves',moveMessage,player2_callback,(table_pub))
        rate.sleep()


if __name__ == "__main__":
    try:
        tic_tac_toe_server()
    except rospy.ROSInterruptException:
        pass
