from tkinter import *
from PIL import Image, ImageDraw
import random as rand
import math
import sys


pic_width = 280
pic_height = 215
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
    def __init__(self,name,x_start,y_start,x_end,y_end,width,color,identity,used):
    	self.name = name
    	self.x_start = x_start
    	self.y_start = y_start
    	self.x_end = x_end
    	self.y_end = y_end
    	self.width = width
    	self.color = color
    	self.identity = identity
    	self.used = used


def calc_corner_diffs(trunk):
	a = trunk.x_end - trunk.x_start
	b = trunk.y_end - trunk.y_start
	d = ((trunk.width*trunk.width)/4)*(1/((b/a)**2 + 1))
	d = math.sqrt(d)
	c = -(b/a)*d
	return c,d


# for fruits and trunk, makes a color thats not too close to white (so as to appear on canvas)
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


# return list of ints that describe continuances or splits on bracnhes/trunks
def gen_split_list(leftover_trunks,reach_type):
	splits = []
	total = 0
	while total <= leftover_trunks:
		if total != 0:
			# we want more likely 1 for total less than leftover_trunks...
			# so 1/(left_over - total) goes from 1/L to ... 1 (then infin)..
			# MAKE THIS SOME HOW OPTIONAL ---> SO BRANCHES CAN BE HIGH ON TREE, FOR A TREE TYPE!!!!
			# when off, (reach_type = false) just randint(1,2) once total != 0
			# when on, (reach_type = true) more likely to continue first split before splitting again
			if total < leftover_trunks and reach_type:
				if rand.random() > .1+1/math.sqrt(leftover_trunks - total):
					addition = rand.randint(1,2)
				else:	
					addition = 1
			else:
				addition = rand.randint(1,2)
		elif total == 0:
			addition = 2
		splits.append(addition)
		total = total + addition
	return splits


# generate trunk cooordinates and line object
def gen_trunk(trunk_angle_max,trunk_angle_min,straight_type,trunk_base_width,trunk_mag,trunk_color,id_index,last_trunk,is_used=True):
	length = trunk_mag #+ 8*(1/(1.1**id_index))
	print("id_index, length: ", id_index, length)
	angle = rand.uniform(trunk_angle_min,trunk_angle_max)
	# above is naive, we want to avoid straight up mooostly, so bend distribution towards edges, using min and max
	# but, only do this is pi/2 included in range of max and min! (so we can use this func to do semi specific angle trunk)
	# turn this off for a pine tree like angle min/max
	if math.pi/2 < trunk_angle_max and math.pi/2 > trunk_angle_min and not straight_type:	
		angle_low = rand.uniform(trunk_angle_min,5*(math.pi)/12)
		angle_high = rand.uniform(7*(math.pi)/12,trunk_angle_max)
		angle = rand.choice([angle_low,angle_high])
	#first trunk always points straight up
	if id_index == 0:
		angle = math.pi/2
		y_start = 0
		x_start = pic_width/2
	if id_index != 0:
		# start at end of last
		x_start = last_trunk.x_end
		y_start = last_trunk.y_end	
	x_end = x_start+length*math.cos(angle)
	y_end = y_start+length*math.sin(angle)	
	width = int(trunk_base_width + 8*rand.uniform(.6,1)*(1/(1.07**id_index)))
	trunk = line_piece("trunk",x_start,y_start,x_end,y_end,width,trunk_color,id_index,is_used)
	return trunk


# generate branch coordinates and line object
def gen_branch(branch_mag,branch_angle_min,branch_angle_max,branch_width,which_trunk,branch_color,id_index,is_used=True):
	#length = 60*rand.random()  ALSO SWITCH TO UNIFORM!
	length = branch_mag
	angle = rand.uniform(branch_angle_min,branch_angle_max)
	# pick where along the trunk to place the branch
	# choose any x on trunk, then project along line defining trunk
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
	branch = line_piece("branch",branch_x_start,branch_y_start,branch_x_end,branch_y_end,branch_width,branch_color,id_index,is_used)
	return branch


# generate the text rules used to draw a tree png
def gen_rules(reach_type):
	id_index = 0
	rules = [None]
	trunk_color = gen_color()
	branch_color = rand.choice(BROWNS)
	# set up initial values that will be varied around randomly
	# trunks first
	trunk_num_min = 22
	trunk_num_max = 50
	trunk_mag = 20
	trunk_base_width = 2
	trunk_angle_min = 5*(math.pi)/12 #math.pi/6 #math.pi/4
	trunk_angle_max = 7*(math.pi)/12 #5*(math.pi/6) #3*(math.pi/4)
	repeat_prob = .2						#DONT FORGET THIS!
	trunk_split_prob = .02	# probability to split once minimum trunks generated met
	trunk_split_factor = 6  # what ratio of trunks need to be met to start splitting (so 2 means 1/2)
	#reach_type = True # set to true if you want to split branches more than spread higher
	reach_type = reach_type
	straight_type = True
	# now branch settings
	branch_num_max = 8
	branch_num_min = 4
	branch_mag = 30
	branch_angle_min = math.pi/6
	branch_angle_max = 5*(math.pi/6)
	branch_width = 3
	# IN MAKING SETS MAY NEED TO ADJUST MAG AND MAG SCALING TO NOT GO OUT OF BOUNDS!

	# generate trunk data
	# first pick number of trunks in whole tree
	trunk_num = rand.randint(trunk_num_min,trunk_num_max)
	for i in range(trunk_num):
		# decide if splitting --> far enough along and rand chance
		if id_index > int(trunk_num/trunk_split_factor) and rand.random() > trunk_split_prob:
			break
		trunk = gen_trunk(trunk_angle_max,trunk_angle_min,straight_type,trunk_base_width,trunk_mag,trunk_color,id_index,rules[-1])
		rules.append(trunk)
		id_index = id_index + 1
	# now generate splits and fill with remaining trunks
	# possible num_splits = rand.randint(1,int((trunk_num-i)/2))
	# generate list of branch structure like 1,2,1.. place randomly
	rules.pop(0)
	split_list = gen_split_list(trunk_num-i,reach_type)
	chosen_trunk = rules[-1]
	for k in range(len(split_list)):
		if split_list[k] == 1:
			chosen_trunk.used = True
			trunk = gen_trunk(math.pi/(1.1),0,False,trunk_base_width,trunk_mag,trunk_color,id_index,chosen_trunk,False)
			rules.append(trunk)
			id_index = id_index + 1 
		if split_list[k] == 2:
			chosen_trunk.used = True
			trunk_r = gen_trunk(math.pi/8.0 + rand.uniform(0,.4),math.pi/8.0 - rand.uniform(0,.3),False,trunk_base_width,trunk_mag,trunk_color,id_index,chosen_trunk,False)
			id_index = id_index + 1
			trunk_l = gen_trunk(7*math.pi/8.0 + rand.uniform(0,.3),7*math.pi/8.0 - rand.uniform(0,.4),False,trunk_base_width,trunk_mag,trunk_color,id_index,chosen_trunk,False)
			rules.append(trunk_l)
			rules.append(trunk_r)
			id_index = id_index + 1
		unused_trunks = []
		for try_trunk in rules:
			if try_trunk.used == False:
				unused_trunks.append(try_trunk)
		chosen_trunk = rand.choice(unused_trunks)

	id_index = 0
	# choose number of main branches to add
	branch_num = rand.randint(branch_num_min,branch_num_max)
	indexes = []  #which trunks already have a branch
	# first set up a main branch
	for i in range(branch_num):
		# pick which trunk
		trunk_index = rand.randint(1,trunk_num)
		while (trunk_index in indexes):
			trunk_index = rand.randint(1,trunk_num)
		which_trunk = rules[trunk_index-1]
		indexes.append(trunk_index)
		# generate a branch
		branch = gen_branch(branch_mag,branch_angle_min,branch_angle_max,branch_width,which_trunk,branch_color,id_index)
		rules.append(branch)
		id_index = id_index + 1
	return rules


# given the list of line objects to draw, do so, in the right order and adding corner fills
def draw_rules(image1,draw,rules):
	for i in range(len(rules)):
		rule = rules[i]
		color = rule.color
		if rule.name == "trunk":
			draw.line([rule.x_start,rule.y_start,rule.x_end,rule.y_end],color,rule.width)
			# now also try filling gaps!
			# for a trunk-trunk pair, get correct corners and construct filling polygon
			if i != len(rules)-1: #so we are not on the last rule
				if rules[i+1].name  == "trunk": # if we are not on the last trunk (only doing pairs!!)
					# can calc corners here
					p1 = [rule.x_end,rule.y_end]
					if i != 0:
						c,d = calc_corner_diffs(rule)
					if i == 0:
						c = -rule.width/2
						d = 0
					if rules[i+1].x_end < rule.x_end:
						c = abs(c)
					if rules[i+1].x_end > rule.x_end:
						c = -abs(c)
					d = -abs(d)
					g,h = calc_corner_diffs(rules[i+1])
					p2 = [p1[0]+c,p1[1]+d]
					p3 = [p1[0]+g,p1[1]+h]
					draw.polygon([p1[0],p1[1],p2[0],p2[1],p3[0],p3[1]],fill=rule.color,outline=None)

	# split drawing trunks and branches to make sure branches are underneath trunks
	#for i in range(len(rules)):
	#	rule = rules[i]
	#	color = rule.color
	#	if rule.name == "branch":
	#		draw.line([rule.x_start,rule.y_start,rule.x_end,rule.y_end],color,rule.width)

	return image1,draw


def create_tree(filename,reach_type):
	# AUTO DRAW CODE THAT CREATES AND SAVES PNG 
	# PIL create an empty image and draw object to draw on
	# memory only, not visible
	image1 = Image.new("RGB", (pic_width, pic_height), white)
	draw = ImageDraw.Draw(image1)

	# gen rules code
	rules = gen_rules(reach_type)

	# gen drawing from rules
	image1, draw = draw_rules(image1, draw, rules)

	image1 = image1.rotate(180, Image.NEAREST, expand = 1)
	
	# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
	#filename = "tree.png"
	image1.save(filename+".png")


create_tree("tree_1",False)
create_tree("tree_true2",True)
create_tree("tree_true3",True)
create_tree("tree_false1",False)
create_tree("tree_false2",False)
create_tree("tree_false3",False)
