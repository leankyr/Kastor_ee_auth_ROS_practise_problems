#!/usr/bin/env python

import sys
import rospy

import actionlib
#from tic_tac_toe.msg import playAction, playGoal, playActionFeedback, playActionResult
import tic_tac_toe.msg #Can't gasp what exactly to import so I import everything
board = [0]*9

class ticTacToeAction(object):
    # messages that are used to publish feedback result
    # These are the class variables
    feedback = tic_tac_toe.msg.playFeedback()
    result = tic_tac_toe.msg.playResult()
    
#### Below is the constructor of the class ####

    def __init__(self, name):
        self._action_name = 'player1client' # I could possibly give the name through a yaml file
        # tic_tac_toe.msg.playAction is the actionSpec
        self._as = actionlib.SimpleActionServer(self._action_name, tic_tac_toe.msg.playAction, execute_cb=self.execute_cb, auto_start = False)   # as stands for action server
        self._as.start()

    def execute_cb(self, goal):
        # helper variables
        r = rospy.Rate(1)
        success = True
        #rospy.loginfo('I am in execute CB!!!')
        if goal.x > 3:
            success = False


        pos = 3*(goal.x-1) + goal.y - 1
        if success:
            if goal.player == 'player2':
                board[pos] = 2
            else:
                board[pos] = 1

        if success:
            # set feedback mesage 
            self.feedback.message = 'Move taken into consideration'
            # publish feedback message to topic /player1client/feedback
            # I can See the feedback by subscribing to the above topic
            # I could also use the functions from previous implementations
            # to make it more realistic
            self._as.publish_feedback(self.feedback)
            # the board as result
            self.result.table = board
            rospy.loginfo('%s: Succeeded' %self._action_name)
            # publish the result and set it as succeded
            self._as.set_succeeded(self.result)
        else:
            self.feedback.message = 'Move out of bounds'
            self._as.publish_feedback(self.feedback)
            # the board as result
            rospy.loginfo('%s: aboorted' %self._action_name)
            self._as.set_aborted(self.result, 'move out of bounds')


############^^^^ End of callback ^^^^#####################



if __name__ == "__main__":
    try:
        rospy.init_node('action_server')
        # server must have the same name as the class
        server = ticTacToeAction(rospy.get_name())
        # rospy.get_name() passes the name of the node to the class
        rospy.loginfo(rospy.get_name())
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
