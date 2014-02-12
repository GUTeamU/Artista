#!/usr/bin/env python
# import cv2
import cv2 as cv
# import pyopencv as cv

# define 0 as lower pen
# define 1 as raise pen

image_x = 1000.0
image_y = 1000.0

pixels_visited = {}
instructions = []
cur_x = -1
cur_y = -1

def createInstructionsFromPath(path, filterName="Canny"):
	global image_x
	global image_y
	img = cv.imread(path, 0)
	image_y, image_x = img.shape
	print image_y
	print image_x
	edges = filter(img, filterName)
	# cv.imwrite("canny.jpg", edges)
	# print generateInstructions(edges, 240)
	return generateInstructions(edges, 240)
	
def createInstructionsFromImage(img, filterName="Canny"):
	global image_x
	global image_y
	image_x, image_y = img.shape
	image_x = float(image_x)
	image_y = float(image_y)
	
	edges = filter(img, filterName)

	return  generateInstructions(edges, 240)

def filter(image, filterName):
	if(filterName.lower()=="canny"):
		return cv.Canny(image,100,200)
	elif(filterName.lower()=="custom"):
		custom(image)
		# Add your stuff here Fraser or Michael
	print "Filter not found"
	return image

def custom(img):
	# convert to greyscale (notice spelling :( )
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# adjust contrast to darken the image, 
	hist = cv2.equalizeHist(gray)
	# create the gaussian filter
	gb = cv2.GaussianBlur(hist, (7,7), 7.0/6.0)
	# edge detection on blurred increased contrast image 
	cannyDetection = cv.Canny(gb, 100, 200)
		
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

	# X #
	# o #
	# # #
	if(check(-1, 0, image, colour)):
		return 0
	
	# # X
	# o #
	# # #
	elif(check(-1, 1, image, colour)):
		return 1


	# # #
	# o X
	# # #
	elif(check(0, 1, image, colour)):
		return 2

	
	# # #
	# o #
	# # X
	elif(check(1, 1, image, colour)):
		return 3

	
	# # #
	# o #
	# X #
	elif(check(1, 0, image, colour)):
		return 4

	
	# # #
	# o #
#	X # #
	elif(check(1, -1, image, colour)):
		return 5

	
	# # #
#	X o #
	# # #
	elif(check(0, -1, image, colour)):
		return 6

	
#	X # #
	# o #
	# # #
	elif(check(-1, -1, image, colour)):
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


if __name__ == '__main__':
	# createInstructionsFromPath("wiener.jpg", "None")
	# print createInstructionsFromPath("wiener.jpg")
	print createInstructionsFromPath("../photos/circle.jpg", "None")
