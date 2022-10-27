import pygame
import random

tutorial = [
"Welcome to disco snake. The classic snake game but with a twist",
"You can eat the bait if your snake is the same color as the bait.",
"Every time you eat the bait, the bait changes color. You can change ",
"the color of your snake if you collide with your snake's body. BUT it ",
"works only if your snake is a different color than the bait. You lose if ",
"your snake is the same color as the bait and you try to change color or ",
"you go out of bounds or you eat the bait while your snake has a different color",
"arrow keys to move, click left mouse button to play and again to initialize the snake",
"There's an issue which i'm hoping to fix, where the snake won't eat the bait every time",
]
# modifying these changes the screen size
rows = 100
cols = 100
# step is the size of an individual square
step = 10
# initial length of the snake
length = 20
# initial colors for the snake and the bait
snakecolor = (89, 212, 151)
baitcolor = (89, 212, 151)
# the colors a snake or a bait can inherit
colors = [
    (89, 212, 151),
    (89, 205, 212),
    (212, 89, 91),
    (212, 206, 89),

]
# ^   feel free to change
#/ \  or add to
# |   these values  
# |


# of course it needs a score
score = 0

# starting up pygame
pygame.init()
# display size is tied to the number of rows and columns in the matrix (below)
DISPLAY_WIDTH = (rows + 2)*step
DISPLAY_HEIGHT = (cols + 2)*step
# setting the screen parameters
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.RESIZABLE) -- see line 187
pygame.display.set_caption("disco snake")
fps = pygame.time.Clock()


# making an empty matrix or a grid with the size of cols*rows in which the snake can move
basegrid = [0] * rows           # 0 0 0 0  --> (times cols)
for i in range(rows):           # 0 0 0 0   
    basegrid[i] = [0] * cols    # 0 0 0 0   |
# print(basegrid)                           v  (times rows)



snakehead = 0
# this holds the links of the snake
rectlist = []
# initial location of the bait, a random location on the screen, with the size of 'step'
bait = (random.randrange(step, DISPLAY_WIDTH-step, step), random.randrange(step, DISPLAY_HEIGHT-step, step),  step, step)
# the directions the snake can travel in
direction = ""
dirs = ["LEFT", "RIGHT", "UP", "DOWN"]

# populating the coordinate system
y_coord = step
x_coord = step
for i in basegrid:
    x_coord = step
    for x in range(len(basegrid[0])):                                       #   for example with a step of 25:
        basegrid[basegrid.index(i)][x] = str(x_coord) + "," + str(y_coord)  # [0, 0] [25, 0] [50, 0]   --> (times cols)
        x_coord += step                                                     # [0,25] [25,25] [50,25]
    y_coord += step                                                         # [0,50] [25,50] [50,50]    |
                                                                            #                           v  (times rows)

# making a 1px wide grid dependent on the coordinate system, for testing purposes
def grid(mt):
    for i in mt:
        for x in range(len(mt[0])):
            p = mt[mt.index(i)][x]
            p = p.split(",")
            pygame.draw.rect(screen, (255, 0, 0), (int(p[0]), int(p[1]), step, step), 1)

# click -> start the snake in the selected square 
def drawsquare(mt1):
    global snakehead
    global rectlist
    global direction
    global dirs
    z, y = pygame.mouse.get_pos() # stores the mouse x, y coords in a tuple eg 467, 332
    print(z, y)                   # for testing
    for i in mt1:
        for x in range(len(mt1[0])):
            p = mt1[mt1.index(i)][x]
            p = p.split(",")    # eg [450, 300] gets split into '450' and '300', therefore:
            p[0] = int(p[0])    # p[0] = 450
            p[1] = int(p[1])    # p[1] = 300
            if p[0] < z < (p[0] + step) and p[1] < y < (p[1] + step):   # checks if the mouse coords are in any square eg with the previous example 'if 450 < 467 < 500 and 300 < 332 < 350':
                snakehead = pygame.Rect(p[0], p[1], step, step)         # it draws the snake's head
                direction = random.choice(dirs) # snake starts to move in a random direction
                print(int(p[0]), int(p[1]))     # just for testing
                rectlist.append(snakehead)      # see below, line 217

# moving the snake
def movesquare():
    global snakehead
    global rectlist
    global direction
    keys = pygame.key.get_pressed()
    # basic controls
    if keys[pygame.K_LEFT] and direction != "RIGHT": # the snake can't change direction to right if its moving left etc
        print("K_LEFT")
        snakehead = pygame.Rect.move(snakehead, -step, 0) # moves the snake along the x and/or y axis
        rectlist.append(snakehead)  # see belowm line 217
        direction = "LEFT"
          
    if keys[pygame.K_RIGHT] and direction != "LEFT":
        print("K_RIGHT")
        snakehead = pygame.Rect.move(snakehead, step, 0)
        rectlist.append(snakehead)
        direction = "RIGHT"

    if keys[pygame.K_UP] and direction != "DOWN":
        print("K_UP")
        snakehead = pygame.Rect.move(snakehead, 0, -step)
        rectlist.append(snakehead)
        direction = "UP"

    if keys[pygame.K_DOWN] and direction != "UP":
        print("K_DOWN")
        snakehead = pygame.Rect.move(snakehead, 0, step)
        rectlist.append(snakehead)
        direction = "DOWN"        

# spawning the bait
def spawn():
    global bait
    global baitcolor
    x = random.randrange(step, DISPLAY_WIDTH-step, step)
    y = random.randrange(step, DISPLAY_HEIGHT-step, step)
    bait = pygame.Rect((x), (y), step, step)
    baitcolor = random.choice(colors)


# drawing the initial bait
pygame.draw.rect(screen, (random.choice(colors)), (bait), 0, -1) 

# basically these loops continue until thing X happens
endloop = False
gameloop = False

# creates the main screen
while endloop is False:
    screen.fill((0, 0, 0))
    myfont = pygame.font.SysFont("Britannic Bold", 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type== pygame.MOUSEBUTTONDOWN: 
            endloop = True # if you click LMB, the main menu loop ends
            gameloop = True # and the game begins
    y_text = DISPLAY_HEIGHT/6
    for i in tutorial:                                  # renders the
        line = myfont.render(str(i), 1, (255, 0, 0))    # tutorial text
        screen.blit(line,(DISPLAY_WIDTH/8,y_text))      # as seen above
        y_text = y_text + 30
    pygame.display.flip()

# the main gameloop
while gameloop is True:
    screen.fill((0,0,0)) 
    #grid(basegrid)  -- un-# if you wanna see the grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # if you press X it closes the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawsquare(basegrid) # press LMB to initialise the snake
        elif event.type == pygame.KEYDOWN:
            movesquare() # if you press a key, the program checks if the snake changes the direction as a result
    
    #DISPLAY_WIDTH, DISPLAY_HEIGHT = pygame.display.get_surface().get_size() -- for testing purposes only, you can resize the screen and it would add more cols rows, but it doesn't really work well
    #cols = sqrt(DISPLAY_WIDTH)
    #rows = sqrt(DISPLAY_HEIGHT)
    #step = (DISPLAY_WIDTH//cols + DISPLAY_HEIGHT//rows)/2
    
    # snake is moving based on the direction
    if direction == "LEFT":
        snakehead = pygame.Rect.move(snakehead, -step, 0)
        rectlist.append(snakehead)
        direction = "LEFT"
          
    if direction == "RIGHT":
        snakehead = pygame.Rect.move(snakehead, step, 0)
        rectlist.append(snakehead)
        direction = "RIGHT"

    if direction == "UP":
        snakehead = pygame.Rect.move(snakehead, 0, -step)
        rectlist.append(snakehead)
        direction = "UP"

    if direction == "DOWN":
        snakehead = pygame.Rect.move(snakehead, 0, step)
        rectlist.append(snakehead)
        direction = "DOWN"   
    scorefont = pygame.font.SysFont("Britannic Bold", 20)
    scoretext = scorefont.render('score: ' + str(score), 1, (255, 0, 0)) # renders the score
    screen.blit(scoretext, (20, 20))
    pygame.draw.rect(screen, baitcolor, (bait), 0, -1) 
    
    for i in rectlist[::-1]:                        # so basically the snake is a list of rect objects like these: <rect(330, 540, 10, 10)>
        pygame.draw.rect(screen, snakecolor, i)     # the list keeps changing all the time, adding new rects and deleting prior ones
                                                    # so at all times theres 'length' amount of rects, which the programs draws onto the screen
                                                    # rectlist[-1] is the last rect added to the list, so the snake's head, like so: [0(tail)] [1] [2] [3] [4] [5(head)]
                                                    # because every time the snake moves, it appends the last rect to the list depending on the direction

    if len(rectlist) > 0 and rectlist[-1] == bait:  # if the snake head == bait, the snake eats the bait
        if snakecolor == baitcolor:                 # only on the condition that their RGB values are the same...
            print(bait) # testing
            spawn() # create a new bait
            length += 1 # enlongen the snake
            score += 5
            
        elif snakecolor != baitcolor:               # ...but if their RGB values are different,
            pygame.quit()                           # the program quits

    for i in rectlist:              
        if len(rectlist) > length:  # if the snake gets added a new value [0(tail)] [1] [2] [3] [4] [5(head)] [6(newhead)] because the snake is continuously moving and adding to the list, the tail bit needs to get chopped off
            rectlist.pop(0)         # without this line for example, the snake would get infinitely long. this line removes the tail or the  rectlist[0] in the list

    try:
        if rectlist[-1].left < 0 or rectlist[-1].right > DISPLAY_WIDTH or rectlist[-1].top < 0 or rectlist[-1].bottom > DISPLAY_HEIGHT: # if the snake moves out of bounds,
            pygame.quit()                                                                                                               # the program quits
    except:
        pass
    

    for i in rectlist:                                                      # the color changing algorithm
        testlist = rectlist[:]                                              # creates a new list identical to the snake's list

        try:                                                                # can only do it when there's enough elements in the list
            testlist.remove(i)                                              # it removes 'i' from testlist and 
            for x in testlist[testlist.index(i):]:                          # compares it to the testlist (so i isn't in testlist) because if i wasn't removed, it would always be on the list and the program would not work as intended
                if i == x and rectlist[-1] == i:                            # if i overlaps x (meaning if any 2 rects overlap meaning if the snake touches itself) and if rectlist[-1] (snake's head) touches 'i' --> meaning any other part in the snake's body
                    if snakecolor != baitcolor:                             # and if you can change the color - meaning if the snake has a different color than the bait (it wouldn't be fun if you could endlessly change colors)
                        newcolors = [x for x in colors if x != snakecolor]  # then it creates a new list excluding the color the snake already has, so the snake wouldn't get the same color
                        snakecolor1 = random.choice(newcolors)              # randomly picks a new color
                    elif snakecolor == baitcolor:                           # as i said,
                        pygame.quit()                                       # it wouldn't be fun if you could endlessly change colors
                if i == x:                                                  # if 2 rects (parts of the snake) overlap, 
                    for x in testlist[testlist.index(i):]:                  # then it takes the list from the overlapping point to the end (front part of the snake) [tail] [don't draw] [don't draw] [don't draw] [overlaps] [draw] [draw] [draw] [snake's head]
                        pygame.draw.rect(screen, snakecolor1, x)            # and draws every square, basically overrinding the line 217 command for drawing the snake
            if i == rectlist[0]:                                            # if there aren't any more overlapping rects,
                snakecolor = snakecolor1                                    # set a new color. without this line, the snake would start moving with a new color, but as soon as no rects overlap, it would turn to the previous color
        except:
            pass
        
                    
    pygame.display.update() # updates the display
    fps.tick(20)            # 20 times per second. fps is tied to the snake's speed, because every time the screen updates, the snake moves 1 instance, so changing this accelerates/decelerates the snake in a way