# -*- coding: utf-8 -*-

import pygame as pg
#import auto_draw_tool as auto_draw
import time
import math
import sys

# constants / images / fonts
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY  = (228,228,228)
BLUE = (0, 237, 250)
GREEN = (34,139,34)
WIDTH = 840
HEIGHT = 680


class Level():
    def __init__(self):
        self.fruit = 0
        self.day = 0
        self.owned_plants = []
        self.items = []
        self.plant = None

class Plant():
    def __init__(self,name, img):
        self.name = name
        self.stage = 0
        self.hydration = 3
        self.sun = 3
        self.prune = 0
        self.old_stage = "seed"
        self.img = img

    def evo_check(self, stage_dict, img_dict):
        draw("text", "Performing evoluton check...", [8,66])
        pg.time.wait(1100)
        sorted_keys = sorted(stage_dict.keys())
        for key in sorted_keys:
            if self.stage >= key:
                self.curr_stage = stage_dict[key]
       
        if self.old_stage != self.curr_stage:
            self.old_stage = self.curr_stage
            self.img = img_dict[self.curr_stage]
            # print that it did too, add in wait
            draw("text", curr_level.plant.name+" evolved!", [8,86])
            pg.time.wait(1100)
            draw("text", "It is now in the "+self.curr_stage+" stage!",[8,93],"midfont")
            pg.time.wait(1100)
        else:
            # need to write that plant name did not evolve
            draw("text", curr_level.plant.name+" did not evolve.", [8,83])
            pg.time.wait(700)


# general draw function for images and text
def draw(type,rsp,pos, fonttype="font", color=pg.Color('SALMON')):
    y = pos[1]
    x = pos[0]
    if type == "text":
        if fonttype == "font":
            rsp_surface = font.render(rsp, True, color)
            text_w , text_h = font.size(rsp)
        if fonttype == "bigfont":
            rsp_surface = big_reg_font.render(rsp, True, color)
            text_w , text_h = bigfont.size(rsp)
        if fonttype == "midfont":
            rsp_surface = midfont.render(rsp, True, color)
            text_w , text_h = midfont.size(rsp)
        screen.blit(rsp_surface, (input_box.x+x, input_box.y+y))
        pg.display.update(pg.Rect(input_box.x+x, input_box.y+y, text_w, text_h))
   
    if type == "img":
        screen.blit(rsp,pos)
        img_w,img_h = rsp.get_size()
        pg.display.update(pg.Rect(x,y, img_w, img_h))

    # pump events so drawing works?
    pg.event.pump()


# extra function to determine action from click on store
def store_check(event):
    option = ""
    # if click on "exit"
    if event.pos[0] >= 31 and event.pos[0] <= 152:
        if event.pos[1] >= 594 and event.pos[1] <= 652:
            option = "exit"
    # if click on first item = propane
    if event.pos[0] >= 189 and event.pos[0] <= 314:
        if event.pos[1] >= 25 and event.pos[1] <= 136:
            option = "propane"

    return option

# response function takes cmd, level (which contains screen data / plant data) and responds to given command with drawing
# and stats update
def response(cmd, curr_level, stage_dict, img_dict):
    # assume doing something that needs FULL clearing
    not_clear = False

    # track day changes
    old_day  = curr_level.day

    # block input during responses
    pg.event.set_blocked(pg.KEYDOWN)
    
    possible_cmd_list =  ["help","hlp","water","rain", "sun", "sunbathe","prune","inventory","store","quit","q","switch plant", "cross"]
    help_cmds = ["Commands: ", "help","water","sunbathe","prune","inventory","store","quit","switch plant","cross"]

    # calc current constants for plant (depends on plant stage), max out at 20 and 10
    max_hydration = 6+float(max((curr_level.plant.stage-20)/(1.3),0)) 
    max_sun = 11+float(max((curr_level.plant.stage-20)/(1.3),0))
    if max_sun > 20:
        max_sun = 20
    if max_hydration > 10:
        max_hydration = 10
    
    # grab current day count
    old_day = curr_level.day

    if cmd == "help" or cmd == "hlp":
        text_vert = 5
        # insert extra print element, blit all cmds
        for i in range(len(help_cmds)):
            rsp = help_cmds[i]
            if rsp != "Commands: ":
                rsp = "- " + rsp
            draw("text",rsp,[8,text_vert])
            text_vert = text_vert+20

        # delay after message end, then clear
        pg.time.wait(2200)
        pg.draw.rect(screen, WHITE, (input_box.x+8,input_box.y+5,input_box.x+8+250,input_box.y+5+60))
        pg.display.update(pg.Rect(input_box.x+8,input_box.y+5,input_box.x+8+250,input_box.y+5+60))      # magic numbers for full command list
        not_clear = True

    if cmd == "q" or cmd == "quit":
        click = False
        draw("img", quit_ask, [100,120])
        while not click:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                # clicks are still allowed in response function, dont stop loop if click not on boxes
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # if click on "SI"
                    if event.pos[0] >= 200 and event.pos[0] <= 325:
                        if event.pos[1] >= 235 and event.pos[1] <= 301:
                            sys.exit()
                    # if click on "NO"
                    if event.pos[0] >= 387 and event.pos[0] <= 503:
                        if event.pos[1] >= 235 and event.pos[1] <= 301:
                            click = True

    if cmd == "water" or cmd == "rain":
        curr_level.day = curr_level.day + 1
        curr_level.plant.hydration = curr_level.plant.hydration + 2
        exp_stage = 5.0*(1.0/math.exp(max_hydration-curr_level.plant.hydration))  # 5 is chosen constant
        curr_level.plant.stage = curr_level.plant.stage + max(exp_stage,1.0)
        
        # draw message and cloud at same time
        draw("text", "Rain clouds darken the sky.", [8,5])
        draw("img",rain, [540,-50])
        pg.time.wait(500)
        #now animate rain
        draw("img", drop, [580,160])
        draw("img", drop, [660, 160])
        pg.time.wait(500)
        draw("img", drop_cover, [580,160])
        draw("img", drop_cover, [660,160])
        pg.time.wait(500)
        draw("img", drop, [640,190])
        draw("img", drop, [720, 190])
        pg.time.wait(500)
        draw("img", drop_cover, [640,190])
        draw("img", drop_cover, [720, 190])
        pg.time.wait(800)              

    if cmd == "sun" or cmd == "sunbathe":
        curr_level.day = curr_level.day + 1
        curr_level.plant.sun = curr_level.plant.sun + 4
        exp_stage = 12.0*(1.0/math.exp(max_sun-curr_level.plant.sun))  # 12 is chosen constant
        curr_level.plant.stage = curr_level.plant.stage + max(exp_stage,1.0)
        curr_level.plant.hydration = curr_level.plant.hydration - .5
        
        # real animation loop?
        # gen items, locations
        # loop thruogh time... if certain time reach, drop from draw list...
        # but previous draw will remain! ... need to update square AROUND item...
        # so capture bounding rect of item..
        # keep rays and rain above box?.. could have bounce effect later on.. last so exact corrds worked out

        # draw message and sun at same time
        draw("text", "The sun is high in the sky.", [8,5])
        draw("img",sun, [560,-100])
        pg.time.wait(500)
        #now animate sun
        draw("img", ray, [610,175])
        draw("img", ray, [660, 175])
        pg.time.wait(500)
        draw("img", ray_cover, [610,175])
        draw("img", ray_cover, [660,175])
        pg.time.wait(500)
        draw("img", ray, [640,190])
        draw("img", ray, [690, 190])
        pg.time.wait(500)
        draw("img", ray_cover, [640,190])
        draw("img", ray_cover, [690, 190])
        pg.time.wait(800)

    if cmd == "store":
        click = False
        draw("img", store, [0,0])
        # wait for option.. include exit button!
        while not click:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                # clicks are still allowed in response function, dont stop loop if click not on boxes
                elif event.type == pg.MOUSEBUTTONDOWN:
                    option = store_check(event)
                    if option == "exit":
                        click = True
                    elif option == "propane":
                        pg.time.wait(500)
                        draw("img", textbox, [200,150])
                        draw("text", "Added Propane to inventory!", [220,80], fonttype="bigfont")
                        pg.time.wait(2000)
                        click = True

    if cmd not in possible_cmd_list:
        rsp =  cmd+" is not an available command"        
        draw("text",rsp,[8,5])
        pg.time.wait(2000)
        text_w , text_h = font.size(rsp)
        pg.draw.rect(screen, WHITE, (input_box.x+8,input_box.y+5,input_box.x+text_w,input_box.y+text_h))
        pg.display.update(pg.Rect(input_box.x+8,input_box.y+5,input_box.x+8+text_w,input_box.y+5+text_h))
        not_clear = True

    # day has gone by, update plants and print day end message if a day has gone by
    if old_day < curr_level.day:
        draw("img", cover, [input_box.x,input_box.y])
        draw("text", "Another day passes.", [8,5])
        pg.time.wait(1100)
        draw("text", "Each of your plants decays.", [8,22])
        pg.time.wait(1100)
        draw("text", "Don't forget to check on them!",[8,39]) 
        pg.time.wait(1100)
        # if day has passed, we want to check for plant evolve and change plant img accordingly
        curr_level.plant.evo_check(stage_dict, img_dict) 

    # now re-allow input as repsonse is over
    pg.event.set_allowed(pg.KEYDOWN)
    # Blit background image first (so below everything else), this is also serving as the "clear" everything function
    if not not_clear:	
    	screen.blit(background, [0,0])
    	pg.display.update()

    return old_day < curr_level.day


# test auto_draw
#auto_draw.create_tree('first_tree')
pg.init()
pg.display.set_caption('seed game')
screen = pg.display.set_mode((WIDTH, HEIGHT))
font = pg.font.SysFont("couriernew", 16, bold=True)
bigfont = pg.font.SysFont("cochin", 24, bold=True)
big_reg_font = pg.font.SysFont("couriernew", 20)
copyfont = pg.font.SysFont("georgia", 12, bold=True)
midfont = pg.font.SysFont("couriernew", 15, bold=True)
clock = pg.time.Clock()
input_box = pg.Rect(60, 130, 300, 32)
cursor_box = pg.Rect(60,135, 10, 20)
cursor_timer = 0
cmd_color = pg.Color('SALMON')
done = False
cmd = ""
intro = True
intro_timer = 0
info_timer = 0
name_scr = False
copyright = copyfont.render("Property of  YaboiCQ games  "+u"\u2122"+", 2019, all rights reserved "+u"\u00AE", True, GREEN)

# images
intro = pg.image.load("pics/intro.png").convert_alpha()
intro = pg.transform.scale(intro, [int(.5*1678), int(.5*1358)])
info = pg.image.load("pics/infocopy.png").convert_alpha()
info = pg.transform.scale(info, [int(.5*1678), int(.5*1358)])
name_pic = pg.image.load("pics/name_scr.png").convert_alpha()
name_pic = pg.transform.scale(name_pic, [int(.5*1678), int(.5*1358)])
background = pg.image.load("pics/back_box_copy.png").convert_alpha()
background = pg.transform.scale(background, [WIDTH,HEIGHT])
back_nobox = pg.image.load("pics/background.png").convert_alpha()
back_nobox = pg.transform.scale(back_nobox, [WIDTH,HEIGHT])
cover = pg.image.load("pics/cover.png").convert_alpha()
cover = pg.transform.scale(cover, [int(.8*490),int(600)])
rain = pg.image.load("pics/cloud.png").convert_alpha()
rain = pg.transform.scale(rain, [int(.5*390), int(.5*198)])   # dimension nums based on image size
drop = pg.image.load("pics/drop.png").convert_alpha()
drop_cover = pg.image.load("pics/drop_cover.png").convert_alpha()
sun  = pg.image.load("pics/sun2.png").convert_alpha()
sun = pg.transform.scale(sun, [int(.72*252), int(.72*252)])
ray = pg.image.load("pics/ray.png").convert_alpha()
ray_cover = pg.image.load("pics/ray_cover.png").convert_alpha()
#seed = pg.image.load("pics/seed.png").convert_alpha()
seed = pg.image.load("tree_1.png").convert_alpha()
#seed = pg.transform.scale(seed, [int(1.2*380),int(1.2*300)])
#seed = pg.transform.scale(seed, [int(.6*99),int(.6*126)])
quit_ask = pg.image.load("pics/test_ask.png").convert_alpha()
store = pg.image.load("pics/store_test.png").convert_alpha()
textbox = pg.image.load("pics/textbox_copy.png").convert_alpha()
#tree_img = pg.image.load("first_tree.png").convert_alpha()
bud = sun # for now, use sun as next evo pic
img_dict = {"seed": seed, "bud": bud}


#timer buffers
first_screen_buffer = 20
second_screen_buffer = 35

#first draw check?
pg.display.update()

# set up first plant, set as plant in focus
first_plant = Plant("",seed)
plant_disp_x = 480  # coords for basic plant display
plant_disp_y = 190

#initial values
curr_level = Level()
curr_level.plant = first_plant
curr_level.owned_plants.append(first_plant)

#stage settings
stage_dict = {0: "seed", 19: "bud", 29: "sapling", 49: "super sapling", 79: "tree"}

#do one update, to start it off
pg.display.update()

#track if FIRST time at main game screen
response_start = False

while not done:
    enter = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if len(cmd) >= 30:
                cmd = ""
            if event.key == pg.K_RETURN:
                enter = True
            elif event.key == pg.K_BACKSPACE:
                enter = False
                cmd = cmd[:-1]
            else:
                enter = False
                cmd += event.unicode

    # Render current command            
    cmd_surface = font.render(cmd, True, cmd_color)

    # once past intro screen and naming first plant
    if not intro and not name_scr:
        day_change = False
        # if this is the first time you're here, reset screen
        if response_start == False:
            screen.blit(background, [0,0])
            screen.blit(curr_level.plant.img, (plant_disp_x, plant_disp_y))
            day_surface = font.render("DAY: "+str(curr_level.day), True, BLACK)
            screen.blit(day_surface, (92, 60))
            pg.display.update()
            response_start = True

        if enter == True:  # if command has been entered by pressing enter?
            cover_box = pg.Rect(input_box.x, input_box.y, cmd_surface.get_width()+40, cmd_surface.get_height()+10)
            pg.draw.rect(screen, WHITE, cover_box)
            pg.display.update(cover_box)
            # pump events so drawing works?
            pg.event.pump()
            day_change = response(cmd, curr_level, stage_dict, img_dict)
            cmd  = ""
            #  now that enter has been pressed and a response drawn and then cleared, need to redraw plant and day!
            # Blit Day counter, render only if day has changed or not rendered yet
            if day_change:
                day_surface = font.render("DAY: "+str(curr_level.day), True, BLACK)

            screen.blit(day_surface, (92, 60))
            text_w , text_h = font.size("DAY: "+str(curr_level.day))
            pg.display.update(pg.Rect(92, 60, text_w, text_h))
        	# Blit plant again!
            draw("img", curr_level.plant.img, [plant_disp_x,plant_disp_y])

        # Blit command as it's being typed
        if not enter:
            text_w , text_h = font.size(cmd)
            pg.draw.rect(screen,WHITE,(input_box.x+5, input_box.y+5, text_w+40, text_h))
            screen.blit(cmd_surface, (input_box.x+5, input_box.y+5))
            #update cursor position
            old_x = cursor_box.x
            cursor_box.x = cursor_box.x + text_w+5
            # Blit the cursor depending on flicker
            if cursor_timer < 8:
                pg.draw.rect(screen, BLUE, cursor_box)
                cursor_timer = cursor_timer + 1
            else:
                cursor_timer = cursor_timer + 1
                pg.draw.rect(screen, WHITE, cursor_box)
                if cursor_timer > 16:       #basically saying: dont draw for X frames, makes flicker effect
                    cursor_timer = 0  
            pg.display.update(pg.Rect(input_box.x+5, input_box.y+5, text_w+40, text_h))  
            # reset position
            cursor_box.x = old_x

    # on the intro screen, not yet to naming
    if intro and not name_scr:
        if intro_timer <= first_screen_buffer:
            # if on intro page
            screen.fill(GRAY)
            screen.blit(intro, [0,0])
            screen.blit(copyright, (225,595)) 
            pg.display.update()
            # pump events so drawing works?
            pg.event.pump()
            intro_timer = intro_timer + 1
        else:
            screen.fill(GRAY)
            screen.blit(info, [0,0])
            pg.display.update()
            info_timer = info_timer + 1
            if info_timer > second_screen_buffer:
                intro = False
                name_scr = True
                screen.blit(name_pic, [0,0])
                pg.display.update()

    if name_scr and not intro:
        #screen.fill(WHITE)
        text_w , text_h = font.size(cmd)
        
        # only blit new cmds if still naming plant, and only reset cursor if no name
        if curr_level.plant.name == "":
            screen.blit(cmd_surface, (input_box.x+5, input_box.y+5))
            # update cursor position and save
            old_x = cursor_box.x
            cursor_box.x = cursor_box.x + text_w+5
            # Blit the cursor depending on flicker
            if cursor_timer < 8:
                pg.draw.rect(screen, BLUE, cursor_box)
                cursor_timer = cursor_timer + 1
            else:
                cursor_timer = cursor_timer + 1
                if cursor_timer > 16:       #basically saying: dont draw for X frames, makes flicker effect
                    cursor_timer = 0  
            pg.display.update(pg.Rect(input_box.x+5, input_box.y+5, text_w+40, text_h))  
            # reset position
            cursor_box.x = old_x
            screen.blit(back_nobox, [0,0])

        else:
            # once named, blit name, then announcements
            name_surface = font.render(curr_level.plant.name, True, cmd_color)
            screen.blit(name_pic, [0,0])
            screen.blit(name_surface, (input_box.x+5, input_box.y+5))
            draw("img", curr_level.plant.img, [plant_disp_x,plant_disp_y])
            draw("text", curr_level.plant.name+" was planted!", [402,-30], color=GREEN)
            pg.display.update()
            pg.time.wait(1100)
            draw("text", "Treat it well!", [402,-10], color=GREEN)
            pg.time.wait(1700)
            name_scr = False
        
        if enter and cmd != "":
            # grab name once enter is pressed
            curr_level.plant.name = cmd
            cmd = ""
    
    clock.tick(60)