#!/usr/bin/env python

import sys
import rospy
from tic_tac_toe.msg import table
from tic_tac_toe.srv import *
#from std_msgs.msg import String

table = [0]*9

def decide_winner(win):
    if win == 0:
        mes = 'showing Table after Play... '
    elif win == 1:
        mes = 'player1 won'
    elif win == 2:
        mes = 'player2 won'
    return mes


def handle_request(req):

    rospy.longinfo("Requesting move...i")
    #for invalid move post table
    if req.x > 3 or req.y > 3:
        mes = 'showing Table'
        rospy.longinfo(mes)
        return moveResponse(mes,table)
     # calculating change in table 
    pos = 3*(req.x-1) + req.y - 1
    
    if table[pos] != 0:
        mes = 'Position already taken.. Showin table...'
        rospy.loginfo(mes)
        return moveResponse(mes,table)

    # Desiding who made move  
    if req.player == './src/player1.py':
        table[pos] = 1
    if req.player == './src/player2.py':
        table[pos] = 2


    win = evaluate_winner()
    mes = decide_winner(win)

    if win != 0:
        rospy.signal_shutdown('game is over!!')

    return moveResponse(mes,table)


def evaluate_winner():
    # Evaluate Rows
    if table[0] == table[1] == table[2] != 0:
        rospy.longinfo ('Winner Found at first row')
        return table[0]
    if table[3] == table[4] == table[5] != 0:
        rospy.longinfo ('Winner Found at second row')
        return table[3]
    if table[6] == table[7] == table[8] != 0:
        rospy.longinfo ('Winner Found at third row')
        return table[6]
    # Evaluate Cols
    if table[0] == table[3] == table[6] != 0:
        rospy.longinfo ('Winner Found at first col')
        return table[0]
    if table[1] == table[4] == table[7] != 0:
        rospy.longinfo ('Winner Found at second col')
        return table[1]
    if table[2] == table[5] == table[8] != 0:
        rospy.longinfo ('Winner Found at third col')
        return table[2]
    # Evaluate Diagonals 
    if table[0] == table[4] == table[8] != 0:
        rospy.longinfo ('Winner Found at diag 1')
        return table[0]
    if table[2] == table[4] == table[6] != 0:
        rospy.longinfo ('Winner Found at diag 2')
        return table[2]

    return 0


def tic_tac_toe_server():
    rospy.init_node('server')
    s = rospy.Service('move_implement', move, handle_request)
    rospy.spin()

if __name__ == "__main__":
    tic_tac_toe_server()




