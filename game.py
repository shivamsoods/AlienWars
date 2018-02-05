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
WIN_SIZE=300

PLAYER_VELOCITY = 9
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

    winSurf = BASICFONT.render('You won!', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALFSCREENWIDTH, HALFSCREENHEIGHT)

    camx=0
    camy=0

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

    for i in range(10):
        stars.append(makeNewStar(camx,camy))
        stars[i]['x'] = random.randint(camx,camx + SCREENWIDTH)
        stars[i]['y']= random.randint(camy,camy + SCREENHEIGHT)

    while True:
        DISPLAYSURF.fill(BLACK)  # global
       # print("hi")
        for eObj in enemies:
            # move the enemies
            eObj['x'] += eObj['movex']
            eObj['y'] += eObj['movey']
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

        while len(stars)<NUM_STARS:
            stars.append(NewStar(camx,camy))

        while len(enemies) < NUM_ENEMY:         #jaise stars append kiye the wese hi enemies append kar rahe h frame me
            enemies.append(NewEnemies(camx, camy))

        
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




            for i in range(len(enemies) - 1, -1, -1):   #colliding function
                eObj = enemies[i]
                if 'rect' in eObj and playerObject['rect'].colliderect(eObj['rect']):
                    # player/enemy collision has occurred

                    if eObj['width'] * eObj['height'] <= playerObject['size'] ** 2:
                        # player is larger and eats the squirrel
                        playerObject['size'] += int((eObj['width'] * eObj['height']) ** 0.2) + 1
                        del enemies[i]

                        if playerObject['size'] > WIN_SIZE:
                            winMode = True  # turn on "win mode"
                        elif not invulnerableMode:
                            # player is smaller and takes damage
                            invulnerableMode = True
                            playerObject['health'] -= 1
                            if playerObject['health'] == 0:
                                gameOverMode = True  # turn on "game over mode"
                              


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN or event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if pygame.key.get_pressed()[K_LEFT]:
                    if playerObject['facing']!=LEFT: # iski wajah se left right move nahi kar raha tha don't know why
                       # playerObject['surface'] = pygame.transform.scale(PLAYERSURFACE,
                                                                     # (playerObject['size'], playerObject['size']))
                        #pygame.transform.flip(PLAYERSURFACE,False,True)  # yaha changes honge
                        playerObject['facing']=LEFT
                    playerObject['x'] -= PLAYER_VELOCITY
                    # movex -= PLAYER_VELOCITY ye nahi hoga
                    if playerObject['x'] < camx+HALFSCREENWIDTH :
                       camx -= PLAYER_VELOCITY
        
                if pygame.key.get_pressed()[K_RIGHT]:
                    if playerObject['facing']!=RIGHT:
                        #pygame.transform.flip(PLAYERSURFACE,False,True)
        
                        playerObject['facing']=RIGHT
                    playerObject['x'] += PLAYER_VELOCITY
                    #movex += PLAYER_VELOCITY
                    if playerObject['x']> camx+HALFSCREENWIDTH:
                        camx += PLAYER_VELOCITY
        
                if pygame.key.get_pressed()[K_UP]:
                   # movey -= PLAYER_VELOCITY
                   playerObject['y'] -= PLAYER_VELOCITY
        
                #if movey < camy+50 : yaha 50 ki jagah halfscreenheight le li
                if playerObject['y'] < camy+HALFSCREENHEIGHT:
                        camy -= PLAYER_VELOCITY
        
                if pygame.key.get_pressed()[K_DOWN]:
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

        pygame.display.update()
        CLOCK.tick(FPS)



def NewStar(camx,camy):
    st = {}
    st["width"] = STARSURFACE.get_width()
    st["height"]= STARSURFACE.get_height()
    st['x'], st['y'] = cord_inactive(camx,camy,st['width'],st['height'])
    st['rect'] = pygame.Rect(st['x'], st['y'], st['width'], st['height'])
    return st

def NewEnemies(camx, camy):    #yaha par enemies banaye
    eObj = {}
    generalSize = random.randint(15, 25)
    multiplier = random.randint(2, 5)
    eObj['width']  = (generalSize + random.randint(0, 10)) * multiplier
    eObj['height'] = (generalSize + random.randint(0, 10)) * multiplier
    eObj['x'], eObj['y'] = cord_inactive(camx, camy, eObj['width'], eObj['height'])
    eObj['movex'] = getRandomVelocity()
    eObj['movey'] = getRandomVelocity()

def getRandomVelocity():
    speed = random.randint(ENEMY_VEL_MIN, ENEMY_VEL_MAX)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed

def drawHealthMeter(currentHealth):
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(DISPLAYSURF, RED,   (10, 10 + (5 * MAX_HEALTH) - i * 10, 20, 10))
    for i in range(MAX_HEALTH): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (10, 10 + (5 * MAX_HEALTH) - i * 10, 20, 10), 1)


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
