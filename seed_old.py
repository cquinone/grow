# -*- coding: utf-8 -*-

import pygame as pg
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
    def __init__(self,name):
        self.name = name
        self.stage = 0
        self.hydration = 3
        self.sun = 3
        self.prune = 0
        self.old_stage = "seed"

# general draw function for images and text
# wraps up event queue bug thing and updating screen
def draw(type,rsp,pos, color=pg.Color('SALMON')):
    y = pos[1]
    x = pos[0]
    if type == "text":
        rsp_surface = font.render(rsp, True, color)
        screen.blit(rsp_surface, (input_box.x+x, input_box.y+y))
        text_w , text_h = font.size(rsp)
        #pg.draw.rect(screen, BLACK, pg.Rect(input_box.x+x, input_box.y+y, text_w+40, text_h))
        pg.display.update(pg.Rect(input_box.x+x, input_box.y+y, text_w+40, text_h))
   
    if type == "img":
        screen.blit(rsp,pos)
        img_w,img_h = rsp.get_size()
        pg.display.update(pg.Rect(x,y, img_w, img_h))  

    # need this event queue becuase of pygame bugs
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

# response function takes cmd, level (which contains screen data / plant data) and responds to given command with drawing
# and stats update
def response(cmd, curr_level):
    possible_cmd_list =  ["help","hlp","water","rain", "sun", "sunbathe","prune","item","store","clear","quit","q","switch plant", "cross"]
    help_cmds = ["Commands: ", "help","water","sunbathe","prune","item","store","quit","switch plant","cross"]

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

        # delay after message end, before bkg clearing happens
        pg.time.wait(2200)

    if cmd == "q" or cmd == "quit":
        sys.exit()

    if cmd == "water" or cmd == "rain":
        curr_level.day = curr_level.day + 1
        curr_level.plant.hydration = curr_level.plant.hydration + 2
        exp_stage = 5.0*(1.0/math.exp(max_hydration-curr_level.plant.hydration))  # 5 is chosen constant
        curr_level.plant.stage = curr_level.plant.stage + max(exp_stage,1.0)
        
        # draw message and cloud at same time
        draw("text", "Rain clouds darken the sky.", [8,5])
        draw("img",rain, [560,80])
        pg.time.wait(2000)

    if cmd == "sun" or cmd == "sunbathe":
        curr_level.day = curr_level.day + 1
        curr_level.plant.sun = curr_level.plant.sun + 4
        exp_stage = 12.0*(1.0/math.exp(max_sun-curr_level.plant.sun))  # 12 is chosen constant
        curr_level.plant.stage = curr_level.plant.stage + max(exp_stage,1.0)
        curr_level.plant.hydration = curr_level.plant.hydration - .5
        
        # draw message and sun at same time
        draw("text", "The sun is high in the sky.", [8,5])
        draw("img",sun, [560,20])
        pg.time.wait(2000)

    if cmd not in possible_cmd_list:
        rsp =  cmd+" is not an available command"        
        draw("text",rsp,[8,5])
        pg.time.wait(2000)

    # day has gone by, update plants and print day end message
    if old_day < curr_level.day:
        draw("img", cover, [input_box.x,input_box.y])
        draw("text", "Another day passes.", [8,5])
        pg.time.wait(1100)
        draw("text", "Each of your plants loses one water and one sun.", [8,22])
        pg.time.wait(1100)
        draw("text", "Don't forget to check each!",[8,39]) 
        pg.time.wait(2200)
        # should you update just curr plant, or all? slow on all, faster on focus?
        # note: to differentiate, possibly outlaw naming two plants same name
        # if name in names of others, reject, ask again
        # then in doing end of day updates, update plants in owned plants that are not main name slowly


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
font = pg.font.SysFont("couriernew", 16, bold=True)
bigfont = pg.font.SysFont("cochin", 24, bold=True)
littlefont = pg.font.SysFont("georgia", 12, bold=True)
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
copyright = littlefont.render("Property of  YaboiCQ games  "+u"\u2122"+", 2019, all rights reserved "+u"\u00AE", True, GREEN)

# images
intro = pg.image.load("pics/intro.png").convert_alpha()
intro = pg.transform.scale(intro, [int(.5*1678), int(.5*1358)])
info = pg.image.load("pics/info.png").convert_alpha()
info = pg.transform.scale(info, [int(.5*1678), int(.5*1358)])
name_pic = pg.image.load("pics/name_scr.png").convert_alpha()
name_pic = pg.transform.scale(name_pic, [int(.5*1678), int(.5*1358)])
background = pg.image.load("pics/mockup.png").convert_alpha()
background = pg.transform.scale(background, [WIDTH,HEIGHT])
cover = pg.image.load("pics/cover.png").convert_alpha()
cover = pg.transform.scale(cover, [490,600])
rain = pg.image.load("pics/cloud.png").convert_alpha()
rain = pg.transform.scale(rain, [int(.5*390), int(.5*198)])   # dimension nums based on image size
sun  = pg.image.load("pics/sun2.png").convert_alpha()
sun = pg.transform.scale(sun, [int(.72*252), int(.72*252)])

#first draw check?
pg.display.update()

# set up first plant, set as plant in focus
first_plant = Plant("")

#initial values
curr_level = Level()
curr_level.plant = first_plant
curr_level.owned_plants.append(first_plant)

#do one update, to start it off
pg.display.update()

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
        if enter == True:  # if command has been entered by pressing enter?
            cover_box = pg.Rect(input_box.x, input_box.y, cmd_surface.get_width()+40, cmd_surface.get_height()+10)
            pg.draw.rect(screen, WHITE, cover_box)
            pg.display.update(cover_box)
            # need this event queue becuase of pygame bugs
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            response(cmd, curr_level)
            cmd  = ""
                 
        # Blit background image first (so below everything else), this is also serving as the "clear" everything function
        screen.blit(background, [0,0])
    
        # Blit Day counter
        day_surface = font.render("DAY: "+str(curr_level.day), True, BLACK)
        screen.blit(day_surface, (92, 60))
        text_w , text_h = font.size("DAY: "+str(curr_level.day))
        pg.display.update(pg.Rect(92, 60, text_w, text_h))
        
        # Blit command as it's being typed
        if not enter:
            text_w , text_h = font.size(cmd)
            screen.blit(cmd_surface, (input_box.x+5, input_box.y+5))
            #update cursor position
            old_x = cursor_box.x
            cursor_box.x = cursor_box.x + text_w+5
            # Blit the cursor if on non-flicker
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

    # on the intro screen, not yet to naming
    if intro and not name_scr:
        if intro_timer <= 100:
            # if on intro page
            screen.fill(GRAY)
            screen.blit(intro, [0,0])
            screen.blit(copyright, (225,595)) 
            pg.display.update()
            # need this event queue becuase of pygame bugs
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            intro_timer = intro_timer + 1
        else:
            screen.fill(GRAY)
            screen.blit(info, [0,0])
            pg.display.update()
            info_timer = info_timer + 1
            if info_timer > 200:
                intro = False
                name_scr = True

    if name_scr and not intro:
        screen.blit(name_pic, [0,0])
        text_w , text_h = font.size(cmd)
        
        # only blit new cmds if still naming plant, and only reset cursor if no name
        if curr_level.plant.name == "":
            screen.blit(cmd_surface, (input_box.x+5, input_box.y+5))
            # update cursor position and save
            old_x = cursor_box.x
            cursor_box.x = cursor_box.x + text_w+5
            # Blit the cursor if on non-flicker
            if cursor_timer < 8:
                pg.draw.rect(screen, BLUE, cursor_box)
                cursor_timer = cursor_timer + 1
            if cursor_timer >= 8:
                cursor_timer = cursor_timer + 1
                if cursor_timer > 16:           #basically saying: dont draw for X frames, makes flicker effect
                    cursor_timer = 0  
            pg.display.update(pg.Rect(input_box.x+5, input_box.y+5, text_w+5, text_h))  
            # reset position
            cursor_box.x = old_x
        else:
            # once named, blit name, then announcements
            name_surface = font.render(curr_level.plant.name, True, cmd_color)
            screen.blit(name_surface, (input_box.x+5, input_box.y+5))
            draw("text", curr_level.plant.name+" was planted:", [510,-10], GREEN)
            pg.time.wait(1100)
            draw("text", "Treat it well!", [510,200], GREEN)
            pg.time.wait(1700)
            name_scr = False
        
        if enter and cmd != "":
            # grab name once enter is pressed
            curr_level.plant.name = cmd
            cmd = ""
    
    clock.tick(60)
