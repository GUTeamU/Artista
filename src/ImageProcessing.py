#!/usr/bin/env python
import cv2 as cv
# import pyopencv as cv
import roslib; roslib.load_manifest('artista')
import rospy

import numpy as np
from matplotlib import pyplot as plt

from rospy.numpy_msg import numpy_msg
from artista.msg import Plotter



# define 0 as lower pen
# define 1 as raise pen

image_x = 1000.0
image_y = 1000.0
	
def createInstructions(image, colour=255):
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
					instructions =np.array([ Plotter(x/image_x, y/image_y, 0) ])
					pen_state = 0
					pen_state = processLine(x, y, instructions, pen_state, pixels_visited, image, colour)
					pub.publish(instructions)
					print instructions.data
					set_of_instructions.append(instructions)
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
		np.append(instructions, (x/image_x, y/image_y, 1) )
	return 1
	
def checkDirection(x, y, x_direction, y_direction, instructions, pState, pixels_visited, image, colour):
	
	if(((x + x_direction, y + y_direction) not in pixels_visited) and image[x + x_direction][y + y_direction]>=colour):
		if(pState==1):
			np.append( instructions, Plotter(x/image_x, y/image_y, pState) )
			pState = 0
			np.append( instructions, Plotter(x/image_x, y/image_y, pState) )
		np.append(instructions,  Plotter( (x + x_direction)/image_x, (y + y_direction)/image_y, pState ))
		pixels_visited[ (x + x_direction, y + y_direction) ] = True
		pState = processLine(x + x_direction, y + y_direction, instructions, pState, pixels_visited, image, colour)
	pixels_visited[(x + x_direction, y + y_direction)] = True
	return pState
	
rospy.Publisher("instructions", numpy_msg(Plotter))
pub = rospy.init_node('imageProcessing')
img = cv.imread('C:\Users\Andrew\Documents\GitHub\Artista\photos\circle.jpg', 0)
image_y, image_x = img.shape
image_x = float(image_x)
image_y = float(image_y)
edges = cv.Canny(img,100,200)

print str(image_y) + " " + str(image_x)

instructions = createInstructions(img, 240)
print "finish processing edges"
print str(len(instructions[0]))

for instruction in instructions:
	print instruction

