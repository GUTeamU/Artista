#!/usr/bin/env python
import roslib; roslib.load_load_manifest('artista')
import rospy
from artista.srv import *


def handle_get_image_request(req):
	print str(req)
	return GetImageResponse();

def main():

	rospy.init_node('capture_server')	

	global takenImage
	takenImage = image
	rospy.init_node('capture_service')
	s = rospy.service('take_photo',Image,handle_get_image_request)
	rospy.Subscriber("",image,takenImage)
	rospy.spin()

if __name__ = '__main__':
	try:
		main()
	except rospy.ROSInterruptException: pass
