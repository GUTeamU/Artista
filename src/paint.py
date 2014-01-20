#!/usr/bin/env python
import roslib; roslib.load_manifest('artista')
import rospy, smach, smach_ros, math, copy, tf, PyKDL, os, shutil, numpy
from tf.transformations import quaternion_from_euler, quaternion_about_axis
from tf_conversions import posemath
from smach import State, Sequence

from clopema_smach import *
from geometry_msgs.msg import *

import cv2 as cv
# import pyopencv as cv
import numpy as np

from matplotlib import pyplot as plt

VISUALIZE=True
CONFIRM=False
EXECUTE=True

IMAGE_PATH="/home/teamu/catkin_ws/src/Artista/photos/Testface.jpg"

EXT_POSITION = 0;
Z_OFFSET = 0.05


AWAY_HAND_LINK = 'r1_ee'
AWAY_X = -0.9
AWAY_Y = -0.3
AWAY_Z = 1.2

FRAME_ID = 'base_link'
DRAW_HAND_LINK = 'r2_ee'
DRAW_X = 0.25
DRAW_Y = -0.75
DRAW_Z = 0.729
DRAW_ORIENTATION = Quaternion(*quaternion_from_euler(math.pi, 0, math.pi))

GRAB_X = 0.35
GRAB_Y = -0.65
GRAB_Z = 0.75 + Z_OFFSET

GRAB_ORIENTATION_Y = 1

# define 0 as lower pen
# define 1 as raise pen
	
def createInstructions(image, colour=255):
	print "createIn"
	pixels_visited = {}
	set_of_instructions = []
	x=0
	for line in image:
		
		y=0
		# sys.stdout.write(str(i) + ": ")
		# sys.stdout.flush()
		for pixel in line:
			
			if ((x,y) not in pixels_visited):
				pixels_visited[(x,y)] = True
				if(pixel>=colour):
					set_of_instructions.append((DRAW_X - (x/100.0), DRAW_Y - (y/100.0), DRAW_Z + Z_OFFSET))
					set_of_instructions.append((DRAW_X - (x/100.0), DRAW_Y - (y/100.0), DRAW_Z))
					pen_state = 0
					pen_state = processLine(x, y, set_of_instructions, pen_state, pixels_visited, image, colour)
					# set_of_instructions.append(instructions)
			y+=1
		x+=1
	return set_of_instructions

def processLine(x, y, instructions, pen_state, pixels_visited, image, colour):
	
	pState = pen_state
	
	# X #
	# o #
	# # #
	pState = checkDirection(x, y, -1, 0, instructions, pState, pixels_visited, image, colour)
	
	# # X
	# o #
	# # #
	pState = checkDirection(x, y, -1, 1, instructions, pState, pixels_visited, image, colour)


	# # #
	# o X
	# # #
	pState = checkDirection(x, y, 0, 1, instructions, pState, pixels_visited, image, colour)

	
	# # #
	# o #
	# # X
	pState = checkDirection(x, y, 1, 1, instructions, pState, pixels_visited, image, colour)

	
	# # #
	# o #
	# X #
	pState = checkDirection(x, y, 1, 0, instructions, pState, pixels_visited, image, colour)

	
	# # #
	# o #
#	X # #
	pState = checkDirection(x, y, 1, -1, instructions, pState, pixels_visited, image, colour)

	
	# # #
#	X o #
	# # #
	pState = checkDirection(x, y, 0, -1, instructions, pState, pixels_visited, image, colour)

	
#	X # #
	# o #
	# # #
	pState = checkDirection(x, y, -1, -1, instructions, pState, pixels_visited, image, colour)

		
	if(pState != 1):
		instructions.append((DRAW_X - (x/100.0), DRAW_Y - (y/100.0), DRAW_Z + Z_OFFSET))
	return 1
	
def checkDirection(x, y, x_direction, y_direction, instructions, pState, pixels_visited, image, colour):
	if(((x + x_direction, y + y_direction) not in pixels_visited) and image[x + x_direction][y + y_direction]>=colour):
		if(pState==1):
			instructions.append((DRAW_X - (x/100.0), DRAW_Y - (y/100.0), DRAW_Z + Z_OFFSET))
			instructions.append((DRAW_X - (x/100.0), DRAW_Y - (y/100.0), DRAW_Z))
			pState = 0
		instructions.append((DRAW_X - ((x + x_direction)/100.0), DRAW_Y - ((y + y_direction)/100.0), DRAW_Z))
		pixels_visited[(x + x_direction, y + y_direction)] = True
		pState = processLine(x + x_direction, y + y_direction, instructions, pState, pixels_visited, image, colour)
	pixels_visited[(x + x_direction, y + y_direction)] = True
	return pState
	
def path_from_image(filename):
    print filename
    img = cv.imread(filename,0)
    print img
    edges = cv.Canny(img,100,200)
    print edges
    # print createInstructions(edges)
    return createInstructions(edges)
    return [
            (DRAW_X, DRAW_Y, DRAW_Z + Z_OFFSET),
            (DRAW_X, DRAW_Y, DRAW_Z),
            (DRAW_X, DRAW_Y - 0.1, DRAW_Z),
            (DRAW_X - 0.1, DRAW_Y - 0.1, DRAW_Z),
            (DRAW_X - 0.1, DRAW_Y, DRAW_Z),
            (DRAW_X, DRAW_Y, DRAW_Z),
            (DRAW_X, DRAW_Y, DRAW_Z + Z_OFFSET)
           ]


def grab_plan(sq):
    
    pose = PoseStamped()
    pose.header.frame_id = FRAME_ID
    pose.pose.position.x = GRAB_X
    pose.pose.position.y = GRAB_Y
    pose.pose.position.z = GRAB_Z
    pose.pose.orientation = DRAW_ORIENTATION

    goals = []
    goals.append(pose.pose)

    sq.userdata.poses = goals
    sq.userdata.ik_link = DRAW_HAND_LINK
    sq.userdata.frame_id = FRAME_ID
    sq.userdata.offset_plus = Z_OFFSET
    sq.userdata.offset_minus = Z_OFFSET

    return gensm_plan_vis_exec(PlanGraspItState(), confirm=CONFIRM, visualize=VISUALIZE, execute=EXECUTE)

def home_plan():
    return gensm_plan_vis_exec(PlanToHomeState(), confirm=CONFIRM, visualize=VISUALIZE, execute=EXECUTE)

def ext_plan():
    sq = Sequence(outcomes=['succeeded', 'aborted', 'preempted'], connector_outcome='succeeded')
    sq.userdata.position = EXT_POSITION;

    plan = gensm_plan_vis_exec(PlanExtAxisState(), confirm=CONFIRM, visualize=VISUALIZE, execute=EXECUTE)
    with sq:
        Sequence.add("EXTA", plan)

    return sq

def away_plan():
    sq = Sequence(outcomes=['succeeded', 'aborted', 'preempted'], connector_outcome='succeeded')

    pose = PoseStamped()
    pose.header.frame_id = 'base_link'
    pose.pose.position.x = AWAY_X
    pose.pose.position.y = AWAY_Y
    pose.pose.position.z = AWAY_Z
    pose.pose.orientation = DRAW_ORIENTATION

    sq.userdata.goal = pose
    sq.userdata.ik_link = AWAY_HAND_LINK
    sq.userdata.frame_id = FRAME_ID

    plan = gensm_plan_vis_exec(Plan1ToXtionPoseState(), confirm=CONFIRM, visualize=VISUALIZE, execute=EXECUTE)
    with sq:
        Sequence.add("EXTA", plan)

    return sq

def draw_plan(path):
    pose = Pose()
    pose.orientation = DRAW_ORIENTATION
    poses = []

    for point in path:
	print point
        pose.position.x = point[0]
        pose.position.y = point[1]
        pose.position.z = point[2]
        poses.append(copy.deepcopy(pose))

    sq = smach.Sequence(outcomes=['succeeded', 'preempted', 'aborted'], connector_outcome='succeeded')
    goto_plan = gensm_plan_vis_exec(Plan1ToPoseState(), input_keys=['goal', 'ik_link'], confirm=CONFIRM, visualize=VISUALIZE, execute=EXECUTE)
    sq.userdata.poses = PoseArray()
    sq.userdata.poses.header.frame_id = FRAME_ID
    sq.userdata.poses.poses = poses
    sq.userdata.frame_id = FRAME_ID
    sq.userdata.ik_link = DRAW_HAND_LINK

    with sq:
        smach.Sequence.add('POSE_BUFFER', PoseBufferState())
        smach.Sequence.add('GOTO', goto_plan, transitions={'aborted':'POSE_BUFFER', 'succeeded':'POSE_BUFFER'},
                           remapping={'goal':'pose'})

    return sq

def main():
    
    rospy.init_node('paint')

    sq = Sequence(outcomes=['succeeded', 'aborted', 'preempted'], connector_outcome='succeeded')
    print "HELP"
    with sq:
        Sequence.add('OPEN_GRIPPER', GripperState(2, True), {'succeeded':'TURN', 'aborted':'HOME'})
 	print "HELP1"
        Sequence.add("TURN", ext_plan(), transitions={'aborted':'HOME', 'succeeded':'AWAY'})
	print "HELP2"
        Sequence.add("AWAY", away_plan(), transitions={'aborted':'HOME', 'succeeded':'GRAB'})
	print "HELP3"
        Sequence.add("GRAB", grab_plan(sq), transitions={'aborted':'HOME', 'succeeded':'DRAW'})
	print "HELP4"
        Sequence.add("DRAW", draw_plan(path_from_image(IMAGE_PATH)), transitions={'aborted':'HOME', 'succeeded':'RELEASE'})
	print "HELP5"
        Sequence.add("RELEASE", GripperState(2, True), transitions={'aborted':'HOME', 'succeeded':'HOME'})
	print "HELP6"
        # TODO
        # Open hand to release -> HOME
        Sequence.add("HOME", home_plan(), transitions={'aborted':'POWER_OFF'})
	print "HELP7"
        Sequence.add("POWER_OFF", SetServoPowerOffState())
	print "HELP8"


    sis = smach_ros.IntrospectionServer('paint', sq, '/SM_ROOT')
    sis.start()
    os.system('clear')
    outcome = sq.execute()
    rospy.loginfo("State machine exited with outcome: " + outcome)
    sis.stop()

if __name__ == '__main__':
    main()
