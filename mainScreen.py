import pygame
import pygame_gui
import PacMan
import sys

MAX_HEIGHT = 800
MAX_WIDTH = 1000

def main():
    pygame.init()

    pygame.display.set_caption('Main Screen')
    windowSurface = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))

    background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

    # hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
    #                                             text='Say Hello',
    #                                             manager=manager)

    pacMan = PacMan(position=(100, 100), images=images)
    pacManSprite = pygame.sprite.Group(pacMan)
    pacManSprite.draw(windowSurface)

    clock = pygame.time.Clock()
    isRunning = True

    while isRunning:
        time_delta = clock.tick(60) / 1000.0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            #move = pygame.key.get_pressed()

            if event.type == pygame.USEREVENT:
                # if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # if event.ui_element == hello_button:
                    #     print('Hello World!')
                if event.user_type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacMan.setMotionDirection("left")
                        pacManSprite.update()
                        pacManSprite.draw(windowSurface)
                        pygame.display.flip()



                    if event.key == pygame.K_RIGHT:
                        pacMan.setMotionDirection("right")
                        pacManSprite.update()
                        pacManSprite.draw(windowSurface)
                        pygame.display.flip()
                    if event.key == pygame.K_UP:
                        pacMan.setMotionDirection("up")
                        pacManSprite.update()
                        pacManSprite.draw(windowSurface)
                        pygame.display.flip()
                    if event.key == pygame.K_DOWN:
                        pacMan.setMotionDirection("down")
                        pacManSprite.update()
                        pacManSprite.draw(windowSurface)
                        pygame.display.flip()

            manager.process_events(event)

        manager.update(time_delta)

        windowSurface.blit(background, (0, 0))
        manager.draw_ui(windowSurface)

        pygame.display.update()

    sys.exit(0)


if __name__ == '__main__':
    main()
