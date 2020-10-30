import pygame
import pygame_gui
import sys
import os
from PacMan import PacMan
from ghost import Ghost
from pygame.locals import *

pygame.init()

MAX_HEIGHT = 800
MAX_WIDTH = 1000
BACKGROUND_COLOR = pygame.Color('black')

mainClock = pygame.time.Clock()

pygame.display.set_caption('Pac Man')
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT), 0, 32)

font = pygame.font.Font('8-BIT WONDER.TTF', 20)


def drawText(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main():
    while True:

        screen.fill((BACKGROUND_COLOR))
        titleFont = pygame.font.Font('8-BIT WONDER.TTF', 30)
        drawText('main menu', titleFont, (255, 255, 255), screen, 270, 220)

        mousePosition = pygame.mouse.get_pos()

        button_1 = pygame.Rect(270, 300, 250, 50)
        button_2 = pygame.Rect(270, 400, 250, 50)

        if button_2.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                credits()

        if button_1.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                game()



        if 270+250 > mousePosition[0] > 270 and 300+50 > mousePosition[1] > 300:
            pygame.draw.rect(screen, (0, 190, 0), button_1)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button_1)

        drawText('start game', font, (255, 255, 255), screen, 290, 315)


        if 270+250 > mousePosition[0] > 270 and 400+50 > mousePosition[1] > 400:
            pygame.draw.rect(screen, (0, 190, 0), button_2)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button_2)

        drawText('Credits', font, (255, 255, 255), screen, 290, 415)

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
        mainClock.tick(10)


def loadImages(path):
    images = []
    if path == 'PacManSprites':
        images = [0, 0, 0, 0, 0]
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
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
            image = pygame.transform.scale(image, (64, 64))
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
        titleFont = pygame.font.Font('8-BIT WONDER.TTF', 30)
        drawText('Game made by', titleFont, (255, 255, 255), screen, 250, 250)
        drawText('Jaden Varin', font, (255, 255, 255), screen, 300, 300)
        drawText('Michelle Wehrle', font, (255, 255, 255), screen, 300, 340)
        drawText('Sidhanth Kafley', font, (255, 255, 255), screen, 300, 380)
        drawText('Cam Brow', font, (255, 255, 255), screen, 300, 420)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False

        pygame.display.update()
        mainClock.tick(10)


def game():
    # Initiate game and window
    window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(BACKGROUND_COLOR)
    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    # create pacman object
    images = loadImages(path='PacManSprites')
    pacMan = PacMan(position=(100, 100), images=images)

    ghosts = []
    # create blue ghost object
    blueGhostImages = loadImages(path='BlueGhostSprites')
    blueGhost = Ghost('blue', position=(400, 200), images=blueGhostImages)
    ghosts.append(blueGhost)

    # create orange ghost object
    orangeGhostImages = loadImages(path='OrangeGhostSprites')
    orangeGhost = Ghost('orange', position=(350, 200), images=orangeGhostImages)
    ghosts.append(orangeGhost)

    # create pink ghost object
    pinkGhostImages = loadImages(path='PinkGhostSprites')
    pinkGhost = Ghost('pink', position=(450, 200), images=pinkGhostImages)
    ghosts.append(pinkGhost)

    # create red ghost object
    redGhostImages = loadImages(path='RedGhostSprites')
    redGhost = Ghost('red', position=(500, 200), images=redGhostImages)
    ghosts.append(redGhost)

    # health bar at the top of the screen
    healthBar = pygame.transform.scale(images[2], (32, 32))

    # ADD GHOSTS TO THIS GROUP SO THEY ALL FOLLOW THE SAME BASIC GUIDELINES
    allSprites = pygame.sprite.Group(pacMan, blueGhost, orangeGhost, pinkGhost, redGhost)

    # clock used for framerate
    clock = pygame.time.Clock()
    isRunning = True

    # start main background music
    backgroundMusic = pygame.mixer.Sound("Music/PacManBeginning.wav")
    backgroundMusic.play(-1)

    while isRunning:
        # times per second this loop runs
        time_delta = clock.tick(60) / 1000.0

        # handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacMan.velocity.y = 0
                    pacMan.velocity.x = (-10)*pacMan.powerUp
                elif event.key == pygame.K_RIGHT:
                    pacMan.velocity.y = 0
                    pacMan.velocity.x = 10*pacMan.powerUp
                elif event.key == pygame.K_UP:
                    pacMan.velocity.x = 0
                    pacMan.velocity.y = -10*pacMan.powerUp
                elif event.key == pygame.K_DOWN:
                    pacMan.velocity.x = 0
                    pacMan.velocity.y = 10*pacMan.powerUp


            manager.process_events(event)

        if pygame.sprite.spritecollide(pacMan, ghosts, False):
            pacManDeath = pygame.mixer.Sound("Music/PacManDeath.wav")
            pacManDeath.play(0)
            pacMan.deathAnimation()

        manager.update(time_delta)
        window.blit(background, (0, 0))
        manager.draw_ui(window)

        # display the health bar at the bottom
        if pacMan.startingHealth - 1 == 2:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
            window.blit(healthBar, (50, MAX_HEIGHT - 50))
        elif pacMan.startingHealth - 1 == 1:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
        # elif pacMan.startingHealth == 0:
        #     displayGameOver(pacMan, window)

        # display score
        window.blit(pacMan.renderScore(24), (10, 10))

        # ensures that the pacMan and ghosts won't go off screen
        pacMan.rect.clamp_ip(windowRect)
        blueGhost.rect.clamp_ip(windowRect)
        orangeGhost.rect.clamp_ip(windowRect)
        pinkGhost.rect.clamp_ip(windowRect)
        redGhost.rect.clamp_ip(windowRect)

        # update the sprite
        allSprites.update()
        # update the image on screen
        allSprites.draw(window)

        pygame.display.update()

    pygame.mixer.music.stop()
    sys.exit(0)
    #mainClock.tick(10)


def displayGameOver(pacMan, window):
    # Make Button with x for exiting
    text = pygame.font.SysFont('Arial', 35) .render('X', True, (25, 25, 166))
    # exit = pygame_gui.elements.ui_button()
    # display the score in the center of the screen
    window.blit(pacMan.renderScore(50), (MAX_HEIGHT/2, MAX_WIDTH/2))
    # display button to play again


if __name__ == '__main__':
    main()
