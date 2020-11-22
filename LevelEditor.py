import os
import pygame
import mainScreen
from Level import Level


def mainEditor():
    tf = True
    clock = pygame.time.Clock()
    offset_x = offset_y = 0

    window = pygame.display.set_mode((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    windowRect = window.get_rect()
    background = pygame.Surface((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    background.fill(mainScreen.BACKGROUND_COLOR)

    # initiate background surface (NEED TO CHANGE THE SIZE TO MATCH THE PROPORTIONS OF THE PLAYABLE AREA)
    basicBox = pygame.Rect((50, 100), (700, 675))

    borderSprites = []
    ghosthouseSprites = []
    ppSprites = []
    rectangleSprites = []
    squareSprites = []
    straightbarSprites = []
    straightbarsmallSprites = []
    tSprites = []

    spriteGroup = pygame.sprite.Group()

    wallSprites = []
    specialSprites = []

    # initialize the wall objects
    path = 'WallObjects'
    for file in os.listdir(path):
        if "border" in file:
            brdr = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 100))
            for wall in brdr.walls:
                if wall not in spriteGroup:
                    borderSprites.append(wall)
                    spriteGroup.add(wall)
        if "ghosthouse" in file:
            gh = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 100))
            for wall in gh.walls:
                if wall not in spriteGroup:
                    ghosthouseSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(ghosthouseSprites)
        if "rectangle" in file:
            rect = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 200))
            for wall in rect.walls:
                if wall not in spriteGroup:
                    rectangleSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(rectangleSprites)
        if "square" in file:
            sqr = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 300))
            for wall in sqr.walls:
                if wall not in spriteGroup:
                    squareSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(squareSprites)
        if "straightBar" in file and file != "straightBarSmall":
            strt = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 400))
            for wall in strt.walls:
                if wall not in spriteGroup:
                    straightbarSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(straightbarSprites)
        if "straightBarSmall" in file:
            small = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 500))
            for wall in small.walls:
                if wall not in spriteGroup:
                    straightbarsmallSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(straightbarsmallSprites)
        if "T" in file:
            t = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 600))
            for wall in t.walls:
                if wall not in spriteGroup:
                    tSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(tSprites)
        if "pp" in file:
            pp = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(100, 700))
            for wall in pp.walls:
                if wall not in spriteGroup:
                    ppSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(ppSprites)

    button4 = pygame.Rect(200, 30, 250, 50)
    button5 = pygame.Rect(500, 30, 250, 50)
    click = False
    while tf:
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        mousePosition = pygame.mouse.get_pos()

        if button4.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                tf = False
        if button5.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                print("hi")
                # CALL THE GAME PLAYER WITH THIS LEVEL

        if 700 + 250 > mousePosition[0] > 700 and 700 + 50 > mousePosition[1] > 700:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button4)

        if 700 + 250 > mousePosition[0] > 700 and 650 + 50 > mousePosition[1] > 650:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button5)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button5)

        mainScreen.drawText('Play Level', mainScreen.font, (255, 255, 255), mainScreen.screen, 525, 45)
        mainScreen.drawText('Main menu', mainScreen.font, (255, 255, 255), mainScreen.screen, 225, 45)
        click = False

        pygame.display.update()

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
                    checker = False
                    new = []
                    for group in wallSprites:
                        for wall in group:
                            if not checker:
                                if wall.rect.collidepoint(event.pos):
                                    if group not in specialSprites:
                                        for x in group:
                                            y = x.copy()
                                            new.append(y)
                                        for walls in new:
                                            walls.calculateDistance()
                                            walls.drag = True
                                    else:
                                        for walls in group:
                                            walls.calculateDistance()
                                            walls.drag = True
                                    checker = True
                    if len(new) != 0:
                        wallSprites.append(new)
                        specialSprites.append(new)
                        for wall in new:
                            spriteGroup.add(wall)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for group in wallSprites:
                        for wall in group:
                            wall.drag = False
            elif event.type == pygame.MOUSEMOTION:
                for group in specialSprites:
                    for walls in group:
                        if walls.drag:
                            mouse_x, mouse_y = event.pos
                            walls.rect.centerx = mouse_x - walls.distancex
                            walls.rect.centery = mouse_y - walls.distancey

        # draw the background box on the screen
        window.blit(background, (0, 0))

        pygame.draw.rect(background, (30, 30, 30), basicBox)

        for x in spriteGroup:
            x.rect.clamp_ip(basicBox)

        # window.blit(basicBox)
        #
        # for wall in wallSprites:
        #     wall.rect.clamp_ip(basicBox)

        # update wall placing collision here

        # update the image on screen
        #borderSprites.draw(window)
       #  spriteGroup.draw(window)
        spriteGroup.draw(window)
        # for x in wallSprites:
        #     x.draw(window)

        pygame.display.update()


def openMenu():
    print("hi")
    # Open the menu and display options for save, discard, and return to main menu
