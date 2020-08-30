from tkinter import *
from PIL import Image, ImageDraw
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


class line_piece():
    def __init__(self,name,x_start,y_start,x_end,y_end,width,color,identity):
    	self.name = name
    	self.x_start = x_start
    	self.y_start = y_start
    	self.x_end = x_end
    	self.y_end = y_end
    	self.width = width
    	self.color = color
    	self.identity = identity


# for fruits and trunk
def gen_color():
	r = rand.randint(0,255)
	if r >= 200:
		g = rand.randint(0,120)
	if r < 200:
		g = rand.randint(0,255)
	if r >= 200 and g >=100:
		b = rand.randint(0,100)
	if r < 200 or g < 100:
		b = rand.randint(0,255)
	return (r,g,b)


# generate the text rules used to draw a tree png
def gen_rules():
	id_index = 0
	rules = []
	trunk_color = gen_color()
	branch_color = rand.choice(BROWNS)
	
	# set up initial values that will be varied around randomly
	# trunks first
	trunk_num_min = 11
	trunk_num_max = 20
	trunk_mag = 25
	trunk_angle_min = math.pi/4
	trunk_angle_max = 3*(math.pi/4)
	# then branches
	branch_num_max = 8
	branch_num_min = 4
	branch_mag = 30
	branch_angle_min = math.pi/6
	branch_angle_max = 5*(math.pi/6)
	branch_width = 6

	# generate trunk data
	trunk_num = rand.randint(trunk_num_min,trunk_num_max)
	# need to pick length of each one .. so make it a dict with each trunk with a length and angle(0 to pi)
	for i in range(trunk_num):
		length = trunk_mag*rand.uniform(.6,1)
		angle = rand.uniform(trunk_angle_min,trunk_angle_max)
		if i == 0:
			y_start = 0
			x_start = pic_width/2

		if i != 0:
			# start at end of last
			x_start = x_end
			y_start = y_end

		x_end = x_start+length*math.cos(angle)
		y_end = y_start+length*math.sin(angle)	
		width = int(5 + 10*rand.uniform(.5,1)*(1/(1.09**i)))
		rules.append(line_piece("trunk",x_start,y_start,x_end,y_end,width,trunk_color,id_index))
		id_index = id_index + 1
	
	for trunk in rules:
		#print("TRUNK AT: ", trunk.x_start, trunk.y_start, " ", "ENDS AT: ", trunk.x_end, trunk.y_end, " ", "ID: ", trunk.identity)
		print("["+str(trunk.x_start)+",", str(trunk.y_start)+"],")
		print("["+str(trunk.x_start)+",", str(trunk.y_start)+"],")
		print("["+str(trunk.x_end)+",", str(trunk.y_end)+"],")
		print("["+str(trunk.x_end)+",", str(trunk.y_end)+"],")
		
	id_index = 0
	# choose number of main branches to add
	branch_num = rand.randint(branch_num_min,branch_num_max)
	indexes = []  #which trunks already have a branch
	# first set up a main branch
	for i in range(branch_num):
		#length = 60*rand.random()  ALSO SWITCH TO UNIFORM!
		length = branch_mag
		angle = rand.uniform(math.pi/6,5*(math.pi/6))
		# pick which trunk
		trunk_index = rand.randint(1,trunk_num)
		while (trunk_index in indexes):
			trunk_index = rand.randint(1,trunk_num)
		which_trunk = rules[trunk_index-1]
		print("TRUNK CHOSEN: ", which_trunk.identity)
		# pick where along the trunk to place the branch
		x_start = which_trunk.x_start
		y_start = which_trunk.y_start
		x_end = which_trunk.x_end
		y_end = which_trunk.y_end
		if x_end != x_start:
			slope = (y_end-y_start)/(x_end-x_start)
			b = y_start - slope*(x_start)
			branch_x_start = rand.uniform(x_end, x_start)
			branch_y_start = slope*(branch_x_start) + b
			branch_y_end = y_start+length*math.sin(angle)
			branch_x_end = x_start+length*math.cos(angle)
		elif x_end == x_start:
			r = rand.random()
			branch_x_start = x_start
			if r < .5:
				branch_x_end = x_start + length
			if r >= .5:
				branch_x_end = x_start - length
			branch_y_start = rand.uniform(y_end,y_start)
			branch_y_end = branch_y_start

		indexes.append(trunk_index)
		# then branch from that branch, necessarily shorter, up to two?
		# TEST BEFORE BRANCHING ON  BRANCHES
		#branch_split = rand.randint(0,2)
		#for j in branch_split:
		#	angle = math.pi/2*rand.random()
			# have to account for side from main branch!
		rules.append(line_piece("branch",branch_x_start,branch_y_start,branch_x_end,branch_y_end,branch_width,branch_color,id_index))
		id_index = id_index + 1
		#print("BRANCH AT: ", rules[-1].x_start,rules[-1].y_start, " ", "ENDS AT: ", rules[-1].x_end,rules[-1].y_end)
	return rules


def draw_rules(image1,draw,rules):
	for rule in rules:
		color = rule.color
		if rule.name == "branch":
			draw.line([rule.x_start,rule.y_start,rule.x_end,rule.y_end],color,rule.width)
	for rule in rules:
		color = rule.color
		if rule.name == "trunk":
			draw.line([rule.x_start,rule.y_start,rule.x_end,rule.y_end],color,rule.width)
	print("DREW TREE")
	print("")
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

	# gen rules code
	rules = gen_rules()

	# gen drawing from rules
	image1, draw = draw_rules(image1, draw, rules)
	
	# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
	#filename = "tree.png"
	image1.save(filename+".png")


for i in range(1,10):
	create_tree("tree_"+str(i))


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



