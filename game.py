import pygame,sys,random,time
from pygame.locals import *

FPS=30
SCREENWIDTH=640
SCREENHEIGHT=480
HALFSCREENWIDTH=int(SCREENWIDTH/2)   #half define kar diya
HALFSCREENHEIGHT=int(SCREENHEIGHT/2)

NUM_ENEMY = 80
NUM_STARS = 80
INVULNTIME = 2
GAMEOVERTIME = 4

LEFT = 'left'
RIGHT = 'right'

MAX_HEALTH=3
INITIAL_SIZE=30
WIN_SIZE=230

PLAYER_VELOCITY = 20
ENEMY_VEL_MIN=2
ENEMY_VEL_MAX=7

BLACK =(0,0,0)
WHITE=(255,255,255)
RED = (126,100,234)

CAMERASLACK=100



def main():

    global PLAYERSURFACE,DISPLAYSURF,STARSURFACE,CLOCK,PLAYERSURFACE1,BASICFONT

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
    pygame.display.set_caption("Game")
    pygame.display.set_icon(pygame.image.load("pikachu.png"))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    CLOCK = pygame.time.Clock()

    PLAYERSURFACE=pygame.image.load("alien.png")
    PLAYERSURFACE1=pygame.image.load("pikachu.png") # baad me use karne k liye phle hi flip kr liya
    STARSURFACE=pygame.image.load("star.png")


    while True:
        runGame()

def runGame():
    invulnerableMode = False  # if the player is invulnerable
    invulnerableStartTime = 0 # time the player became invulnerable
    gameOverMode = False      # if the player has lost
    gameOverStartTime = 0     # time the player lost
    winMode = False           # if the player has won

    gameOverSurf = BASICFONT.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALFSCREENWIDTH, HALFSCREENHEIGHT)

    winSurf = BASICFONT.render('You have achieved OMEGA ALIEN!', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALFSCREENWIDTH, HALFSCREENHEIGHT)

    camx=0
    camy=0

    playerObject = {
        "surface":PLAYERSURFACE,
        "facing":LEFT,
        "size":INITIAL_SIZE,
        "health":MAX_HEALTH,
        "x":HALFSCREENWIDTH,
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
            # move the enemies
            eObj['x'] += eObj['movex']
            eObj['y'] += eObj['movey']

       #      # random chance they change direction
        if random.randint(0, 99) < 2:
                eObj['movex'] = getRandomVelocity()
                eObj['movey'] = getRandomVelocity()

        for i in range (len(stars)-1,-1):   #see the below one
            if stars[i]['x'] not in range(camx-SCREENWIDTH,camx+3*SCREENWIDTH) and stars[i]['y'] not in range(camy-SCREENHEIGHT,camy+3*SCREENHEIGHT):
                del stars[i]
                #we have to delete the enemies as well
        for i in range (len(enemies)-1,-1,-1):
            if enemies[i]['x'] not in range(camx-SCREENWIDTH,camx+3*SCREENWIDTH) and enemies[i]['y'] not in range(camy-SCREENHEIGHT,camy+3*SCREENHEIGHT):
                del enemies[i]

                #append kar rahe h

        while len(stars) < NUM_STARS:
            stars.append(makeNewStar(camx,camy))

        while len(enemies) < NUM_ENEMY:
            enemies.append(makeNewEnemies(camx, camy))

        playerCenterx = playerObject['x'] + int(playerObject['size'] / 2)
        playerCentery = playerObject['y'] + int(playerObject['size'] / 2)
        if (camx + HALFSCREENWIDTH) - playerCenterx > CAMERASLACK:
            camx = playerCenterx + CAMERASLACK - HALFSCREENWIDTH
        elif playerCenterx - (camx + HALFSCREENWIDTH) > CAMERASLACK:
            camx = playerCenterx - CAMERASLACK - HALFSCREENWIDTH
        if (camy + HALFSCREENHEIGHT) - playerCentery > CAMERASLACK:
            camy = playerCentery + CAMERASLACK - HALFSCREENHEIGHT
        elif playerCentery - (camy + HALFSCREENHEIGHT) > CAMERASLACK:
            camy = playerCentery - CAMERASLACK - HALFSCREENHEIGHT

        for st in stars:
           #changes
            sRect = pygame.Rect(st['x']-camx,   #camx and camy change ho rha h
                                st['y']-camy,
                                st['width'],st['height'])
          #  print(st['x'])

            DISPLAYSURF.blit(STARSURFACE,sRect)
         #  emnemy squuirels banayi
        for eObj in enemies:                    #yha bhi chnages kiye enemies ka rect banaya    #yaha error aa rahi h pata nahi kyu
            eObj['rect'] = pygame.Rect((eObj['x'] - camx,
                                        eObj['y'] - camy,
                                        eObj['width'],
                                        eObj['height']))

            DISPLAYSURF.blit(eObj['surface'],(eObj['x'],eObj['y']))
            #yha pr player object ka rect banaya

            if not gameOverMode and not invulnerableMode:
                playerObject['rect'] = pygame.Rect((playerObject['x']-camx,    # x and y ki value define nahi ki
                                         playerObject['y']-camy,               #thi upar isliye error aa rahi thi
                                         playerObject['size'],
                                         playerObject['size']))

                DISPLAYSURF.blit(playerObject['surface'],playerObject['rect'])

            drawHealthMeter(playerObject['health'])         #Health meter niche define kiya h


        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                    if playerObject['x'] < camx + HALFSCREENWIDTH:
                        camx -= PLAYER_VELOCITY
                    #if playerObject['facing'] != LEFT: # change player image
                     #   playerObject['surface'] = pygame.transform.scale(PLAYERSURFACE, (playerObject['size'], playerObject['size']))
                    #playerObject['facing'] = LEFT
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True
                    #if playerObject['facing'] != RIGHT: # change player image
                    #    playerObject['surface'] = pygame.transform.scale(PLAYERSURFACE1, (playerObject['size'], playerObject['size']))
                    #playerObject['facing'] = RIGHT
                elif winMode and event.key == K_r:
                    return

            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                elif event.key in (K_RIGHT, K_d):
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False

                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not gameOverMode:
            # actually move the player
            if moveLeft:
                playerObject['x'] -= PLAYER_VELOCITY
            if moveRight:
                playerObject['x'] += PLAYER_VELOCITY
            if moveUp:
                playerObject['y'] -= PLAYER_VELOCITY
            if moveDown:
                playerObject['y'] += PLAYER_VELOCITY

            for i in range(len(enemies) - 1, -1, -1):   #colliding function
                eObj = enemies[i]
                if 'rect' in eObj and playerObject['rect'].colliderect(eObj['rect']):
                    # player/enemy collision has occurred

                    if eObj['width'] * eObj['height'] <= playerObject['size'] ** 2:
                        # player is larger and eats the squirrel
                        playerObject['size'] += int((eObj['width'] * eObj['height']) ** 0.2 )+1
                        del enemies[i]
                        playerObject['surface']=pygame.transform.scale(PLAYERSURFACE,(playerObject['size'],playerObject['size']))

                        if playerObject['size'] > WIN_SIZE:
                            winMode = True  # turn on "win mode"

                    elif not invulnerableMode:
                            # player is smaller and takes damage
                            invulnerableMode = True
                            invulnerableStartTime = time.time()
                            playerObject['health'] -= 1
                            if playerObject['health'] == 0:
                                gameOverMode = True  # turn on "game over mode"
                                gameOverStartTime = time.time()

        if winMode :
            DISPLAYSURF.blit(winSurf,winRect)
        elif gameOverMode:
            DISPLAYSURF.blit(gameOverSurf,gameOverRect)







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
    eObj['width']  = (generalSize * random.randint(1, 3))
    eObj['height'] = (generalSize * random.randint(1, 3))
    eObj['x'], eObj['y'] = cord_inactive(camx, camy, eObj['width'], eObj['height'])
    eObj['movex'] = getRandomVelocity()
    eObj['movey'] = getRandomVelocity()
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