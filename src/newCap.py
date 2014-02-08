#!/usr/bin/env python
import roslib; roslib.load_manifest('artista')
import sys
import rospy
import cv
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class capture_image:
	def __init__(self):
	#	self.image_pub = rospy.Publisher("image_topic_2",Image)
	
		cv.NamedWindow("Image Window", 1)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/camera/image_raw",Image,self.callback)

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv(data,"bgr8")
		except CvBridgeError, e:
			print e
		
		cv.ShowImage("Image Window", cv_image)
		cv.SaveImage("face.png",cv_image)

def main():
	ci = capture_image()
	rospy.init_node('image_converter', anonymous=True) # Don't know if needed.
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Shutting down"
	cv.DestroyAllWindows()

if __name__ == '__main__':
	main()
