from PIL import Image, ImageDraw
from functools import reduce
import operator as op
import random as rand
import math
import sys


pic_width = 500
pic_height = 500
white = (255, 255, 255)
green = (41,172,32)
brown = (210,105,30)


def draw_poly(image1,draw,points,widths):
	for i in range(0,len(points)-1,2):
		print("ON i = ", i)
		print("doing points: ",points[i][0],points[i][1] ," to ",points[i+1][0],points[i+1][1])
		if i == 0:
			w = widths[0]
		elif i == 2:
			w = widths[1]
		draw.line([points[i][0],points[i][1],points[i+1][0],points[i+1][1]],fill=brown,width=w)

	a = points[1][0] - points[0][0]
	b = points[1][1] - points[0][1]
	print("a,b: ",a,b)
	if a != 0:
		d = -(widths[0]/2)*(1/(math.sqrt((b/a)**2 + 1)))
		c = (b/a)*d
	elif a == 0:
		c = -widths[0]/2
		d = 0

	e = points[3][0] - points[2][0]
	f = points[3][1] - points[2][1]
	print("e,f: ",e,f)
	g = -(widths[1]/2)*(1/math.sqrt((f/e)**2 + 1))
	h = (f/e)*g
	# hack in agles this time, but usually save angle to know... or just check if next x lesser  / greater...
	p1 = points[1]
	p2 = [p1[0]+c,p1[1]+d]
	p3 = [p1[0]+h,p1[1]-g]
	print(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1])
	draw.polygon([p1[0],p1[1],p2[0],p2[1],p3[0],p3[1]],fill=brown,outline=None)

	return image1,draw


def create_curve_img(filename):
	# PIL create an empty image and draw object to draw on
	# memory only, not visible
	image1 = Image.new("RGB", (pic_width, pic_height), white)
	draw = ImageDraw.Draw(image1)

	# example points, modify this
	points = [[250,0],[250,11.26468028654089],[250,11.26468028654089],[254.5154765785274,17.59485579034518 ]]
	widths = [15,10]

	# actually draw the points
	image1, draw = draw_poly(image1, draw, points,widths)
	
	# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
	image1.save(filename+".png")


create_curve_img("something")