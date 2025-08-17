import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawtext(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
gameOverSound = pygame.mixer.Sound('gameover.wav')

playerRect = pygame.Rect(WINDOWWIDTH // 2 - 20, WINDOWHEIGHT - 60, 40, 40)

windowSurface.fill(BACKGROUNDCOLOR)
drawtext('Dodger', font, windowSurface, WINDOWWIDTH // 3, WINDOWHEIGHT // 3)
drawtext('Press a key to start.', font, windowSurface, (WINDOWWIDTH // 3) - 30, (WINDOWHEIGHT // 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topscore = 0
while True:
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH // 2 - 20, WINDOWHEIGHT - 60)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_p:
                    paused = not paused
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]

        if paused:
            drawtext('Paused', font, windowSurface, WINDOWWIDTH // 2 - 50, WINDOWHEIGHT // 2)
            pygame.display.update()
            mainClock.tick(FPS)
            continue  # Skip the rest of the loop to freeze the game

        score += 1

        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1

        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {
                'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            }
            baddies.append(newBaddie)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        windowSurface.fill(BACKGROUNDCOLOR)
        drawtext(f'Score: {score}', font, windowSurface, 10, 0)
        drawtext(f'Top score: {topscore}', font, windowSurface, 10, 40)

        pygame.draw.rect(windowSurface, (0, 0, 255), playerRect)  # blue player

        for b in baddies:
            pygame.draw.rect(windowSurface, (255, 0, 0), b['rect'])  # red baddies

        pygame.display.update()

        if playerHitBaddie(playerRect, baddies):
            if score > topscore:
                topscore = score
            break

        mainClock.tick(FPS)

    gameOverSound.play()
    drawtext('Game over', font, windowSurface, WINDOWWIDTH // 3, WINDOWHEIGHT // 3)
    drawtext('Press a key to play again.', font, windowSurface, (WINDOWWIDTH // 3) - 80, (WINDOWHEIGHT // 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()
