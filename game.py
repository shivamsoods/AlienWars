import pygame,sys,random,time
from pygame.locals import *

FPS=30
SCREENWIDTH=640
SCREENHEIGHT=480

NUM_ENEMY = 30
NUM_STARS = 80

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



DIS=100




def main():

    global PLAYERSURFACE,DISPLAYSURF,STARSURFACE,CLOCK

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
    pygame.display.set_caption("Game")
    pygame.display.set_icon(pygame.image.load("pikachu.png"))
    CLOCK = pygame.time.Clock()

    PLAYERSURFACE=pygame.image.load("alien.png")
    STARSURFACE=pygame.image.load("star.png")

    while True:
        runGame()

def runGame():
    camx=0
    camy=0
    movex = (camx + SCREENWIDTH) / 2
    movey = (camy + SCREENHEIGHT) / 2
    playerObject = {
        "surface":PLAYERSURFACE,
        "facing":LEFT,
        "size":INITIAL_SIZE,
        "health":MAX_HEALTH,
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

        for st in stars:
          #  print(st['x'])
            DISPLAYSURF.blit(STARSURFACE,(st['x'],st['y']))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if playerObject['facing']!=LEFT:
                        pygame.transform.flip(PLAYERSURFACE,False,True)
                        playerObject['facing']=LEFT

                    movex -= PLAYER_VELOCITY
                    if movex < camx+50 :
                        camx -= PLAYER_VELOCITY

                if event.key == pygame.K_RIGHT:
                    if playerObject['facing']!=RIGHT:
                        pygame.transform.flip(PLAYERSURFACE,False,True)
                        playerObject['facing']=RIGHT

                    movex += PLAYER_VELOCITY
                    if movex> camx+SCREENWIDTH-50:
                        camx += PLAYER_VELOCITY

                if event.key == pygame.K_UP:
                    movey -= PLAYER_VELOCITY

                    if movey < camy+50 :
                        camy -= PLAYER_VELOCITY

                if event.key == pygame.K_DOWN:
                    movey += PLAYER_VELOCITY

                    if movey> camx+SCREENHEIGHT-50 :
                        camy += PLAYER_VELOCITY

                if event.key== pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()




        pygame.display.update()
        CLOCK.tick(FPS)

        while len(stars)<NUM_STARS:
            stars.append(makeNewStar(camx,camy))

        for i in range (len(stars)-1,0):
            if stars[i]['x'] not in range(camx-SCREENWIDTH,camx+2*SCREENWIDTH) and stars[i]['y'] not in range(camy-SCREENHEIGHT,camy+2*SCREENHEIGHT):
                del stars[i]
        DISPLAYSURF.blit(PLAYERSURFACE, (movex, movey))





def makeNewStar(camx,camy):
    st = {}
    st["width"] = STARSURFACE.get_width()
    st["height"]= STARSURFACE.get_height()
    st['x'], st['y'] = cord_inactive(camx,camy)
    st['rect'] = pygame.Rect(st['x'], st['y'], st['width'], st['height'])
    return st

def cord_inactive(camx, camy):

    while True:
        x = random.randint(camx-SCREENWIDTH, camx+2*SCREENWIDTH)
        y=random.randint(camy-SCREENHEIGHT, camy+2*SCREENHEIGHT)
        if (x < camx or x >camx+SCREENWIDTH) and (y <camy or y>camy + SCREENHEIGHT):
            # st['x'] = x
            # st['y'] = y
            return x,y

if __name__ == '__main__':
    main()