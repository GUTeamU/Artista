#!/usr/bin/env python
# import cv2
import cv2 as cv
# from lineDect import *
# import pyopencv as cv

# define 0 as lower pen
# define 1 as raise pen

image_x = 1000.0
image_y = 1000.0

scale_x = 2
scale_y = 2

pixels_visited = {}
instructions = []
cur_x = -1
cur_y = -1

def createInstructionsFromPath(path):
	global image_x
	global image_y
	
	source = path + "temp.jpg"
	destination = path + "temp_after.jpg"
	
	custom_filter(source, destination)
	
	img = cv.imread(source, 0)
	edges = cv.imread(destination, 0)
	image_y, image_x = edges.shape
	
	return generateInstructions(edges, 240)

def preprocessedCreateInstructions(path):
	global image_x
	global image_y
	
	source = path + "temp_after.jpg"
	
	img = cv.imread(source, 0)
	image_y, image_x = img.shape
	
	return generateInstructions(img, 240)

	
# def createInstructionsFromImage(img, filterName="Canny"):
# 	global image_x
# 	global image_y
# 	image_x, image_y = img.shape
# 	image_x = float(image_x)
# 	image_y = float(image_y)
	
# 	edges = filter(img, filterName)

# 	return  generateInstructions(edges, 240)

# def filter(image, filterName):

# 	elif(filterName.lower()=="custom"):
# 		custom_filter(source, destination)
		
# 	print "Filter not found"
# 	return image
		
def generateInstructions(image, colour=255):
	global pixels_visited
	global instructions

	y=0
	for line in image:
		x=0
		for pixel in line:
			
			if ((x,y) not in pixels_visited):
				pixels_visited[(x,y)] = True
				if(pixel>=colour):
					instructions.append((x/float(image_x), y/float(image_y), 1))
					instructions.append((x/float(image_x), y/float(image_y), 0))
					processLine(x, y, image, colour)
			x+=1
		y+=1
	return instructions
	
def processLine(x, y, image, colour):
	global cur_x
	global cur_y
	cur_x = x
	cur_y = y
	while(nextInstruction(image, colour) != -1):
		continue
	instructions.append((cur_x/float(image_x), cur_y/float(image_y), 1))
	return
	
def nextInstruction(image, colour):
	
	scale_Factor = 1
	# X #
	# o #
	# # #
	if(check(-1 * scale_Factor, 0 * scale_Factor, image, colour)):
		return 0
	
	# # X
	# o #
	# # #
	elif(check(-1 * scale_Factor, 1 * scale_Factor, image, colour)):
		return 1


	# # #
	# o X
	# # #
	elif(check(0 * scale_Factor, 1 * scale_Factor, image, colour)):
		return 2

	
	# # #
	# o #
	# # X
	elif(check(1 * scale_Factor, 1 * scale_Factor, image, colour)):
		return 3

	
	# # #
	# o #
	# X #
	elif(check(1 * scale_Factor, 0 * scale_Factor, image, colour)):
		return 4

	
	# # #
	# o #
#	X # #
	elif(check(1 * scale_Factor, -1 * scale_Factor, image, colour)):
		return 5

	
	# # #
#	X o #
	# # #
	elif(check(0 * scale_Factor, -1 * scale_Factor, image, colour)):
		return 6

	
#	X # #
	# o #
	# # #
	elif(check(-1 * scale_Factor, -1 * scale_Factor, image, colour)):
		return 7
	
	return -1

def check(x_direction, y_direction, image, colour):
	global pixels_visited
	global instructions
	global cur_x
	global cur_y


	if(((cur_x + x_direction, cur_y + y_direction) not in pixels_visited) \
	   and (0<(cur_x + x_direction)) \
	   and ((cur_x + x_direction)<image_x) \
	   and (0<(cur_y + y_direction)) \
	   and ((cur_y + y_direction)<image_y) \
	   and image[cur_y + y_direction][cur_x + x_direction]>=colour):
		instructions.append(( (cur_x + x_direction)/float(image_x), (cur_y + y_direction)/float(image_y), 0))
		cur_x += x_direction
		cur_y += y_direction
		pixels_visited[(cur_x, cur_y)] = True
		return True
	pixels_visited[(cur_x + x_direction, cur_y + y_direction)] = True
	return False

def draw(point, pen):
	pen.setx(-point[0] * image_x * scale_x)
	pen.sety(-point[1] * image_y * scale_y)
	if(point[2]<0.5):
		pen.pendown()
	else:
		pen.penup()
	

if __name__ == '__main__':
	
	import turtle
	wn = turtle.Screen()
	wn.screensize(image_x, image_y)
	pen = turtle.Turtle() 
	pen.shape("circle")
	pen.turtlesize(0.1, 0.1)
	
	# instructions = createInstructionsFromPath("./pictures/")
	instructions = preprocessedCreateInstructions("./pictures/")
	# print instructions
	
	for point in instructions:
		draw(point, pen)
	wn.exitonclick()
