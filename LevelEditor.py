import os
import pygame

HEIGHT = 800
WIDTH = 1000


def WallPicsLoad():
    images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    path = 'WallSprites'
    for file in os.listdir(path):
        image = pygame.image.load(path + os.sep + file).convert_alpha()
        image = pygame.transform.scale(image, (16, 16))
        if 'BlackSquare' in file:
            images[0] = image
        elif 'CornerBottomLeft' in file:
            images[1] = image
        elif 'CornerBottomRight' in file:
            images[2] = image
        elif 'CornerTopLeft' in file:
            images[3] = image
        elif 'CornerTopRight' in file:
            images[4] = image
        elif 'Gate' in file:
            images[5] = image
        elif 'HorizontalClosedLeft' in file:
            images[6] = image
        elif 'HorizontalClosedRight' in file:
            images[7] = image
        elif 'HorizontalIntersectionDown' in file:
            images[8] = image
        elif 'HorizontalIntersectionUp' in file:
            images[9] = image
        elif 'HorizontalOpen' in file:
            images[10] = image
        elif 'VerticalClosedBottom' in file:
            images[11] = image
        elif 'VerticalClosedTop' in file:
            images[12] = image
        elif 'VerticalIntersectionLeft' in file:
            images[13] = image
        elif 'VerticalIntersectionRight' in file:
            images[14] = image
        elif 'VerticalOpen' in file:
            images[15] = image
        elif 'Wall' in file:
            images[16] = image
    return images


def loadWallObjects():
    images = WallPicsLoad()

    # create objects for ghost house, side walls, rectangle, square, T-shaped things


def mainEditor():
    tf = True
    clock = pygame.time.Clock()
    wallSprites = []
    offset_x = offset_y = 0
    while tf:
        # times per second this loop runs
        time_delta = clock.tick_busy_loop(60) / 1000.0
        # handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tf = False
            # VVVVVVVVVVVVVVVVVVVVVVVVVVV EVENTS FOR DRAGGING AND DROPPING THE WALL OBJECTS VVVVVVVVVVVVVVVVVVVVVVVVVVV
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for wall in wallSprites:
                        if wall.collidepoint(event.pos):
                            wall.drag = True
                            mouse_x, mouse_y = event.pos
                            offset_x = wall.x - mouse_x
                            offset_y = wall.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for wall in wallSprites:
                        wall.drag = False
            elif event.type == pygame.MOUSEMOTION:
                for wall in wallSprites:
                    if wall.drag:
                        mouse_x, mouse_y = event.pos
                        wall.x = mouse_x + offset_x
                        wall.y = mouse_y + offset_y
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    openMenu()

        # update wall placing collision here

        # display the health bar at the bottom

        # update the wall sprites
        # wallSprites.update()
        # update the image on screen
        # allSprites.draw(window)

        pygame.display.update()


def openMenu():
    print("hi")
    # Open the menu and display options for save, discard, and return to main menu
