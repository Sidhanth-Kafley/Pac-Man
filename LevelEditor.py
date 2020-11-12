import os
import pygame
import mainScreen
from Level import Level

HEIGHT = 800
WIDTH = 1000


#
# def WallPicsLoad():
#     images = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     path = 'WallSprites'
#     for file in os.listdir(path):
#         image = pygame.image.load(path + os.sep + file).convert_alpha()
#         image = pygame.transform.scale(image, (16, 16))
#         if 'BlackSquare' in file:
#             images[0] = image
#         elif 'CornerBottomLeft' in file:
#             images[1] = image
#         elif 'CornerBottomRight' in file:
#             images[2] = image
#         elif 'CornerTopLeft' in file:
#             images[3] = image
#         elif 'CornerTopRight' in file:
#             images[4] = image
#         elif 'Gate' in file:
#             images[5] = image
#         elif 'HorizontalClosedLeft' in file:
#             images[6] = image
#         elif 'HorizontalClosedRight' in file:
#             images[7] = image
#         elif 'HorizontalIntersectionDown' in file:
#             images[8] = image
#         elif 'HorizontalIntersectionUp' in file:
#             images[9] = image
#         elif 'HorizontalOpen' in file:
#             images[10] = image
#         elif 'VerticalClosedBottom' in file:
#             images[11] = image
#         elif 'VerticalClosedTop' in file:
#             images[12] = image
#         elif 'VerticalIntersectionLeft' in file:
#             images[13] = image
#         elif 'VerticalIntersectionRight' in file:
#             images[14] = image
#         elif 'VerticalOpen' in file:
#             images[15] = image
#         elif 'Wall' in file:
#             images[16] = image
#     return images


def mainEditor():
    tf = True
    clock = pygame.time.Clock()
    offset_x = offset_y = 0

    window = pygame.display.set_mode((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    background.fill(mainScreen.BACKGROUND_COLOR)

    # initiate background surface (NEED TO CHANGE THE SIZE TO MATCH THE PROPORTIONS OF THE PLAYABLE AREA)
    basicBox = pygame.Rect((int(mainScreen.MAX_WIDTH / 2), int(mainScreen.MAX_HEIGHT / 2)),
                           (int(mainScreen.MAX_WIDTH / 3), int(mainScreen.MAX_HEIGHT / 1.5)))

    wallSprites = pygame.sprite.Group()

    # initialize the wall objects
    path = 'WallObjects'
    obj = [0, 0, 0, 0, 0, 0, 0, 0]
    for file in os.listdir(path):
        if "border" in file:
            obj[0] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(100, 70))
            wallSprites.add(obj[0])
        elif "ghosthouse" in file:
            obj[1] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 70))
            wallSprites.add(obj[1])
        elif "pp" in file:
            obj[2] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(300, 70))
            wallSprites.add(obj[2])
        elif "rectangle" in file:
            obj[3] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(400, 70))
            wallSprites.add(obj[3])
        elif "square" in file:
            obj[4] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(500, 70))
            wallSprites.add(obj[4])
        elif "straightBar" in file:
            obj[5] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(600, 70))
            wallSprites.add(obj[5])
        elif "straightBarSmall" in file:
            obj[6] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 170))
            wallSprites.add(obj[6])
        elif "T" in file:
            obj[7] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(300, 170))
            wallSprites.add(obj[7])

    while tf:
        # times per second this loop runs
        time_delta = clock.tick_busy_loop(60) / 1000.0

        # handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tf = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for wall in wallSprites:
                        if wall.collidepoint(event.pos):
                            newWall = wall.copy()
                            newWall.drag = True
                            wallSprites.add(newWall)
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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    openMenu()

        # draw the background box on the screen
        window.blit(background, (0, 0))
        window.blit(basicBox, "gray")

        for wall in wallSprites:
            wall.rect.clamp_ip(basicBox)

        # update wall placing collision here
        wallSprites.update()

        # update the image on screen
        wallSprites.draw(window)

        pygame.display.update()


def openMenu():
    print("hi")
    # Open the menu and display options for save, discard, and return to main menu
