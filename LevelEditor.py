import os
import pygame
import mainScreen
from Level import Level

HEIGHT = 800
WIDTH = 1000


def mainEditor():
    tf = True
    clock = pygame.time.Clock()
    offset_x = offset_y = 0

    window = pygame.display.set_mode((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    background.fill(mainScreen.BACKGROUND_COLOR)

    # initiate background surface (NEED TO CHANGE THE SIZE TO MATCH THE PROPORTIONS OF THE PLAYABLE AREA)
  #  basicBox = pygame.Rect((int(mainScreen.MAX_WIDTH / 2), int(mainScreen.MAX_HEIGHT / 2)),
                      #     (int(mainScreen.MAX_WIDTH / 3), int(mainScreen.MAX_HEIGHT / 1.5)))

    borderSprites = pygame.sprite.Group()
    ghosthouseSprites = pygame.sprite.Group()
    ppSprites = pygame.sprite.Group()
    rectangleSprites = pygame.sprite.Group()
    squareSprites = pygame.sprite.Group()
    straightbarSprites = pygame.sprite.Group()
    straightbarsmallSprites = pygame.sprite.Group()
    tSprites = pygame.sprite.Group()

    wallSprites = []

    # initialize the wall objects
    path = 'WallObjects'
    obj = [0, 0, 0, 0, 0, 0, 0, 0]
    for file in os.listdir(path):
        if "border" in file:
            obj[0] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 100))
            for wall in obj[0].walls:
                borderSprites.add(wall)
           # wallSprites.append(borderSprites)
        elif "ghosthouse" in file:
            obj[1] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 300))
            for wall in obj[1].walls:
                ghosthouseSprites.add(wall)
            wallSprites.append(ghosthouseSprites)
        elif "pp" in file:
            obj[2] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(300, 300))
            for wall in obj[2].walls:
                ppSprites.add(wall)
            wallSprites.append(ppSprites)
        elif "rectangle" in file:
            obj[3] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(400, 300))
            for wall in obj[3].walls:
                rectangleSprites.add(wall)
            wallSprites.append(rectangleSprites)
        elif "square" in file:
            obj[4] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(300, 400))
            for wall in obj[4].walls:
                squareSprites.add(wall)
            wallSprites.append(squareSprites)
        elif "straightBar" in file:
            obj[5] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(300, 300))
            for wall in obj[5].walls:
                straightbarSprites.add(wall)
            wallSprites.append(straightbarSprites)
        elif "straightBarSmall" in file:
            obj[6] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 300))
            for wall in obj[6].walls:
                straightbarsmallSprites.add(wall)
            wallSprites.append(straightbarsmallSprites)
        elif "T" in file:
            obj[7] = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(300, 300))
            for wall in obj[7].walls:
                tSprites.add(wall)
            wallSprites.append(tSprites)

    specialSprites = []
    click = False
    while tf:

       # mainScreen.screen.fill(mainScreen.BACKGROUND_COLOR)
        mainScreen.drawText('Creative Mode', mainScreen.titleFont, (255, 255, 255), mainScreen.screen, 300, 50)
        mousePosition = pygame.mouse.get_pos()
        button4 = pygame.Rect(700, 700, 250, 50)

        if button4.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                tf = False

        if 700 + 250 > mousePosition[0] > 700 and 700 + 50 > mousePosition[1] > 700:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button4)

        mainScreen.drawText('Main menu', mainScreen.font, (255, 255, 255), mainScreen.screen, 725, 715)
        click = False

        pygame.display.update()
        mainScreen.mainClock.tick(10)
        # times per second this loop runs
        time_delta = clock.tick_busy_loop(60) / 1000.0

        # handles events
        for event in pygame.event.get():
            if event.type == mainScreen.QUIT:
                pygame.quit()
                mainScreen.sys.exit()
            elif event.type == mainScreen.KEYDOWN:
                if event.key == mainScreen.K_ESCAPE:
                    tf = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    for group in wallSprites:
                        for wall in group:
                            if wall.rect.collidepoint(event.pos):
                                if group not in specialSprites:
                                    newWall = group
                                    specialSprites.append(newWall)
                                    wallSprites.append(newWall)
                                    for walls in newWall:
                                        walls.drag = True
                                        mouse_x, mouse_y = event.pos
                                        offset_x = walls.rect.x - mouse_x
                                        offset_y = walls.rect.y - mouse_y
                                else:
                                    for walls in group:
                                        walls.drag = True
                                        mouse_x, mouse_y = event.pos
                                        offset_x = walls.rect.x - mouse_x
                                        offset_y = walls.rect.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for group in specialSprites:
                        for wall in group:
                            wall.drag = False
            elif event.type == pygame.MOUSEMOTION:
                for group in specialSprites:
                    for wall in group:
                        if wall.drag:
                            for walls in group:
                                mouse_x, mouse_y = event.pos
                                walls.rect.x = mouse_x + offset_x
                                walls.rect.y = mouse_y + offset_y

        # draw the background box on the screen
        window.blit(background, (0, 0))
        # window.blit(basicBox)
        #
        # for wall in wallSprites:
        #     wall.rect.clamp_ip(basicBox)

        # update wall placing collision here
     #   wallSprites.update()

        # update the image on screen
        borderSprites.draw(window)
        for x in wallSprites:
            x.draw(window)

        pygame.display.update()


def openMenu():
    print("hi")
    # Open the menu and display options for save, discard, and return to main menu
