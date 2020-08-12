import pygame
from pygame.locals import *
import sys, os
import time
import math

BOARDWIDTH = 19
BOARDHEIGHT = 19
#DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#print(pygame.display.get_surface())
DISPLAYSURF = pygame.display.set_mode(flags=pygame.RESIZABLE)
#my computer is 1366 by 768 (except for bar at top: it is 705 with this bar)
WINDOWWIDTH = pygame.Surface.get_size(DISPLAYSURF)[0]
WINDOWHEIGHT = pygame.Surface.get_size(DISPLAYSURF)[1] - 63 #subtract 63 to account for taskbar
SPACESIZE = max(20, int(min(WINDOWWIDTH, WINDOWHEIGHT) / 24)) #pixels in one space; adjusted to screen size, no smaller than 20
OUTERSURF = 2 #SPACESIZE lengths between board and outer area
DRAWINGLENGTH = SPACESIZE * 2 #length the user may draw in a turn
EPSILON = 0.1 #drawing length margin of error
XMARGIN = int((WINDOWWIDTH - ((BOARDWIDTH - 1) * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - ((BOARDHEIGHT - 1) * SPACESIZE)) / 2)
INTERSECTDIST = 1.95 #closest distance a player's line can come within contacting the other player's lines
#INTERSECTDIST = 5 #temp

MAXMAGNET = 10 #magnet ranges from 0 through MAXMAGNET
SLIDERLEFT = 50 #location of left of slider
SLIDERRIGHT = SLIDERLEFT + MAXMAGNET * 13 #location of right of slider
SLIDERDIVISION = (SLIDERRIGHT - SLIDERLEFT) / MAXMAGNET #divides slider into sections to show location of circle
CLICKDIVISION = (SLIDERRIGHT - SLIDERLEFT) / (MAXMAGNET + 1) #divides slider into sections to process mouse click
SLIDERHEIGHT = WINDOWHEIGHT - 250
SLIDERRECT = pygame.Rect(SLIDERLEFT, SLIDERHEIGHT, SLIDERRIGHT - SLIDERLEFT, 12) #slider rectangle

#                         R    G    B
BLACK     = pygame.Color( 0 ,  0 ,  0 )
WHITE     = pygame.Color(255, 255, 255)
TAN       = pygame.Color(227, 195, 122)
GRAY      = pygame.Color(128, 128, 128)
GRAYALPHA = pygame.Color(128, 128, 128, 100)
RED       = pygame.Color(255,  0 ,  0 )
GREEN     = pygame.Color( 0 , 255,  0 )
LIGHTGRAY = pygame.Color(200, 200, 200)

TEXTCOLOR = WHITE
BGCOLOR = TAN #background color of board and surface surrounding board
OUTERBGCOLOR = GRAY #background color of area surrounding surface, consider changing
GRIDLINECOLOR = GRAYALPHA
DRAWCOLOR = RED #color of potential lines and dots indicating click
SLIDERCOLOR = LIGHTGRAY
SLIDERCIRCLECOLOR = GREEN

def main():
    COUNT = 0 #temp
    changed = False #variable to keep track of whether the program has artificially adjusted the mouse's position
    adjustedPos = (-4 * SPACESIZE, -4 * SPACESIZE) #position of this artificial adjustment; initially set to a place off the board
    potentialLine = False #variable to keep track of whether a potential line is currently being drawn
    potentialOffBoard = None #special case variable to identify when a potential line starts off board
    magnetDist = 4 #initial magnet strength value
    cutOffBreak = False #variable to keep track of whether a drawn line was cut off for being too close to an opponent's line
    global FONT
    pygame.init()
    pygame.display.set_caption('Continuous Go')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    mouse = pygame.mouse
    #fpsClock = pygame.time.Clock()
    #canvas = DISPLAYSURF.copy()
    #canvas.fill(BGCOLOR)
    dots = [] #keeps track of points and lines drawn as series of connected points in current drawing
    turn = 'black' #black always goes first
    #DISPLAYSURF.fill(BGCOLOR)
    #DISPLAYSURF.blit(canvas, (0, 0))
    #pygame.display.update()
    turnLength = 0 #length of lines drawn so far
    mainBoard = [] #keeps track of everything drawn on board
    drawBoard(mainBoard)
    drawTurn(turn)
    drawLengthNum(turnLength)
    drawSlider(magnetDist)
    pygame.display.update()

    while True:
        #print(pygame.Surface.get_size(pygame.display.get_surface()))
        #left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
        for event in pygame.event.get():
            checkForQuit(event)          

            if not isOnSurface(mouse.get_pos()):
                if event.type == MOUSEBUTTONDOWN:
                    (x, y) = mouse.get_pos()
                    if SLIDERRECT.collidepoint(x, y):
                        magnetDist = int((x - SLIDERLEFT) / CLICKDIVISION)
                        drawBoard(mainBoard)
                        drawTurn(turn)
                        drawLengthNum(turnLength)
                        drawSlider(magnetDist)
                        pygame.display.update()
                continue

            if dist(mouse.get_pos(), adjustedPos) >= 1.5: #sqrt(2) < 1.5 < 2
                changed = False
            if not changed:
                closestLine = findClosestLine(mainBoard, mouse.get_pos(), turn, magnetDist)
                if closestLine != None:
                    #mouse is close to a line, so move the mouse to that line
                    mouse.set_pos(closestLine)
                    adjustedPos = closestLine
                    changed = True

            if event.type == MOUSEBUTTONDOWN:
                drawStraight = False #variable to keep track of whether user is drawing straight (as opposed to free-hand), initially False
                firstClickLocation = mouse.get_pos() #keeps track of initial click location
                drawBegin = True #tracks whether user is begining a free-hand draw; if so, firstClickLocation is used; initially True
                while True:
                    endTurn = False #indicator that a section of a turn is over; occurs upon stopping a draw or drawing past DRAWINGLENGTH
                    for event in pygame.event.get():
                        checkForQuit(event)

                        if not isOnSurface(mouse.get_pos()):
                            if event.type == MOUSEBUTTONDOWN:
                                (x, y) = mouse.get_pos()
                                if SLIDERRECT.collidepoint(x, y):
                                    magnetDist = int((x - SLIDERLEFT) / CLICKDIVISION)
                                drawBoard(mainBoard)
                                drawTurn(turn)
                                drawLengthNum(turnLength)
                                drawSlider(magnetDist)
                                pygame.display.update()
                            continue

                        if event.type == MOUSEBUTTONUP:
                            if len(dots) == 0: #user is starting a straight draw
                                drawStraight = True
                                pygame.draw.circle(DISPLAYSURF, DRAWCOLOR, mouse.get_pos(), 2)
                                pygame.display.update()
                                dots.append(mouse.get_pos())
                                drawBegin = False
                                continue
                            #user is stopping a draw
                            endTurn = True
                            break
                        elif drawBegin:
                            dots.append(firstClickLocation)
                            drawBegin = False
                        if drawStraight:
                            if dist(mouse.get_pos(), adjustedPos) >= 1.5: #sqrt(2) < 1.5 < 2
                                changed = False
                            if not changed:
                                closestLine = findClosestLine(mainBoard, mouse.get_pos(), turn, magnetDist)
                                if closestLine != None:
                                    #mouse is close to a line, so move the mouse to that line
                                    mouse.set_pos(closestLine)
                                    adjustedPos = closestLine
                                    changed = True

                            if event.type == MOUSEBUTTONDOWN:
                                drawStraight = False
                                potentialLine = False
                                potentialOffBoard = None
                                drawBoard(mainBoard)
                                drawTurn(turn)
                                drawLengthNum(turnLength)
                                drawSlider(magnetDist)
                                pygame.display.update()
                            else:
                                dots.append(mouse.get_pos())
                                potentialLine = True
                        if drawStraight == False:
                            dots.append(mouse.get_pos())
                        if potentialOffBoard:
                            dots[-2] = potentialOffBoard
                        if len(dots) > 1 and (not isOnBoard(dots[-2]) or not isOnBoard(dots[-1])): #drew outside board's boundary
                            if boundaryLineFix(dots[-2], dots[-1]) == None: #line drawn was entirely off the board
                                if potentialLine:
                                    del dots[-1]

                                    drawBoard(mainBoard)
                                    drawTurn(turn)
                                    drawLengthNum(turnLength)
                                    drawSlider(magnetDist)
                                    #pygame.draw.circle(DISPLAYSURF, DRAWCOLOR, dots[-1], 2)
                                    pygame.draw.circle(DISPLAYSURF, DRAWCOLOR, (round(dots[-1][0]), round(dots[-1][1])), 2)
                                    pygame.display.update()

                                    continue
                                last = dots[-1]
                                del dots[-1]
                                turnLength += drawnLength(dots)
                                dots = [last]
                                continue
                            else: #line was drawn partially off board and partially on
                                if drawStraight and not isOnBoard(dots[-2]):
                                    potentialOffBoard = dots[-2]
                                dots[-2], dots[-1] = boundaryLineFix(dots[-2], dots[-1])

                        #if len(dots) > 1 and not potentialLine:
                        if len(dots) > 1: #check if line should be cut off near intersections with opponent's lines
                            origDots1 = dots[-2]
                            origDots2 = dots[-1]
                            cutOff = checkIntersection(mainBoard, (dots[-2], dots[-1]), turn)
                            del dots[-1]
                            del dots[-1]

                            #potentialOffBoard = origDots1 #keep?
                            
                            if cutOff != None:
                                #del dots[-1]
                                dots.append(cutOff[0])
                                dots.append(cutOff[1])
                                #mainBoard.append((color(turn), dots[-2], dots[-1]))
                                if cutOff[0] != origDots1 or cutOff[1] != origDots2:
                                    cutOffBreak = True
                            else:
                                #if potentialLine and drawStraight: #FIX
                                if drawStraight:
                                    potentialOffBoard = origDots1
                                    dots.append(origDots1)
                                else:
                                    endTurn = True
                                    break

                        if turnLength + drawnLength(dots) > DRAWINGLENGTH: #too long because of quick drawing or just at DRAWINGLENGTH limit
                            overDrawnDot = dots[-1]
                            overDrawnLength = turnLength + drawnLength(dots)
                            del dots[-1]
                            underDrawnDot = dots[-1]
                            underDrawnLength = turnLength + drawnLength(dots)
                            newDot = divideLine(overDrawnDot, overDrawnLength, underDrawnDot, underDrawnLength)
                            dots.append(newDot)
                            if not potentialLine:
                                #cutOff = checkIntersection(mainBoard, (dots[-2], dots[-1]), turn)
                                #del dots[-1]
                                #del dots[-1]
                                #if cutOff != None:
                                #    dots.append(cutOff[0])
                                #    dots.append(cutOff[1])
                                #    mainBoard.append((color(turn), dots[-2], dots[-1]))

                                #print(dots[-2])
                                #print(dots[-1])

                                mainBoard.append((color(turn), dots[-2], dots[-1]))
                                
                                endTurn = True
                                break
                        if len(dots) > 1:
                            if potentialLine:
                                mainBoard.append((DRAWCOLOR, dots[-2], dots[-1]))
                                drawBoard(mainBoard)
                                drawTurn(turn)
                                drawLengthNum(turnLength)
                                drawSlider(magnetDist)
                                if potentialOffBoard:
                                    #pygame.draw.circle(DISPLAYSURF, DRAWCOLOR, potentialOffBoard, 2)
                                    pygame.draw.circle(DISPLAYSURF, DRAWCOLOR, (round(potentialOffBoard[0]), round(potentialOffBoard[1])), 2)
                                pygame.display.update()
                                del dots[-1]
                                del mainBoard[-1]
                                potentialLine = False
                                dots[-1] = origDots1 #attempt
                                continue
                            #cutOff = checkIntersection(mainBoard, (dots[-2], dots[-1]), turn)
                            #del dots[-1]
                            #del dots[-1]
                            #if cutOff != None:
                            #    dots.append(cutOff[0])
                            #    dots.append(cutOff[1])
                            #    mainBoard.append((color(turn), dots[-2], dots[-1]))
                            #else:
                            #    endTurn = True
                            #    break
                            
                            mainBoard.append((color(turn), dots[-2], dots[-1]))
                            if cutOffBreak:
                                endTurn = True
                                break
                            drawBoard(mainBoard)
                            drawTurn(turn)
                            drawLengthNum(turnLength + drawnLength(dots))
                            drawSlider(magnetDist)
                            pygame.display.update()
                        if turnLength + drawnLength(dots) > DRAWINGLENGTH - EPSILON: #IS THIS NECESSARY?
                            endTurn = True
                            break
                    if endTurn:
                        turnLength += drawnLength(dots)
                        drawBoard(mainBoard)
                        drawTurn(turn)
                        drawLengthNum(turnLength)
                        drawSlider(magnetDist)
                        pygame.display.update()
                        if turnLength >= DRAWINGLENGTH - EPSILON:
                            turn = opposite(turn)
                            turnLength = 0
                            drawBoard(mainBoard)
                            drawTurn(turn)
                            drawLengthNum(turnLength)
                            drawSlider(magnetDist)
                            pygame.display.update()
                            #pygame.time.wait(500) #small pause in between turns
                            #pygame.event.clear() #clear event queue
                        pygame.event.clear() #clear event queue CORRECT PLACE?
                        dots = []
                        potentialOffBoard = None
                        cutOffBreak = False
                        break

def drawnLength(dots):
    #returns the sum of the lengths of the lines formed in dots
    sum = 0
    i = 0
    while i < len(dots) - 1:
        sum += dist(dots[i], dots[i + 1])
        i += 1
    return sum

def dist(a, b):
    #returns the distance between two points
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def opposite(color):
    #returns the opposite color
    if color == WHITE:
        return BLACK
    if color == BLACK:
        return WHITE
    if color == 'white':
        return 'black'
    if color == 'black':
        return 'white'

def color(col):
    #converts turn to color
    if col == 'white':
        return WHITE
    if col == 'black':
        return BLACK

def boundaryLineFix(first, second):
    #returns point where line should be cut off to account for keeping the drawing on the board
    #returns None if there is no such point
    if first[0] == second[0] and first[1] == second[1]:
        return None
    leftBorder, topBorder = translateBoardToPixelCoord(0, 0)
    rightBorder, bottomBorder = translateBoardToPixelCoord(BOARDWIDTH - 1, BOARDHEIGHT - 1)

    if first[0] < leftBorder:
        if second[0] < leftBorder:
            return None
        proportion = (leftBorder - first[0]) / (second[0] - first[0])
        first = (leftBorder, first[1] + proportion * (second[1] - first[1]))
    if first[1] < topBorder:
        if second[1] < topBorder:
            return None
        proportion = (topBorder - first[1]) / (second[1] - first[1])
        first = (first[0] + proportion * (second[0] - first[0]), topBorder)
    if first[0] > rightBorder:
        if second[0] > rightBorder:
            return None
        proportion = (first[0] - rightBorder) / (first[0] - second[0])
        first = (rightBorder, first[1] + proportion * (second[1] - first[1]))
    if first[1] > bottomBorder:
        if second[1] > bottomBorder:
            return None
        proportion = (first[1] - bottomBorder) / (first[1] - second[1])
        first = (first[0] + proportion * (second[0] - first[0]), bottomBorder)
    if not isOnBoard(first):
        return None
    if second[0] < leftBorder:
        proportion = (leftBorder - second[0]) / (first[0] - second[0])
        second = (leftBorder, second[1] + proportion * (first[1] - second[1]))
    if second[1] < topBorder:
        proportion = (topBorder - second[1]) / (first[1] - second[1])
        second = (second[0] + proportion * (first[0] - second[0]), topBorder)
    if second[0] > rightBorder:
        proportion = (second[0] - rightBorder) / (second[0] - first[0])
        second = (rightBorder, second[1] + proportion * (first[1] - second[1]))
    if second[1] > bottomBorder:
        proportion = (second[1] - bottomBorder) / (second[1] - first[1])
        second = (second[0] + proportion * (first[0] - second[0]), bottomBorder)

    if dist(first, second) < EPSILON:
        return None
    
    return first, second

def divideLine(overDrawnDot, overDrawnLength, underDrawnDot, underDrawnLength):
    #returns point where line should be cut off to account for keeping the drawing under DRAWINGLENGTH
    proportion = (DRAWINGLENGTH - underDrawnLength) / (overDrawnLength - underDrawnLength)
    x = underDrawnDot[0] + proportion * (overDrawnDot[0] - underDrawnDot[0])
    y = underDrawnDot[1] + proportion * (overDrawnDot[1] - underDrawnDot[1])
    return (x, y)

def translateBoardToPixelCoord(x, y):
    #converts location on board to pixels
    return XMARGIN + x * SPACESIZE, YMARGIN + y * SPACESIZE

def drawBoard(board, last=None): #add last turn color?
    #draw background of area surrounding board
    DISPLAYSURF.fill(OUTERBGCOLOR)

    #draw background of board
    #boardRect = Rect(translateBoardToPixelCoord(-1, -1), (SPACESIZE * (BOARDWIDTH + 1), SPACESIZE * (BOARDHEIGHT + 1)))
    topLeft = translateBoardToPixelCoord(-OUTERSURF, -OUTERSURF)
    boardRect = Rect(topLeft, (SPACESIZE * (BOARDWIDTH - 1 + 2 * OUTERSURF), SPACESIZE * (BOARDHEIGHT - 1 + 2 * OUTERSURF)))
    #boardRect = Rect(XMARGIN - OUTERSURFACE, YMARGIN - OUTERSURFACE, SPACESIZE * (BOARDWIDTH - 1) + 2 * OUTERSURFACE, SPACESIZE * (BOARDHEIGHT - 1) + 2 * OUTERSURFACE)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, boardRect)

    #draw grid lines of the board
    alphaSurf = pygame.Surface(pygame.Surface.get_size(DISPLAYSURF), pygame.SRCALPHA)

    for x in range(BOARDWIDTH):
        # Draw the horizontal lines.
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + ((BOARDHEIGHT - 1) * SPACESIZE)
        pygame.draw.line(alphaSurf, GRAYALPHA, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT):
        # Draw the vertical lines.
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + ((BOARDWIDTH - 1) * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(alphaSurf, GRAYALPHA, (startx, starty), (endx, endy))

    #draw the small circles (star points) on the go board
    if BOARDWIDTH == 19 and BOARDHEIGHT == 19:
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if x % 6 == 3 and y % 6 == 3:
                    centerx, centery = translateBoardToPixelCoord(x, y)
                    pygame.draw.circle(alphaSurf, GRAYALPHA, (round(centerx), round(centery)), 5, 0)

    DISPLAYSURF.blit(alphaSurf, (0, 0))

    #draw the game's lines
    for line in board:
        pygame.draw.line(DISPLAYSURF, line[0], line[1], line[2])

def drawTurn(turn):
    #draws whose turn it is at the bottom of the screen
    turnSurf = FONT.render("%s's Turn" % (turn.title()), True, TEXTCOLOR)
    turnRect = turnSurf.get_rect()
    turnRect.bottomleft = (10, WINDOWHEIGHT - 60)
    DISPLAYSURF.blit(turnSurf, turnRect)

def drawLengthNum(length):
    #draws how much of the turn's line length has been drawn so far
    lengthSurf = FONT.render("%.2f Drawn" % (round(length, 2)), True, TEXTCOLOR)
    lengthRect = lengthSurf.get_rect()
    lengthRect.bottomleft = (10, WINDOWHEIGHT - 120)
    DISPLAYSURF.blit(lengthSurf, lengthRect)

    lengthSurf2 = FONT.render("(Out Of %.2f)" % (DRAWINGLENGTH), True, TEXTCOLOR)
    lengthRect2 = lengthSurf.get_rect()
    lengthRect2.bottomleft = (10, WINDOWHEIGHT - 100)
    DISPLAYSURF.blit(lengthSurf2, lengthRect2)

def drawSlider(magnetDist):
    #draws the interactive magnetic slider
    slideSurf = FONT.render("Mouse Magnet Strength", True, TEXTCOLOR)
    slideRect = slideSurf.get_rect()
    slideRect.bottomleft = (SLIDERLEFT - 26, SLIDERHEIGHT - 20)
    DISPLAYSURF.blit(slideSurf, slideRect)

    #minSurf = FONT.render("min", True, TEXTCOLOR)
    minSurf = FONT.render("0", True, TEXTCOLOR)
    minRect = minSurf.get_rect()
    minRect.topright = (SLIDERLEFT - 8, SLIDERHEIGHT)
    DISPLAYSURF.blit(minSurf, minRect)

    maxSurf = FONT.render("max", True, TEXTCOLOR)
    maxRect = maxSurf.get_rect()
    maxRect.topleft = (SLIDERRIGHT + 8, SLIDERHEIGHT)
    DISPLAYSURF.blit(maxSurf, maxRect)

    pygame.draw.rect(DISPLAYSURF, SLIDERCOLOR, (SLIDERLEFT, SLIDERHEIGHT, SLIDERRIGHT - SLIDERLEFT, 12))
    pygame.draw.circle(DISPLAYSURF, SLIDERCIRCLECOLOR, (int(SLIDERLEFT + SLIDERDIVISION * magnetDist), SLIDERHEIGHT + 6), 10)

def isOnBoard(position):
    #returns True iff the coordinates are located on the board
    x = position[0]
    y = position[1]
    minX, minY = translateBoardToPixelCoord(0, 0)
    maxX, maxY = translateBoardToPixelCoord(BOARDWIDTH - 1, BOARDHEIGHT - 1)
    return x >= minX and x <= maxX and y >= minY and y <= maxY

def isOnSurface(position):
    #returns True iff the coordinates are located on the surface surrounding the board
    x = position[0]
    y = position[1]
    minX, minY = translateBoardToPixelCoord(-OUTERSURF, -OUTERSURF)
    maxX, maxY = translateBoardToPixelCoord(BOARDWIDTH - 1 + OUTERSURF, BOARDHEIGHT - 1 + OUTERSURF)
    return x >= minX and x <= maxX and y >= minY and y <= maxY

def between(a, b, c):
    #checks if b is between a and c, inclusive
    low = min(a, c)
    high = max(a, c)
    return low <= b and b <= high

def betweenEx(a, b, c):
    #checks if b is between a and c, exclusive
    low = min(a, c)
    high = max(a, c)
    return low < b and b < high

def between2(a, b, c):
    #checks if b is between a and c, inclusive, or within one of being so
    low = min(a, c)
    high = max(a, c)
    return low <= b + 1 and b - 1 <= high

def inBox(p, line, d):
    #checks if p is within d of line, inclusive; if so, returns the nearest point on line to p; if not, returns None
    i = line[0]
    j = line[1]
    #near line:
    if i[0] == j[0]: #vertical line
        if between(i[1], p[1], j[1]) and between(i[0] - d, p[0], i[0] + d):
            return (i[0], p[1])
    elif i[1] == j[1]: #horizontal line
        if between(i[0], p[0], j[0]) and between(i[1] - d, p[1], i[1] + d):
            return (p[0], i[1])
    else: #oblique line
        m1 = (j[1] - i[1]) / (j[0] - i[0])
        b1 = i[1] - m1 * i[0]
        m2 = -1 / m1
        b2 = p[1] - m2 * p[0]
        x = (b2 - b1) / (m1 - m2)
        y = m2 * x + b2
        if between(i[0], x, j[0]) and dist(p, (x, y)) <= d:
            return (x, y)
    #near endpoint:
    if dist(p, i) <= d and dist(p, j) <= d:
        if dist(p, i) <= dist(p, j):
            return i
        return j
    if dist(p, i) <= d:
        return i
    if dist(p, j) <= d:
        return j
    return None

def findClosestLine(board, new, turn, magnetDist):
    #finds the closest line (among player's own) to the mouse (new) as long as it is within magnetDist
    #then returns the point on that line where the closest distance to the mouse is
    closestLine = None
    new = (new[0], -new[1]) #temporary conversion to treat board like coordinate plane
    for line in board:
        if line[0] != color(turn):
            continue
        line = ((line[1][0], -line[1][1]), (line[2][0], -line[2][1])) #temporary conversion to treat board like coordinate plane
        closestPoint = inBox(new, line, magnetDist)
        if closestPoint == None:
            continue
        closestDist = dist(new, closestPoint)
        if closestLine == None or closestDist < closestLine[0]:
            closestLine = [closestDist, closestPoint]
    if closestLine == None:
        return None
    return (closestLine[1][0], -closestLine[1][1]) #convert from coordinate plane back to board

def parallelLines(line, dist):
    #returns the two lines parallel to line at distance dist
    i = line[0]
    j = line[1]
    if i[0] == j[0]: #vertical line
        return ((i[0] - dist, i[1]), (i[0] - dist, j[1])), ((i[0] + dist, i[1]), (i[0] + dist, j[1]))
    if i[1] == j[1]: #horizontal line
        return ((i[0], i[1] + dist), (j[0], i[1] + dist)), ((i[0], i[1] - dist), (j[0], i[1] - dist))
    #oblique line:
    m1 = (j[1] - i[1]) / (j[0] - i[0])
    m2 = -1 / m1
    #m2 = tan(a), sin(a) = dy/dist, cos(a) = dx/dist
    dx = abs(dist * math.cos(math.atan(m2)))
    dy = abs(dist * math.sin(math.atan(m2)))
    if m1 > 0:
        dx = -dx
    return ((i[0] + dx, i[1] + dy), (j[0] + dx, j[1] + dy)), ((i[0] - dx, i[1] - dy), (j[0] - dx, j[1] - dy))

def linesIntersect(line1, line2):
    #return the intersection point of line1 and line2
    #return None if they don't intersect
    #if they intersect at multiple points:
    #if line1 is within line2, return None
    #if line1[0] is part of the intersection, return the part of the intersection closest to line1[1]
    #otherwise, return the part of the intersection closest to line1[0]
    h = line1[0]
    i = line1[1]
    j = line2[0]
    k = line2[1]
    if h[0] == i[0]: #vertical line1
        if j[0] == k[0]: #vertical line2
            if h[0] != j[0]:
                return None
            if between(j[1], h[1], k[1]):
                if between(j[1], i[1], k[1]):
                    return None
                if dist(i, j) < dist(i, k):
                    return j
                return k
            if between(j[1], i[1], k[1]) or between(h[1], j[1], i[1]):
                if dist(h, j) < dist(h, k):
                    return j
                return k
            return None
        if j[1] == k[1]: #horizontal line2
            if between(j[0], h[0], k[0]) and between(h[1], j[1], i[1]):
                return (h[0], j[1])
            return None
        #oblique line2
        m = (k[1] - j[1]) / (k[0] - j[0])
        b = j[1] - m * j[0]
        y = m * h[0] + b
        if between(h[1], y, i[1]) and between(j[0], h[0], k[0]):
            return (h[0], y)
        return None
    elif h[1] == i[1]: #horizontal line1
        if j[0] == k[0]: #vertical line2
            if between(j[1], h[1], k[1]) and between(h[0], j[0], i[0]):
                return (j[0], h[1])
            return None
        if j[1] == k[1]: #horizontal line2
            if h[1] != j[1]:
                return None
            if between(j[0], h[0], k[0]):
                if between(j[0], i[0], k[0]):
                    return None
                if dist(i, j) < dist(i, k):
                    return j
                return k
            if between(j[0], i[0], k[0]) or between(h[0], j[0], i[0]):
                if dist(h, j) < dist(h, k):
                    return j
                return k
            return None
        #oblique line2
        m = (k[1] - j[1]) / (k[0] - j[0])
        b = j[1] - m * j[0]
        x = (h[1] - b) / m
        if between(h[0], x, i[0]) and between(j[1], h[1], k[1]):
            return (x, h[1])
        return None
    else: #oblique line1
        if j[0] == k[0]: #vertical line2
            m = (i[1] - h[1]) / (i[0] - h[0])
            b = h[1] - m * h[0]
            y = m * j[0] + b
            if between(j[1], y, k[1]) and between(h[0], j[0], i[0]):
                return (j[0], y)
            return None
        if j[1] == k[1]: #horizontal line2
            m = (i[1] - h[1]) / (i[0] - h[0])
            b = h[1] - m * h[0]
            x = (j[1] - b) / m
            if between(j[0], x, k[0]) and between(h[1], j[1], i[1]):
                return (x, j[1])
            return None
        #oblique line2
        m1 = (i[1] - h[1]) / (i[0] - h[0])
        b1 = h[1] - m1 * h[0]
        m2 = (k[1] - j[1]) / (k[0] - j[0])
        b2 = j[1] - m2 * j[0]
        if m1 == m2:
            if b1 != b2:
                return None
            if between(j[0], h[0], k[0]):
                if between(j[0], i[0], k[0]):
                    return None
                if dist(i, j) < dist(i, k):
                    return j
                return k
            if between(j[0], i[0], k[0]) or between(h[0], j[0], i[0]):
                if dist(h, j) < dist(h, k):
                    return j
                return k
            return None
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        if between(h[0], x, i[0]) and between(j[0], x, k[0]):
            return (x, y)
        return None

def circleLineIntersect(line, center, rad, switch=False):
    #returns the intersection point of line and the circle with center center and radius rad
    #if multiple such points and switch is False, returns the one closest to the first point in the line
    #if multiple such points and switch is True, returns the one closest to the second point in the line
    #if no such points, returns None
    if switch:
        p = line[1]
        q = line[0]
    else:
        p = line[0]
        q = line[1]
    #(x - center[0]) ** 2 + (y - center[1]) ** 2 = rad ** 2
    if p[0] == q[0]: #vertical line
        if rad ** 2 - (p[0] - center[0]) ** 2 < 0:
            return None
        y1 = center[1] - math.sqrt(rad ** 2 - (p[0] - center[0]) ** 2)
        y2 = center[1] + math.sqrt(rad ** 2 - (p[0] - center[0]) ** 2)
        if (p[1] > y2 and q[1] > y2) or (p[1] < y1 and q[1] < y1):
            return None
        if y1 < p[1] and p[1] < y2 and y1 < q[1] and q[1] < y2:
            return None
        if p[1] > y1 and q[1] > y1:
            return (p[0], y2)
        if p[1] < y2 and q[1] < y2:
            return (p[0], y1)
        if p[1] < q[1]:
            return (p[0], y1)
        return (p[0], y2)
    #horizontal line or oblique line
    m = (q[1] - p[1]) / (q[0] - p[0])
    b = p[1] - m * p[0]
    A = m ** 2 + 1
    B = 2 * m * b - 2 * center[0] - 2 * m * center[1]
    C = center[0] ** 2 + b ** 2 - 2 * b * center[1] + center[1] ** 2 - rad ** 2
    if B ** 2 - 4 * A * C < 0:
        return None
    x1 = (-B - math.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
    x2 = (-B + math.sqrt(B ** 2 - 4 * A * C)) / (2 * A)
    if (p[0] < x1 and q[0] < x1) or (p[0] > x2 and q[0] > x2):
        return None
    if x1 < p[0] and p[0] < x2 and x1 < q[0] and q[0] < x2:
        return None
    if p[0] < x2 and q[0] < x2:
        x = x1
    elif p[0] > x1 and q[0] > x1:
        x = x2
    elif p[0] < q[0]:
        x = x1
    else:
        x = x2
    y = m * x + b
    return (x, y)

def checkIntersection(board, newLine, turn):
    #check if the new line comes within INTERSECTDIST of the opposing player's lines on the board
    #if so, return the section of the line remaining after being cut off
    #if this section is nonexistent, return None
    #if the new line never comes near any opposing lines, return the original line

    shortestLine = ((newLine[0][0], -newLine[0][1]), (newLine[1][0], -newLine[1][1])) #conversion to treat board like coordinate plane

    #print("shortestLine start:")
    #print(shortestLine)

    firstPointIntersect = [] #variable to keep track of lines that cause shortestLine[0] to be adjusted because of proximity

    while True:
        lineChange = False #variable to keep track of whether shortestLine has been adjusted because its first point is near another line
        for line in board:
            if line[0] == color(turn):
                continue

            i = line[1]
            j = line[2]

            i = (i[0], -i[1]) #conversion to treat board like coordinate plane
            j = (j[0], -j[1]) #conversion to treat board like coordinate plane

            if inBox(shortestLine[0], (i, j), INTERSECTDIST) and (i, j) not in firstPointIntersect:
                if inBox(shortestLine[1], (i, j), INTERSECTDIST):
                    return None
                a, b = parallelLines((i, j), INTERSECTDIST)
                newPoint = linesIntersect((shortestLine[0], shortestLine[1]), a)
                if newPoint != None:
                    shortestLine = (newPoint, shortestLine[1])
                    lineChange = True
                newPoint = linesIntersect((shortestLine[0], shortestLine[1]), b)
                if newPoint != None:
                    shortestLine = (newPoint, shortestLine[1])
                    lineChange = True
                newPoint = circleLineIntersect((shortestLine[0], shortestLine[1]), i, INTERSECTDIST, True)
                if newPoint != None:
                    shortestLine = (newPoint, shortestLine[1])
                    lineChange = True
                newPoint = circleLineIntersect((shortestLine[0], shortestLine[1]), j, INTERSECTDIST, True)
                if newPoint != None:
                    shortestLine = (newPoint, shortestLine[1])
                    lineChange = True
                firstPointIntersect.append((i, j))
                #if not lineChange:
                    #print(shortestLine[0], shortestLine[1]) #why should this ever print?
                    #print(i, j)
                if lineChange:
                    break
        if shortestLine[0] == shortestLine[1]:
            return None
        if not lineChange:
            break

    #print("shortestLine middle:")
    #print(shortestLine)

    for line in board:
        if line[0] == color(turn):
            continue

        i = line[1]
        j = line[2]

        i = (i[0], -i[1]) #conversion to treat board like coordinate plane
        j = (j[0], -j[1]) #conversion to treat board like coordinate plane

        #skip lines for which shortestLine[0] has already been adjusted
        if (i, j) in firstPointIntersect:
            continue

        #attempt:
        #if inBox(shortestLine[0], (i, j), INTERSECTDIST):
        #    continue

        a, b = parallelLines((i, j), INTERSECTDIST)
        newPoint = linesIntersect((shortestLine[0], shortestLine[1]), a)
        if newPoint != None:
            #print("A")
            #print(shortestLine)
            shortestLine = (shortestLine[0], newPoint)
            #print(shortestLine)
        newPoint = linesIntersect((shortestLine[0], shortestLine[1]), b)
        if newPoint != None:
            #print("B")
            #print(shortestLine)
            shortestLine = (shortestLine[0], newPoint)
            #print(shortestLine)
        newPoint = circleLineIntersect((shortestLine[0], shortestLine[1]), i, INTERSECTDIST)
        if newPoint != None:
            #print("C")
            #print(shortestLine)
            shortestLine = (shortestLine[0], newPoint)
            #print(shortestLine)
        newPoint = circleLineIntersect((shortestLine[0], shortestLine[1]), j, INTERSECTDIST)
        if newPoint != None:
            #print("D")
            #print(shortestLine)
            shortestLine = (shortestLine[0], newPoint)
            #print(shortestLine)
        if shortestLine[0] == shortestLine[1]:
            return None

    #print("shortestLine end:")
    #print(shortestLine)

    return ((shortestLine[0][0], -shortestLine[0][1]), (shortestLine[1][0], -shortestLine[1][1])) #conversion back to original coordinates

def checkForQuit(event):
    #if the user has quit or hit the escape key, quit the program
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()

#to do:
#determine if I need EPSILON
#make written displays like go
#figure out if drawing length should equal space size
#make potential line reflect checkIntersection cutoff
    #problems:
        #still observing crossing-over errors in complex situations
            #investigate whether results of inBox and results of circleLineIntersect may conflict
                #changes to circleLineIntersect still don't solve problem RESUME HERE
        #to do: change name of "potentialOffBoard" now that I'm using it for another purpose
#consider discretizing inputs
#investigate clock
#handle cases where user only has a tiny amount left to draw

#eventually do:
#allow player to redo turn so far or at least cancel current drawing
#check if need the double "for event in pygame.event.get():"
#clarify difference in main between continue and break
#make the slider draggable
#distinguish last turn, probably via color
#allow querying of groups and distance between groups
#allow planning phase to try to draw lines and then button to click for confirmation
#add ability to find area completely enclosed (like "fill" in Paint) in order for player to be able to count
    #or possibly even almost completely enclosed
    #or make player draw around territory to query the area
#fill in enclosed area smaller than (or equal to) X with player's color (including area enclosed between discs)
    #X = minimum area to make life
    #whenever something is filled add text of area over it
    #add these numbers to total on side bar
    #area connected to/added to shaded group is automatically shaded
    #once a shaded group supasses (or is equal to) X, it can't be captured
    #condsider: do light shading when <X and then fully black/white when greater
#add clock
#allow competitive play on different computers
#determine and add komi

#consider:
#add feature to either be able to check if line A is connected to line B, or to tell if an opening is closed
#add feature to calculate distance or even draw line from point a to point b even if it has to go around another line
    #maybe with right clicks
#allowing pass of the end of a turn (like when player has two pixels left to draw)
#making version with only option to plop down one line per turn at different angles
    #with potential line that rotates via scrolling
#add ability to zoom
#automatic enclosing to help players close off area
#have panel to choose ways to draw lines
    #see full length of straight line
    #point to point like in Paint
    #free-hand
    #circle
        #could just hold in mouse for expanding circle
    #curve?
#add light shading based on likely future of area
#add panel to keep track of all the groups on the board
#decide whether to add option to pass
    #one way to maintain passing would be to disallow territory additions so small as to be below a certain threshold
        #this would make moving after a certain point useless
#change mouse pointer (for visibility)