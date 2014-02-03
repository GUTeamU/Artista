#!/usr/bin/env python
import roslib; roslib.load_manifest('artista')
import rospy, smach, smach_ros, math, copy, tf, PyKDL, os, shutil
import cv
import sys
import numpy as np
import os.path
import tf

from smach import State, Sequence
from clopema_smach import *
from geometry_msgs.msg import *
from sensor_msgs.msg import Image
from rospy.numpy_msg import numpy_msg
from cv_bridge import *
from artista.srv import Image


def main():
    
    rospy.init_node('capture')

    img = picture()
    cv.ShowImage(img)
    cv.WaitKey()
    cv.DestroyWindow()
    cv.SaveImage("face.png",img)


def picture():
    takenImage = None
    rospy.wait_for_service('take_photo')
    try:
        service = rospy.ServiceProxy('take_photo',Image)  #calls the service
        response = service() 
        imData = response.image #Should return the image

    except rospy.ServiceException, e:

        show_message("Could not return image", MsgTypes.exception)
        return None

    try:
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv(imData,"bgr8") #maybe rgb8 ?
    except CvBridgeError, e:
        show_message("Failed to convert the image", MsgTypes.exception)
        return None
    
    return takenImage

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
