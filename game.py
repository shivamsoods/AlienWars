import pygame,sys,random,time
from pygame.locals import *

FPS=30
SCREENWIDTH=640
SCREENHEIGHT=480
HALFSCREENWIDTH=int(SCREENWIDTH/2)   #half define kar diya
HALFSCREENHEIGHT=int(SCREENHEIGHT/2)

NUM_ENEMY = 30
NUM_STARS = 80
INVULNTIME = 2

LEFT = 'left'
RIGHT = 'right'

MAX_HEALTH=3
INITIAL_SIZE=30
WIN_SIZE=300

PLAYER_VELOCITY = 15
ENEMY_VEL_MIN=2
ENEMY_VEL_MAX=7

BLACK =(0,0,0)
WHITE=(255,255,255)
RED = (126,100,234)

CAMERAVIEW=100


def main():

    global PLAYERSURFACE,DISPLAYSURF,STARSURFACE,CLOCK,PLAYERSURFACE1

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
    pygame.display.set_caption("Game")
   # pygame.display.set_icon(pygame.image.load("pikachu.png"))
    CLOCK = pygame.time.Clock()

    PLAYERSURFACE=pygame.image.load("alien.png")
    PLAYERSURFACE1=pygame.transform.flip(PLAYERSURFACE,True,False) # baad me use karne k liye phle hi flip kr liya
    STARSURFACE=pygame.image.load("star.png")

    while True:
        runGame()

def runGame():
    invulnerableMode = False  # if the player is invulnerable
    invulnerableStartTime = 0 # time the player became invulnerable
    gameOverMode = False      # if the player has lost
    gameOverStartTime = 0     # time the player lost
    winMode = False           # if the player has won
    camx=0
    camy=0
    # movex = (camx + SCREENWIDTH) / 2
    # movey = (camy + SCREENHEIGHT) / 2
    playerObject = {
        "surface":PLAYERSURFACE,
        "facing":LEFT,
        "size":INITIAL_SIZE,
        "health":MAX_HEALTH,
        "x":HALFSCREENWIDTH,   #yaha x or y ki value li
        "y":HALFSCREENHEIGHT
    }

    stars = []
    enemies=[]

    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    for i in range(10):
        stars.append(makeNewStar(camx,camy))
        stars[i]['x'] = random.randint(camx,camx + SCREENWIDTH)
        stars[i]['y']= random.randint(camy,camy + SCREENHEIGHT)

    while True:

        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False

        DISPLAYSURF.fill(BLACK)  # global
       # print("hi")
        for eObj in enemies:
            # move the squirrel
            eObj['x'] += eObj['movex']
            eObj['y'] += eObj['movey']

       #      # random chance they change direction
        if random.randint(0, 99) < 2:
                eObj['movex'] = getRandomVelocity()
                eObj['movey'] = getRandomVelocity()
                if eObj['movex'] > 0: # faces right
                    eObj['surface'] = pygame.transform.scale(PLAYERSURFACE1, (eObj['width'], eObj['height']))
                else: # faces left
                    eObj['surface'] = pygame.transform.scale(PLAYERSURFACE, (eObj['width'], eObj['height']))

        for st in stars:
           #changes
            sRect = pygame.Rect(st['x']-camx,   #camx and camy change ho rha h
                                st['y']-camy,
                                st['width'],st['height'])
          #  print(st['x'])
            DISPLAYSURF.blit(STARSURFACE,sRect)
         #  emnemy squuirels banayi
        for eObj in enemies:                    #yha bhi chnages kiye enemies ka rect banaya    #yaha error aa rahi h pata nahi kyu
            # eObj['rect'] = pygame.Rect((eObj['x'] - camx,
            #                             eObj['y'] - camy,
            #                             eObj['width'],
            #                             eObj['height']))
            DISPLAYSURF.blit(eObj['surface'],(eObj['x'],eObj['y']))
            #yha pr player object ka rect banaya
            if not gameOverMode and not invulnerableMode:
                playerObject['rect'] = pygame.Rect((playerObject['x']-camx,    # x and y ki value define nahi ki
                                         playerObject['y']-camy,               #thi upar isliye error aa rahi thi
                                         playerObject['size'],
                                         playerObject['size']))
                DISPLAYSURF.blit(playerObject['surface'],playerObject['rect'])
        drawHealthMeter(playerObject['health'])         #Health meter niche define kiya h


        # for event in pygame.event.get(): # event handling loop
        #     if event.type == QUIT:
        #         terminate()
        #
        #     elif event.type == KEYDOWN:
        #         if event.key in (K_UP, K_w):
        #             moveDown = False
        #             moveUp = True
        #         elif event.key in (K_DOWN, K_s):
        #             moveUp = False
        #             moveDown = True
        #         elif event.key in (K_LEFT, K_a):
        #             moveRight = False
        #             moveLeft = True
        #             if playerObject['facing'] != LEFT: # change player image
        #                 playerObject['surface'] = pygame.transform.scale(PLAYERSURFACE, (playerObject['size'], playerObject['size']))
        #             playerObject['facing'] = LEFT
        #         elif event.key in (K_RIGHT, K_d):
        #             moveLeft = False
        #             moveRight = True
        #             if playerObject['facing'] != RIGHT: # change player image
        #                 playerObject['surface'] = pygame.transform.scale(PLAYERSURFACE1, (playerObject['size'], playerObject['size']))
        #             playerObject['facing'] = RIGHT
        #         elif winMode and event.key == K_r:
        #             return
        #
        #     elif event.type == KEYUP:
        #         # stop moving the player's squirrel
        #         if event.key in (K_LEFT, K_a):
        #             moveLeft = False
        #         elif event.key in (K_RIGHT, K_d):
        #             moveRight = False
        #         elif event.key in (K_UP, K_w):
        #             moveUp = False
        #         elif event.key in (K_DOWN, K_s):
        #             moveDown = False
        #
        #         elif event.key == K_ESCAPE:
        #             pygame.quit()
        #             sys.exit()
        #
        # if not gameOverMode:
        #     # actually move the player
        #     if moveLeft:
        #         playerObject['x'] -= PLAYER_VELOCITY
        #     if moveRight:
        #         playerObject['x'] += PLAYER_VELOCITY
        #     if moveUp:
        #         playerObject['y'] -= PLAYER_VELOCITY
        #     if moveDown:
        #         playerObject['y'] += PLAYER_VELOCITY

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key ==K_LEFT:
                    if playerObject['facing']!=LEFT: # iski wajah se left right move nahi kar raha tha don't know why
                       # playerObject['surface'] = pygame.transform.scale(PLAYERSURFACE,
                                                                     # (playerObject['size'], playerObject['size']))
                        #pygame.transform.flip(PLAYERSURFACE,False,True)  # yaha changes honge
                        playerObject['facing']=LEFT
                    playerObject['x'] -= PLAYER_VELOCITY
                    # movex -= PLAYER_VELOCITY ye nahi hoga
                    if playerObject['x'] < camx+HALFSCREENWIDTH :
                       camx -= PLAYER_VELOCITY

                elif event.key == pygame.K_RIGHT:
                    if playerObject['facing']!=RIGHT:
                        #pygame.transform.flip(PLAYERSURFACE,False,True)

                        playerObject['facing']=RIGHT
                    playerObject['x'] += PLAYER_VELOCITY
                    #movex += PLAYER_VELOCITY
                    if playerObject['x']> camx+HALFSCREENWIDTH:
                        camx += PLAYER_VELOCITY

                elif event.key == pygame.K_UP:
                   # movey -= PLAYER_VELOCITY
                   playerObject['y'] -= PLAYER_VELOCITY

                #if movey < camy+50 : yaha 50 ki jagah halfscreenheight le li
                if playerObject['y'] < camy+HALFSCREENHEIGHT:
                        camy -= PLAYER_VELOCITY

                elif event.key == pygame.K_DOWN:
                    playerObject['y'] += PLAYER_VELOCITY
                   # movey += PLAYER_VELOCITY

                    if playerObject['y']> camy+HALFSCREENHEIGHT :
                       camy += PLAYER_VELOCITY

                elif event.key== pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT, K_a):
                    playerObject['x'] = playerObject['x']
                elif event.key in (K_RIGHT, K_d):
                   playerObject['x']=playerObject['x']
                elif event.key in (K_UP, K_w):
                    playerObject['y']=playerObject['y']
                elif event.key in (K_DOWN, K_s):
                    playerObject['y']=playerObject['y']






        while len(stars)<NUM_STARS:
            stars.append(makeNewStar(camx,camy))
        while len(enemies) < NUM_ENEMY:         #jaise stars append kiye the wese hi enemies laa rahe h frame me
            enemies.append(makeNewEnemies(camx, camy))

        for i in range (len(stars)-1,0):
            if stars[i]['x'] not in range(camx-SCREENWIDTH,camx+2*SCREENWIDTH) and stars[i]['y'] not in range(camy-SCREENHEIGHT,camy+2*SCREENHEIGHT):
                del stars[i]

        pygame.display.update()
        CLOCK.tick(FPS)



def makeNewStar(camx,camy):
    st = {}
    st["width"] = STARSURFACE.get_width()
    st["height"]= STARSURFACE.get_height()
    st['x'], st['y'] = cord_inactive(camx,camy,st['width'],st['height'])
    st['rect'] = pygame.Rect(st['x'], st['y'], st['width'], st['height'])
    return st

def makeNewEnemies(camx, camy):    #yaha par enemies banaye
    eObj = {}
    generalSize = random.randint(5, 25)
    multiplier = random.randint(1, 3)
    eObj['width']  = (generalSize + random.randint(0, 10)) * multiplier
    eObj['height'] = (generalSize + random.randint(0, 10)) * multiplier
    eObj['x'], eObj['y'] = cord_inactive(camx, camy, eObj['width'], eObj['height'])
    eObj['movex'] = getRandomVelocity()
    eObj['movey'] = getRandomVelocity()
    if eObj['movex'] < 0: # squirrel is facing left
        eObj['surface'] = pygame.transform.scale(PLAYERSURFACE, (eObj['width'], eObj['height']))
    else: # squirrel is facing right
        eObj['surface'] = pygame.transform.scale(PLAYERSURFACE1, (eObj['width'], eObj['height']))
    return eObj

def getRandomVelocity():
    speed = random.randint(ENEMY_VEL_MIN, ENEMY_VEL_MAX)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed

def drawHealthMeter(currentHealth):
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(DISPLAYSURF, RED,   (15, 5 + (10 * MAX_HEALTH) - i * 10, 20, 10))
    for i in range(MAX_HEALTH): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (15, 5 + (10 * MAX_HEALTH) - i * 10, 20, 10), 1)


def cord_inactive(camx, camy,objWidth,objHeight):

    while True:
        x = random.randint(camx-SCREENWIDTH, camx+2*SCREENWIDTH)
        y=random.randint(camy-SCREENHEIGHT, camy+2*SCREENHEIGHT)
        if (x < camx or x >camx+SCREENWIDTH) and (y <camy or y>camy + SCREENHEIGHT):
            # st['x'] = x
            # st['y'] = y
            return x,y

if __name__ == '__main__':
    main()