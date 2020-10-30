import pygame
import pygame_gui
import sys
import os
from PacMan import PacMan
from ghost import Ghost
from Wall import Wall
from Level import Level
pygame.init()

MAX_HEIGHT = 700
MAX_WIDTH = 900
BACKGROUND_COLOR = pygame.Color('black')


def loadImages(path):
    images = []
    for file in os.listdir(path):
        image = pygame.image.load(path + os.sep + file).convert_alpha()
        image = pygame.transform.scale(image, (64, 64))
        images.append(image)
    return images


def main():
    # Initiate game and window
    pygame.display.set_caption('Pac-Man')
    window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(BACKGROUND_COLOR)
    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    # create pacman object
    images = loadImages(path='PacManSprites')
    pacMan = PacMan(position=(100, 100), images=images)

    # create test wall object


    # create test level object
    level1 = Level(layoutFilename='Levels/level1alt.txt', wallSize=(16, 16))

    # create blue ghost object
    blueGhostImages = loadImages(path='BlueGhostSprites')
    blueGhost = Ghost('blue', position=(400, 200), images=blueGhostImages)

    # create orange ghost object
    orangeGhostImages = loadImages(path='OrangeGhostSprites')
    orangeGhost = Ghost('orange', position=(350, 200), images=orangeGhostImages)

    # create pink ghost object
    pinkGhostImages = loadImages(path='PinkGhostSprites')
    pinkGhost = Ghost('pink', position=(450, 200), images=pinkGhostImages)

    # create red ghost object
    redGhostImages = loadImages(path='RedGhostSprites')
    redGhost = Ghost('red', position=(500, 200), images=redGhostImages)

    # health bar at the bottom of the screen
    healthBar = pygame.transform.scale(images[0], (32, 32))

    # ADD GHOSTS TO THIS GROUP SO THEY ALL FOLLOW THE SAME BASIC GUIDELINES
    allSprites = pygame.sprite.Group(pacMan, blueGhost, orangeGhost, pinkGhost, redGhost, level1.walls)

    # clock used for framerate
    clock = pygame.time.Clock()
    isRunning = True

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

        manager.update(time_delta)
        window.blit(background, (0, 0))
        manager.draw_ui(window)

        # display the health bar at the top
        if PacMan.startingHealth - 1 == 2:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
            window.blit(healthBar, (50, MAX_HEIGHT - 50))
        elif PacMan.startingHealth - 1 == 1:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))

        # else:
        #     displayGameOver()

        # display score
        window.blit(pacMan.renderScore(), (10, 10))

        # ensures that the pacMan won't go off screen
        pacMan.rect.clamp_ip(windowRect)
        # update the sprite
        allSprites.update()
        # update the image on screen
        allSprites.draw(window)

        pygame.display.update()

    sys.exit(0)


if __name__ == '__main__':
    main()
