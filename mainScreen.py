import pygame
import pygame_gui
import time
import sys
import os
from PacMan import PacMan
from ghost import Ghost
from pill import Pill
from Wall import Wall
from Level import Level

pygame.init()

MAX_HEIGHT = 800
MAX_WIDTH = 1000
BACKGROUND_COLOR = pygame.Color('black')
SPRITE_SIZE = 48


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


def main():
    # Initiate game and window
    pygame.display.set_caption('Pac-Man')
    window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(BACKGROUND_COLOR)
    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    pillImage = pygame.image.load("PointPill.png").convert_alpha()
    pillImage = pygame.transform.scale(pillImage, (int(SPRITE_SIZE/3), int(SPRITE_SIZE/3)))
    i = 0
    pills = []
    while i < 10:
        pills.append(Pill(False, pillImage, (10 + i, 100)))
        i += 1
    pillGroup = pygame.sprite.Group(pills)

    # create pacman object
    images = loadImages(path='PacManSprites')
    pacMan = PacMan(position=(MAX_WIDTH/2, MAX_HEIGHT/2), images=images)
    
    #create level object
    level1 = Level(layoutFilename='Levels/level1alt.txt', wallSize=(16, 16))

    ghosts = []
    # create blue ghost object
    blueGhostImages = loadImages(path='BlueGhostSprites')
    blueGhost = Ghost('blue', position=(255, 310), images=blueGhostImages)
    ghosts.append(blueGhost)

    # create orange ghost object
    orangeGhostImages = loadImages(path='OrangeGhostSprites')
    orangeGhost = Ghost('orange', position=(290, 310), images=orangeGhostImages)
    ghosts.append(orangeGhost)

    # create pink ghost object
    pinkGhostImages = loadImages(path='PinkGhostSprites')
    pinkGhost = Ghost('pink', position=(220, 310), images=pinkGhostImages)
    ghosts.append(pinkGhost)

    # create red ghost object
    redGhostImages = loadImages(path='RedGhostSprites')
    redGhost = Ghost('red', position=(255, 250), images=redGhostImages)
    ghosts.append(redGhost)


    # health bar at the top of the screen
    healthBar = pygame.transform.scale(images[2], (int(SPRITE_SIZE/2), int(SPRITE_SIZE/2)))

    # ADD GHOSTS TO THIS GROUP SO THEY ALL FOLLOW THE SAME BASIC GUIDELINES
    allSprites = pygame.sprite.Group(pacMan, blueGhost, orangeGhost, pinkGhost, redGhost, level1.walls)

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
            if pacMan.powerUp == 1:
                pacManDeath = pygame.mixer.Sound("Music/PacManDeath.wav")
                pacManDeath.play(0)
                pacMan.deathAnimation()
            else:
                pacManEatGhost = pygame.mixer.Sound("Music/PacManEatGhost.wav")
                pacManEatGhost.play(0)
                # CODE TO EAT THE GHOST GOES HERE
                # pacMan.eatGhost(EATEN GHOST GOES HERE)

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

        pillGroup.draw(window)
        # update the sprite
        allSprites.update()
        # update the image on screen
        allSprites.draw(window)

        pygame.display.update()

    pygame.mixer.music.stop()
    sys.exit(0)


def displayGameOver(pacMan, window):
    # Make Button with x for exiting
    text = pygame.font.SysFont('Arial', 35) .render('X', True, (25, 25, 166))
    # exit = pygame_gui.elements.ui_button()
    # display the score in the center of the screen
    window.blit(pacMan.renderScore(50), (MAX_HEIGHT/2, MAX_WIDTH/2))
    # display button to play again


if __name__ == '__main__':
    main()
