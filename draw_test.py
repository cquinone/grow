from tkinter import *
from PIL import Image, ImageDraw
from functools import reduce
import operator as op
import random as rand
import math
import sys


pic_width = 500
pic_height = 500
white = (255, 255, 255)
choco = (210,105,30)
sienna = (160,82,45)
peru = (205,133,63)
maroon = (128,0,0)
leaf = (41,172,32)
baby_turtle = (142,255,134)
jungle = (7,100,1)
amoeba = (139,199,159)
BROWNS = [choco,sienna,peru,maroon]
GREENS = [leaf,baby_turtle,jungle,amoeba]


def nchoosek(n,k):
	k = min(k,n-k)
	numerator = reduce(op.mul,range(n,n-k,-1),1)
	denominator = reduce(op.mul, range(1,k+1),1)
	return numerator // denominator


# return bezier point corresponding to given control points and t
def bezier(t,points):
	b_point = [0,0]
	n = len(points)-1  # to get correct binaomial coeffs
	for i in range(0,n+1):
		#print("i, points[i], com(n,i):", i,points[i],nchoosek(n,i))
		b_point[0] = b_point[0] + nchoosek(n,i)*((1-t)**(n-i))*(t**i)*points[i][0]
		b_point[1] = b_point[1] + nchoosek(n,i)*((1-t)**(n-i))*(t**i)*points[i][1]
	return b_point


def draw_rules(image1,draw):
	points = [[250.0, 0],
		[250.0, 0],
		[246.3976714644102, 21.36406768166191],
		[246.3976714644102, 21.36406768166191],
		[246.3976714644102, 21.36406768166191],
		[246.3976714644102, 21.36406768166191],
		[242.3407812273183, 42.6859406235677],
		[242.3407812273183, 42.6859406235677],
		[242.3407812273183, 42.6859406235677],
		[242.3407812273183, 42.6859406235677],
		[245.16521534708335, 64.23952430186912],
		[245.16521534708335, 64.23952430186912],
		[245.16521534708335, 64.23952430186912],
		[245.16521534708335, 64.23952430186912],
		[241.71738305377391, 80.2867533201888],
		[241.71738305377391, 80.2867533201888],
		[241.71738305377391, 80.2867533201888],
		[241.71738305377391, 80.2867533201888],
		[244.4200424936087, 95.36064039975479],
		[244.4200424936087, 95.36064039975479],
		[244.4200424936087, 95.36064039975479],
		[244.4200424936087, 95.36064039975479],
		[235.20641483297294, 107.3655245458313],
		[235.20641483297294, 107.3655245458313],
		[235.20641483297294, 107.3655245458313],
		[235.20641483297294, 107.3655245458313],
		[245.26169840670585, 126.87271759432656],
		[245.26169840670585, 126.87271759432656],
		[245.26169840670585, 126.87271759432656],
		[245.26169840670585, 126.87271759432656],
		[247.75672089714928, 141.8421420367613],
		[247.75672089714928, 141.8421420367613],
		[247.75672089714928, 141.8421420367613],
		[247.75672089714928, 141.8421420367613],
		[232.877151525925, 158.6556700782413],
		[232.877151525925, 158.6556700782413],
		[232.877151525925, 158.6556700782413],
		[232.877151525925, 158.6556700782413],
		[217.67598870480322, 174.08274303699582],
		[217.67598870480322, 174.08274303699582],
		[217.67598870480322, 174.08274303699582],
		[217.67598870480322, 174.08274303699582],
		[208.8895562034398, 191.54367546549895],
		[208.8895562034398, 191.54367546549895],
		[208.8895562034398, 191.54367546549895],
		[208.8895562034398, 191.54367546549895],
		[209.6091735694422, 211.57800878163988],
		[209.6091735694422, 211.57800878163988],
		[209.6091735694422, 211.57800878163988],
		[209.6091735694422, 211.57800878163988],
		[202.74517852511516, 224.9525568721879],
		[202.74517852511516, 224.9525568721879],
		[202.74517852511516, 224.9525568721879],
		[202.74517852511516, 224.9525568721879],
		[211.36848073345317, 248.35659564660259],
		[211.36848073345317, 248.35659564660259],
		[211.36848073345317, 248.35659564660259],
		[211.36848073345317, 248.35659564660259],
		[208.05650044655331, 264.71209777016617],
		[208.05650044655331, 264.71209777016617],
		[208.05650044655331, 264.71209777016617],
		[208.05650044655331, 264.71209777016617],
		[214.05424836408397, 279.98299956952127],
		[214.05424836408397, 279.98299956952127]
		]

	pointss = [ [1,1],[2,3],[4,3],[6,4] ]


	for i in range(0,len(points)-1):
		if i != len(points)-1:
			draw.line([points[i][0],points[i][1],points[i+1][0],points[i+1][1]],fill=choco,width=4)

	for t in range(0,1000):
		t = t/1000.0
		curr_point = bezier(t,points)
		print(curr_point,t)
		draw.point([curr_point[0],curr_point[1]], fill=leaf)

	return image1,draw
	#
	## do the PIL image/draw (in memory) drawings
	#draw.line([0, 250, width, 250], branch_color)
	## example polygon, some traingle on triangle thing
	#draw.polygon([(128,128),(384,384),(128,384),(384,128)],
	#          fill=main_color,outline=(255,0,0,255))


def create_tree(filename):
	# AUTO DRAW CODE THAT CREATES AND SAVES PNG 
	# PIL create an empty image and draw object to draw on
	# memory only, not visible
	image1 = Image.new("RGB", (pic_width, pic_height), white)
	draw = ImageDraw.Draw(image1)


	# gen drawing from rules
	image1, draw = draw_rules(image1, draw)
	
	# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
	#filename = "tree.png"
	image1.save(filename+".png")



create_tree("point")

# generate rules for plant structure...
# so like trunk num, trunk color (color vals could be combined and remixed!!)
# branch num -> choose either? 

# or different type---> literally write list where drawing steps are followed
# then have splice pooints and take splices via fitness
#EXAMPLE:
# ##TRUNKS##
# (this will be all lines, but only requires lengths and angles)
# LINE(start, end, width, color)
# LINE(start, end, width, color)
# (will need to have algo to gen starts, ends, widthz based on angles desired and so on..)
# ##BRANCHES##
# LINE(start, end, width, color)
# LINE(start, end, width, color)
# ##LEAVES##
# CIRCLE(x,y,radius,color)
# CIRCLE(x,y,radius,color)

# so gen rules code, draw rules code, and cross rules code
# first make gen rules code!!



