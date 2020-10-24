import pygame
import pygame_gui
import sys
import os
from PacMan import PacMan
pygame.init()

MAX_HEIGHT = 700
MAX_WIDTH = 900
BACKGROUND_COLOR = pygame.Color('black')


def loadImages(path):
    images = []
    for file in os.listdir(path):
        image = pygame.image.load(path + os.sep + file).convert()
        images.append(image)
    ims = []
    for x in images:
        im = pygame.transform.scale(x, (64, 64))
        ims.append(im)
    return ims


def main():
    # Initiate game and window
    pygame.display.set_caption('Pac-Man')
    window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(BACKGROUND_COLOR)
    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    # create pacman object
    pacMan = PacMan(position=(100, 100), images=loadImages(path='Pac_Man_Sprites'))

    # ADD GHOSTS TO THIS GROUP SO THEY ALL FOLLOW THE SAME BASIC GUIDELINES
    allSprites = pygame.sprite.Group(pacMan)

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
