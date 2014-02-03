#!/usr/bin/env python
import cv2 as cv
# import pyopencv as cv
import roslib; roslib.load_manifest('artista')
import rospy

import numpy as np
from matplotlib import pyplot as plt

from rospy.numpy_msg import numpy_msg
from artista.msg import Plot



# define 0 as lower pen
# define 1 as raise pen

image_x = 1000.0
image_y = 1000.0

def createInstructionsFromPath(path, filterName="canny"):
	img = cv.imread(path, 0)
	image_y, image_x = img.shape
	image_x = float(image_x)
	image_y = float(image_y)
	
	edges = filter(img, filterName)

	# print str(image_y) + " " + str(image_x)

	return generateInstructions(edges, 240)
	# print "finish processing edges"
	# print str(len(instructions[0]))

	# for instruction in instructions:
	# 	print instruction
	
def createInstructionsFromImage(img, filterName="canny"):
	image_y, image_x = img.shape
	image_x = float(image_x)
	image_y = float(image_y)
	
	edges = filter(img, filterName)

	# print str(image_y) + " " + str(image_x)

	return  generateInstructions(edges, 240)

def filter(image, filterName):
	if(filterName=="canny"):
		return cv.Canny(image,100,200)
	
	print "Filter not found"
	return None
	
def generateInstructions(image, colour=255):
	pixels_visited = {}
	instructions = np.array([], dtype=Plot)
	x=0
	for line in image:
		y=0
		# sys.stdout.write(str(i) + ": ")
		# sys.stdout.flush()
		for pixel in line:
			
			if ((x,y) not in pixels_visited):
				pixels_visited[(x,y)] = True
				if(pixel>=colour):
					np.append(instructions, Plot(x/image_x, y/image_y, 0))
					pen_state = 0
					pen_state = processLine(x, y, instructions, pen_state, pixels_visited, image, colour)
			y+=1
		x+=1
	return instructions
	
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
	print "x: %i, y: %i, x_d: %i, y_d: %i" % (x, y, x_direction, y_direction)
	if(((x + x_direction, y + y_direction) not in pixels_visited) and (0<(x + x_direction)<=image_x) and (0<(y + y_direction)<=image_y) and image[x + x_direction][y + y_direction]>=colour):
		if(pState==1):
			np.append( instructions, Plot(x/image_x, y/image_y, pState) )
			pState = 0
			np.append( instructions, Plot(x/image_x, y/image_y, pState) )
		np.append(instructions,  Plot( (x + x_direction)/image_x, (y + y_direction)/image_y, pState ))
		pixels_visited[ (x + x_direction, y + y_direction) ] = True
		pState = processLine(x + x_direction, y + y_direction, instructions, pState, pixels_visited, image, colour)
	pixels_visited[(x + x_direction, y + y_direction)] = True
	return pState

if __name__ == '__main__':
	# createInstructionsFromPath("C:\Users\Andrew\Documents\GitHub\Artista\photos\circle.jpg")
	createInstructionsFromPath("/home/teamu/catkin_ws/src/Artista/photos/circle.jpg")