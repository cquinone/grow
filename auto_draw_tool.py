from tkinter import *
from PIL import Image, ImageDraw
import random as rand
import math


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
    def __init__(self,name,x_start,y_start,x_end,y_end,color):
    	self.name = name
    	self.x_start = x_start
    	self.y_start = y_start
    	self.x_end = x_end
    	self.y_end = y_end
    	self.color = color


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
	rules = []
	trunk_color = gen_color()
	branch_color = rand.choice(BROWNS)

	# generate trunk data
	trunk_num = rand.randint(4,10)
	# need to pick length of each one .. so make it a dict with each trunk with a length and angle(0 to pi)
	for i in range(trunk_num):
		length = 9*rand.uniform(.5,1)
		if i == 0:
			# start at center of width for first one, stright up angle
			angle = math.pi/2
			y_start = 0
			x_start = pic_width/2

		if i != 0:
			# start at end of last
			angle = rand.uniform(math.pi/4,3*(math.pi/4))
			x_start = x_end
			y_start = y_end

		x_end = x_start+length*math.cos(angle)
		y_end = y_start+length*math.sin(angle)
		rules.append(line_piece("trunk",x_start,y_start,x_end,y_end,trunk_color))
	
	for trunk in rules:
		print("x_start: ", trunk.x_start)
		print("x_end: ", trunk.x_end)

	# choose number of main branches to add
	branch_num = rand.randint(2,5)
	# first set up a main branch
	for i in range(branch_num):
		length = 4*rand.random()
		angle = rand.uniform(math.pi/6,5*(math.pi/6))
		# pick which trunk
		trunk_index = rand.randint(1,trunk_num)
		which_trunk = rules[trunk_index-1]
		# pick where along the trunk to place the branch
		x_start = which_trunk.x_start
		y_start = which_trunk.y_start
		x_end = which_trunk.x_end
		y_end = which_trunk.y_end
		if x_end != x_start:
			slope = (y_end-y_start)/(x_end-x_start)
			b = y_start - slope*(x_start)
			branch_x_start = rand.random()*(x_end-x_start)
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
			branch_y_start = rand.random()*(y_end-y_start)
			branch_y_end = branch_y_start

		# then branch from that branch, necessarily shorter, up to two?
		# TEST BEFORE BRANCHING ON  BRANCHES
		#branch_split = rand.randint(0,2)
		#for j in branch_split:
		#	angle = math.pi/2*rand.random()
			# have to account for side from main branch!
		rules.append(line_piece("branch",branch_x_start,branch_y_start,branch_x_end,branch_y_end,branch_color))

	## pick num of branches
	#branch_num = rand.randint(2,5)

	## gen list of branches, each with a lnnegth, angle, position, breakdown
	#branches = gen_branches(branch_num) 
	return rules


def draw_rules(image1,draw,rules):
	for rule in rules:
		color = rule.color
		if rule.name == "trunk":
			draw.line([rule.x_start,rule.y_start,rule.x_end,rule.y_end],color,width=5)
		if rule.name == "branch":
			draw.line([rule.x_start,rule.y_start,rule.x_end,rule.y_end],color,width=1)

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


create_tree("test_tree")


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



