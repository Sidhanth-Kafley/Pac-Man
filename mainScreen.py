import pygame
import pygame_gui
import sys
import os
from PacMan import PacMan
from ghost import Ghost
from pygame.locals import *
from pill import Pill
from Wall import Wall
from Level import Level

pygame.init()

MAX_HEIGHT = 800
MAX_WIDTH = 1000
BACKGROUND_COLOR = pygame.Color('black')
SPRITE_SIZE = 36

click = False
mainClock = pygame.time.Clock()
font = pygame.font.Font('8-BIT WONDER.TTF', 20)
titleFont = pygame.font.Font('8-BIT WONDER.TTF', 30)


pygame.display.set_caption('Pac Man')
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT), 0, 32)


# function to draw text onto the screen
def drawText(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (int(x), int(y))
    surface.blit(textObj, textRect)


def main():
    mainMenu()


def mainMenu():
    running = True
    global click
    click = False
    
    while running:

        screen.fill(BACKGROUND_COLOR)
        drawText('main menu', titleFont, (255, 255, 255), screen, MAX_HEIGHT/2.5, MAX_WIDTH/4)

        # get mousePosition for collision detection
        mousePosition = pygame.mouse.get_pos()

        # create buttons
        button1 = pygame.Rect(int(MAX_HEIGHT/2.5), int(MAX_WIDTH/3.0), 250, 50)
        button2 = pygame.Rect(int(MAX_HEIGHT/2.5), int(MAX_WIDTH/2.4), 250, 50)

        # if button is clicked call corresponding functions
        if button2.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                credits()

        if button1.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                game()

        # draw buttons and add hover effect
        # got logic for button hovering from pythonprogramming.net
        if MAX_HEIGHT/2.5+250 > mousePosition[0] > MAX_HEIGHT/2.5 and MAX_WIDTH/3.0+50 > mousePosition[1] > MAX_WIDTH/3.0:
            pygame.draw.rect(screen, (0, 190, 0), button1)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button1)

        drawText('start game', font, (255, 255, 255), screen, MAX_HEIGHT/2.3, MAX_WIDTH/2.9)

        if MAX_HEIGHT/2.5+250 > mousePosition[0] > MAX_HEIGHT/2.5 and MAX_WIDTH/2.4+50 > mousePosition[1] > MAX_WIDTH/2.4:
            pygame.draw.rect(screen, (0, 190, 0), button2)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button2)

        drawText('Credits', font, (255, 255, 255), screen, MAX_HEIGHT/2.2, MAX_WIDTH/2.32)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def loadImages(path):
    images = []
    if path == 'PacManSprites':
        images = [0, 0, 0, 0, 0]
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert_alpha()
            image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
            if 'Down' in file:
                images[0] = image
            elif 'Left' in file:
                images[1] = image
            elif 'Right' in file:
                images[2] = image
            elif 'Up' in file:
                images[3] = image
            elif 'Closed' in file:
                images[4] = image
    elif 'GhostSprites' in path:
        images = [0, 0, 0, 0, 0]
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert_alpha()
            image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
            if 'Down' in file:
                images[0] = image
            elif 'Left' in file:
                images[1] = image
            elif 'Right' in file:
                images[2] = image
            elif 'Up' in file:
                if 'Power' in file:
                    images[4] = image
                else:
                    images[3] = image
    return images


def credits():
    isRunning = True
    while isRunning:
        screen.fill((BACKGROUND_COLOR))
        drawText('Game made by', titleFont, (255, 255, 255), screen, 300, 250)
        drawText('Jaden Varin', font, (255, 255, 255), screen, 350, 340)
        drawText('Michelle Wehrle', font, (255, 255, 255), screen, 350, 380)
        drawText('Sidhanth Kafley', font, (255, 255, 255), screen, 350, 420)
        drawText('Cam Brown', font, (255, 255, 255), screen, 350, 460)

        mousePosition = pygame.mouse.get_pos()
        button = pygame.Rect(350, 540, 250, 50)

        if button.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                isRunning = False

        if 270+250 > mousePosition[0] > 270 and 300+50 > mousePosition[1] > 300:
            pygame.draw.rect(screen, (0, 190, 0), button)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button)

        drawText('Main Menu', font, (255, 255, 255), screen, 370, 555)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                isRunning = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(10)

def game():
    # Initiate game and window
    pygame.init()
    window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(BACKGROUND_COLOR)
    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    pillImage = pygame.image.load("PointPill.png").convert_alpha()
    pillImage = pygame.transform.scale(pillImage, (int(SPRITE_SIZE/3), int(SPRITE_SIZE/3)))

    # create pacman object
    images = loadImages(path='PacManSprites')

    pacMan = PacMan(position=(MAX_WIDTH/5, (MAX_HEIGHT/2)+5), images=images)
    
    # create level object
    level1 = Level(layoutFilename='Levels/level1alt.txt', wallSize=(16, 16), originPosition=(200, 70))

    pillGroup = pygame.sprite.Group(level1.pills)

    ghosts = []
    # create blue ghost object
    blueGhostImages = loadImages(path='BlueGhostSprites')
    blueGhost = Ghost('blue', position=(500, 390), images=blueGhostImages)
    ghosts.append(blueGhost)

    # create orange ghost object
    orangeGhostImages = loadImages(path='OrangeGhostSprites')
    orangeGhost = Ghost('orange', position=(465, 390), images=orangeGhostImages)
    ghosts.append(orangeGhost)

    # create pink ghost object
    pinkGhostImages = loadImages(path='PinkGhostSprites')
    pinkGhost = Ghost('pink', position=(430, 390), images=pinkGhostImages)
    ghosts.append(pinkGhost)

    # create red ghost object
    redGhostImages = loadImages(path='RedGhostSprites')
    redGhost = Ghost('red', position=(465, 320), images=redGhostImages)
    ghosts.append(redGhost)

    # health bar at the top of the screen
    healthBar = pygame.transform.scale(images[2], (int(24), int(24)))

    # ADD GHOSTS TO THIS GROUP SO THEY ALL FOLLOW THE SAME BASIC GUIDELINES
    allSprites = pygame.sprite.Group(pacMan, blueGhost, orangeGhost, pinkGhost, redGhost, level1.walls)

    # clock used for framerate
    clock = pygame.time.Clock()
    isRunning = True

    # start main background music
    backgroundMusic = pygame.mixer.Sound("Music/PacManBeginning.wav")
    backgroundMusic.play(0)

    while isRunning:
        # times per second this loop runs
        time_delta = clock.tick_busy_loop(60) / 1000.0

        # determine if a wall is colliding
        collidingWallTop = False
        collidingWallBottom = False
        collidingWallLeft = False
        collidingWallRight = False
        collidingWalls = pacMan.rect.collidelistall(level1.walls)
        for wallIndex in collidingWalls:
            if level1.walls[wallIndex].rect.left >= pacMan.rect.right:
                collidingWallRight = True
            elif level1.walls[wallIndex].rect.right <= pacMan.rect.left:
                collidingWallLeft = True
            elif level1.walls[wallIndex].rect.top >= pacMan.rect.bottom:
                collidingWallBottom = True
            elif level1.walls[wallIndex].rect.bottom <= pacMan.rect.top:
                collidingWallTop = True

        # handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacMan.velocity.y = 0
                    pacMan.velocity.x = (-4)*pacMan.powerUp
                elif event.key == pygame.K_RIGHT:
                    pacMan.velocity.y = 0
                    pacMan.velocity.x = 4*pacMan.powerUp
                elif event.key == pygame.K_UP:
                    pacMan.velocity.x = 0
                    pacMan.velocity.y = (-4)*pacMan.powerUp
                elif event.key == pygame.K_DOWN:
                    pacMan.velocity.x = 0
                    pacMan.velocity.y = 4*pacMan.powerUp

            manager.process_events(event)

        #if collidingWallRight:
         #   pacMan.velocity.x = min(0, (-4)*pacMan.powerUp)
        #elif collidingWallLeft:
         #   pacMan.velocity.x = max(0, 4 * pacMan.powerUp)
        #elif collidingWallTop:
         #   pacMan.velocity.y = max(0, 4 * pacMan.powerUp)
        #elif collidingWallBottom:
         #   pacMan.velocity.x = min(0, (-4) * pacMan.powerUp)

        if pygame.sprite.spritecollide(pacMan, ghosts, False):
            if pacMan.powerUp == 1:
                pacManDeath = pygame.mixer.Sound("Music/PacManDeath.wav")
                pacManDeath.play(0)
                pacMan.deathAnimation()
            else:
                pacManEatGhost = pygame.mixer.Sound("Music/PacManEatGhost.wav")
                pacManEatGhost.play(0)
                for x in ghosts:
                    if pacMan.rect.colliderect(x.rect):
                        pacMan.eatGhost(x)

        if pygame.sprite.spritecollide(pacMan, pillGroup, False):
            # pygame.sprite.
            pacManChomp = pygame.mixer.Sound("Music/PacManChomp.wav")
            pacManChomp.play(0)
            for x in pillGroup:
                if pacMan.rect.colliderect(x.rect):
                    if pacMan.eatPill(x):
                        for ghost in ghosts:
                            ghost.setPowerUpMode()
                    pillGroup.remove(x)

        manager.update(time_delta)
        window.blit(background, (0, 0))
        manager.draw_ui(window)

        # display the health bar at the bottom
        if pacMan.startingHealth - 1 == 2:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
            window.blit(healthBar, (50, MAX_HEIGHT - 50))
        elif pacMan.startingHealth - 1 == 1:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
        elif pacMan.startingHealth == 0:
            displayGameOver(pacMan, window)

        # display score
        window.blit(pacMan.renderScore(32), (10, 10))

        # inefficient collision for testing, should be handled in PacMan movement code instead
        # for wall in level1.walls:
        #     wall.collision(pacMan)

        # ensures that the pacMan and ghosts won't go off screen
        pacMan.rect.clamp_ip(windowRect)
        blueGhost.rect.clamp_ip(windowRect)
        orangeGhost.rect.clamp_ip(windowRect)
        pinkGhost.rect.clamp_ip(windowRect)
        redGhost.rect.clamp_ip(windowRect)

        pillGroup.draw(window)
        # update the sprite
        allSprites.update()
        # update the image on screen
        allSprites.draw(window)

        pygame.display.update()

    pygame.mixer.music.stop()
    sys.exit(0)
    #mainClock.tick(10)


def displayGameOver(pacMan, window):
    # display button to play again
    click = False
    isRunning = True
    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('GameOver', titleFont, (255, 255, 255), screen, 340, 250)
        window.blit(pacMan.renderScore(100), (440, 380))
        mousePosition = pygame.mouse.get_pos()
        button = pygame.Rect(340, 500, 250, 50)

        if button.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                game()

        if 270+250 > mousePosition[0] > 270 and 300+50 > mousePosition[1] > 300:
            pygame.draw.rect(screen, (0, 190, 0), button)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button)

        drawText('Play again', font, (255, 255, 255), screen, 360, 515)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(10)


if __name__ == '__main__':
    main()
