#!/usr/bin/env python

from __future__ import print_function
import rospy
# Brings in the SimpleActionClient
import actionlib
import random
# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import tic_tac_toe.msg

def player1_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    # 'player1client' is the ns (namespace)
    client = actionlib.SimpleActionClient('player1client', tic_tac_toe.msg.playAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = tic_tac_toe.msg.playGoal()
    goal.x = random.randrange(1,7)
    goal.y = random.randrange(1,4)
    goal.player = 'player2'
    #rospy.loginfo('the goal is %d',goal.x)
    #rospy.loginfo('the goal is %d',goal.y)
    #rospy.loginfo('the name  is %s',goal.player)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result(),client.get_state()  # A FibonacciResult


if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('player2client')
        rate = rospy.Rate(0.5)
        while not rospy.is_shutdown():
            result,state = player1_client() # if state is 4 means goal was aborted
                                            # according to actionlib cocumentation
            rospy.loginfo(state)
            print(result.table)
            rate.sleep()
    except rospy.ROSInterruptException:
        print("program interrupted before completion", file=sys.stderr)



