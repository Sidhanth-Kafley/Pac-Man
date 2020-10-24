import pygame
import pygame_gui
import sys
import os
from PacMan import PacMan
pygame.init()

MAX_HEIGHT = 480
MAX_WIDTH = 720
BACKGROUND_COLOR = pygame.Color('black')


def loadImages(path):
    images = []
    for file in os.listdir(path):
        image = pygame.image.load(path + os.sep + file).convert()
        images.append(image)
    return images


def main():
    pygame.display.set_caption('Main Screen')
    window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(BACKGROUND_COLOR)

    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    pacMan = PacMan(position=(100, 100), images=loadImages(path='Pac_Man_Sprites'))
    pacManSprite = pygame.sprite.Group(pacMan)
    pacManSprite.draw(window)

    clock = pygame.time.Clock()
    isRunning = True

    while isRunning:
        # updates at 60 FPS
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacMan.velocity.y = 0
                        pacMan.velocity.x = -4
                    elif event.key == pygame.K_RIGHT:
                        pacMan.velocity.y = 0
                        pacMan.velocity.x = 4
                    elif event.key == pygame.K_UP:
                        pacMan.velocity.x = 0
                        pacMan.velocity.y = -4
                    elif event.key == pygame.K_DOWN:
                        pacMan.velocity.x = 0
                        pacMan.velocity.y = 4

            manager.process_events(event)

        # update the sprite
        pacManSprite.update()
        # update the image on screen
        pacManSprite.draw(window)

        manager.update(time_delta)
        window.blit(background, (0, 0))
        manager.draw_ui(window)

        pygame.display.update()

    sys.exit(0)


if __name__ == '__main__':
    main()
