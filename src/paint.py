#!/usr/bin/env python
import roslib; roslib.load_manifest('artista')
import rospy, smach, smach_ros, math, copy, tf, PyKDL, os, shutil, numpy
from tf.transformations import quaternion_from_euler, quaternion_about_axis
from tf_conversions import posemath
from smach import State, Sequence

from clopema_smach import *
from geometry_msgs.msg import *

from rospy.numpy_msg import numpy_msg

from ImageProcessing import *
from faceCrop import *


VISUALIZE=True
CONFIRM=False
EXECUTE=True

IMAGE_PATH="./pictures/"

X_DIMENSION = 0.5    # The dimensions of the board we write on
Y_DIMENSION = 0.5

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
DRAW_Z = 0.747
DRAW_ORIENTATION = Quaternion(*quaternion_from_euler(math.pi, 0, math.pi))

GRAB_X = 0.35
GRAB_Y = -0.65
GRAB_Z = 0.75 + Z_OFFSET

GRAB_ORIENTATION_Y = 1

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

def draw_plan(path=IMAGE_PATH):
	pose = Pose()
	pose.orientation = DRAW_ORIENTATION
	poses = []
	
#	take_Picture(IMAGE_PATH)
	instructions = preprocessedCreateInstructions(IMAGE_PATH)

	for point in instructions:
		pose.position.x = DRAW_X - (point[0] * X_DIMENSION)
		pose.position.y = DRAW_Y - (point[1] * Y_DIMENSION)
		pose.position.z = DRAW_Z + (Z_OFFSET*point[2])
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

	with sq:
		Sequence.add('OPEN_GRIPPER', GripperState(2, True), {'succeeded':'TURN', 'aborted':'HOME'})

		Sequence.add("TURN", ext_plan(), transitions={'aborted':'HOME', 'succeeded':'AWAY'})

		Sequence.add("AWAY", away_plan(), transitions={'aborted':'HOME', 'succeeded':'GRAB'})

		Sequence.add("GRAB", grab_plan(sq), transitions={'aborted':'HOME', 'succeeded':'DRAW'})

		Sequence.add("DRAW", draw_plan(), transitions={'aborted':'HOME', 'succeeded':'RELEASE'})

		Sequence.add("RELEASE", GripperState(2, True), transitions={'aborted':'HOME', 'succeeded':'HOME'})

		# TODO
		# Open hand to release -> HOME
		Sequence.add("HOME", home_plan(), transitions={'aborted':'POWER_OFF'})

		Sequence.add("POWER_OFF", SetServoPowerOffState())



	sis = smach_ros.IntrospectionServer('paint', sq, '/SM_ROOT')
	sis.start()
	os.system('clear')
	outcome = sq.execute()
	rospy.loginfo("State machine exited with outcome: " + outcome)
	sis.stop()

if __name__ == '__main__':
	main()

