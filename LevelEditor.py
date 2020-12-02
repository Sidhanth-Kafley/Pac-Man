import os
import pygame
import mainScreen
import math
import sqlite3
from sqlite3 import Error
from Level import Level
from PacMan import PacMan
from pill import Pill
from ghost import Ghost
from inputBox import InputBox
from Wall import Wall
from PathingGridController import PathingGridController


def mainEditor():
    tf = True

    mainScreen.screen.fill(mainScreen.BACKGROUND_COLOR)
    window = mainScreen.screen
    background = mainScreen.screen

    # initiate background surface
    basicBox = pygame.Rect((int(mainScreen.MAX_WIDTH / 5)-150, int(mainScreen.MAX_HEIGHT / 12) - 2), (700, 675))
    placeableArea = pygame.Rect((int(mainScreen.MAX_WIDTH / 5), int(mainScreen.MAX_HEIGHT / 12) - 2), (550, 675))
    otherSideBasicBox = pygame.Rect((int(mainScreen.MAX_WIDTH / 5), int(mainScreen.MAX_HEIGHT / 12) - 2), (700, 675))

    # left hand side objects
    borderSprites = []
    wallSprites = []
    specialSprites = []

    otherwallsprites = []
    allWalls = []

    # right hand side objects
    pill = []
    specialpillSprites = []
    ghostsAndPacman = []

    # sprite groups to draw everything
    spriteGroup = pygame.sprite.Group()
    groupoSprites = pygame.sprite.Group()
    characterSpriteGroup = pygame.sprite.Group()
    pillSpriteGroup = pygame.sprite.Group()

    allWallSprites = pygame.sprite.Group()

    SPRITE_SIZE = 3 * mainScreen.CELL_SIZE

    # load Pacman object
    imgs = mainScreen.loadImages(path="PacManSprites")
    pcmn = PacMan(position=(810, 250), size=(SPRITE_SIZE, SPRITE_SIZE), images=imgs)
    characterSpriteGroup.add(pcmn)
    ghostsAndPacman.append(pcmn)

    powerPillImage = pygame.image.load("PowerUpPointPill.png").convert_alpha()
    powerPillImage = pygame.transform.scale(powerPillImage, (24, 24))
    pll = Pill(True, powerPillImage, (813, 503))
    pll.rect.size = (24, 24)
    pill.append(pll)
    pillSpriteGroup.add(pll)

    levelOriginX = int(mainScreen.MAX_WIDTH / 5) + int(mainScreen.MAX_WIDTH / 5) % mainScreen.CELL_SIZE
    levelOriginY = int(mainScreen.MAX_HEIGHT / 12) - int(mainScreen.MAX_HEIGHT / 12) % mainScreen.CELL_SIZE
    defaultLevel = Level(layoutFilename='Levels/level1alt.txt', wallSize=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE),
                  originPosition=(levelOriginX, levelOriginY))

    pathingGrid = PathingGridController(defaultLevel, mainScreen.CELL_SIZE, mainScreen.CELL_SIZE, mainScreen.MAX_WIDTH,
                                        mainScreen.MAX_HEIGHT)

    # create ghost objects
    blueGhostImages = mainScreen.loadImages(path='BlueGhostSprites')
    blueGhost = Ghost('blue', position=(800, 350), moveSpeed=1, size=(SPRITE_SIZE, SPRITE_SIZE),
                      images=blueGhostImages, pathingGridController=pathingGrid)
    ghostsAndPacman.append(blueGhost)
    characterSpriteGroup.add(blueGhost)

    orangeGhostImages = mainScreen.loadImages(path='OrangeGhostSprites')
    orangeGhost = Ghost('orange', position=(800, 300), moveSpeed=1.25, size=(SPRITE_SIZE, SPRITE_SIZE),
                        images=orangeGhostImages, pathingGridController=pathingGrid)
    ghostsAndPacman.append(orangeGhost)
    characterSpriteGroup.add(orangeGhost)

    pinkGhostImages = mainScreen.loadImages(path='PinkGhostSprites')
    pinkGhost = Ghost('pink', position=(800, 250), moveSpeed=2, size=(SPRITE_SIZE, SPRITE_SIZE),
                      images=pinkGhostImages, pathingGridController=pathingGrid)
    ghostsAndPacman.append(pinkGhost)
    characterSpriteGroup.add(pinkGhost)

    redGhostImages = mainScreen.loadImages(path='RedGhostSprites')
    redGhost = Ghost('red', position=(800, 400), moveSpeed=1.5, size=(SPRITE_SIZE, SPRITE_SIZE),
                     images=redGhostImages, pathingGridController=pathingGrid)
    ghostsAndPacman.append(redGhost)
    characterSpriteGroup.add(redGhost)

    # initialize the wall objects
    path = 'WallObjects'
    for file in os.listdir(path):
        check = True
        lvl = None
        if "border" in file:
            brdr = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16),
                         originPosition=(int(mainScreen.MAX_WIDTH / 5), int(mainScreen.MAX_HEIGHT / 12) - 2))
            for wall in brdr.walls:
                if wall not in spriteGroup:
                    borderSprites.append(wall)
                    allWallSprites.add(wall)
            del brdr
        if "ghosthouse" in file and "Down" not in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 100))
        elif "rectangle" in file and "Vertical" not in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 250))
        elif "square" in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(90, 350))
        elif "straightBar" in file and file != "straightBarSmall" and "Vertical" not in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(55, 450))
        elif "straightBarSmall" in file and "Vertical" not in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(75, 525))
        elif "T" in file and "Down" not in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 600))
        # loop for vertical wall objects
        elif "ghosthouse" in file and "Down" in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 100))
            check = False
        elif "rectangle" in file and "Vertical" in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(95, 225))
            check = False
        elif "straightBar" in file and "Small" not in file and "Vertical" in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(90, 420))
            check = False
        elif "straightBarSmall" in file and "Vertical" in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(125, 440))
            check = False
        elif "T" in file and "Down" in file and "border" not in file:
            lvl = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 600))
            check = False
        group = []
        if "border" not in file:
            for wall in lvl.walls:
                if wall not in spriteGroup:
                    group.append(wall)
                    if check:
                        spriteGroup.add(wall)
                    else:
                        groupoSprites.add(wall)
            if check:
                wallSprites.append(group)
            else:
                otherwallsprites.append(group)
            allWalls.append(group)
            del lvl

    click = False
    vertical = False
    while tf:

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
                    if not vertical:
                        wllsprt = wallSprites
                    else:
                        wllsprt = otherwallsprites
                    for group in wllsprt:
                        for wall in group:
                            if not checker:
                                if wall.rect.collidepoint(event.pos):
                                    if group not in specialSprites:
                                        for x in group:
                                            y = x.copy()
                                            new.append(y)
                                        for walls in new:
                                            walls.calculateDistance()
                                            walls.setCollideRect()
                                            walls.drag = True
                                    checker = True
                    checker = False
                    for group in specialSprites:
                        for wall in group:
                            if not checker:
                                if wall.rect.collidepoint(event.pos):
                                    for walls in group:
                                        walls.calculateDistance()
                                        walls.drag = True
                                    checker = True
                    if len(new) != 0:
                        allWalls.append(new)
                        specialSprites.append(new)
                        for wall in new:
                            allWallSprites.add(wall)
                        if not vertical:
                            wllsprt.append(new)
                            wallSprites = wllsprt
                        else:
                            wllsprt.append(new)
                            otherwallsprites = wllsprt
                    for character in characterSpriteGroup:
                        if character.rect.collidepoint(event.pos):
                            character.drag = True
                    for x in pill:
                        if x.rect.collidepoint(event.pos):
                            if x not in specialpillSprites:
                                newPill = Pill(True, x.image, x.rect.topleft)
                                newPill.rect.size = (24, 24)
                                newPill.drag = True
                                specialpillSprites.append(newPill)
                                pill.append(newPill)
                                pillSpriteGroup.add(newPill)
                            else:
                                x.drag = True
                elif event.button == 3:
                    vertical = not vertical
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    checker1 = False
                    for group in specialSprites:
                        for wall in group:
                            if not checker1:
                                if wall.drag:
                                    if collisionDetection(wall, specialSprites):
                                        wall.drag = False
                                        specialSprites.remove(group)
                                        for x in group:
                                            allWallSprites.remove(x)
                                        checker1 = True
                                wall.drag = False
                                if not wall.rect.colliderect(placeableArea) and group in specialSprites:
                                    specialSprites.remove(group)
                                    for x in group:
                                        allWallSprites.remove(x)
                                    checker1 = True
                    for character in characterSpriteGroup:
                        if character.drag:
                            character.drag = False
                    for x in pill:
                        if x.drag:
                            x.drag = False
                            if not x.rect.colliderect(placeableArea) and x in specialpillSprites:
                                pill.remove(x)
                                specialpillSprites.remove(x)
                                pillSpriteGroup.remove(x)
            elif event.type == pygame.MOUSEMOTION:
                for group in specialSprites:
                    for walls in group:
                        if walls.drag:
                            mouse_x, mouse_y = event.pos
                            walls.rect.centerx = mouse_x - walls.distancex
                            walls.rect.centery = mouse_y - walls.distancey
                            walls.collideRect.centerx = mouse_x - walls.distancex
                            walls.collideRect.centery = mouse_y - walls.distancey
                for character in characterSpriteGroup:
                    if character.drag:
                        character.rect.center = event.pos
                for x in specialpillSprites:
                    if x.drag:
                        x.rect.center = event.pos

        grayColor = (30, 30, 30)
        pygame.draw.rect(background, grayColor, basicBox)
        pygame.draw.rect(background, grayColor, otherSideBasicBox)
        pygame.draw.rect(background, (0, 30, 30), placeableArea)

        # make the sprites stay within their respective boxes
        for x in allWallSprites:
            x.rect.clamp_ip(basicBox)
        for x in characterSpriteGroup:
            x.rect.clamp_ip(otherSideBasicBox)
        for x in pillSpriteGroup:
            x.rect.clamp_ip(otherSideBasicBox)

        # wall collision indicators drawing and clamping
        for x in specialSprites:
            for y in x:
                y.collideRect.clamp_ip(basicBox)
                if collisionDetection(y, specialSprites):
                    pygame.draw.rect(background, (50, 0, 0), y.collideRect)
                else:
                    pygame.draw.rect(background, (0, 50, 50), y.collideRect)

        # draw all the sprites on screen
        if vertical:
            groupoSprites.draw(window)
        else:
            spriteGroup.draw(window)
        allWallSprites.draw(window)
        characterSpriteGroup.draw(window)
        pillSpriteGroup.draw(window)

        # Buttons
        buttonplace4x = 200
        buttonplace6x = 500
        buttonplacey = 10
        button4 = pygame.Rect(buttonplace4x, buttonplacey, 250, 50)
        button6 = pygame.Rect(buttonplace6x, buttonplacey, 250, 50)
        mousePosition = pygame.mouse.get_pos()

        if button4.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                tf = False
        if button6.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                saveLevel(borderSprites, specialSprites, specialpillSprites, pcmn, blueGhost, redGhost,
                          pinkGhost, orangeGhost)
                tf = False

        if buttonplace4x + 250 > mousePosition[0] > buttonplace4x and buttonplacey + 50 > mousePosition[1] > buttonplacey:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button4)

        if buttonplace6x + 250 > mousePosition[0] > buttonplace6x and buttonplacey + 50 > mousePosition[1] > buttonplacey:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button6)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button6)

        mainScreen.drawText('Main menu', mainScreen.font, (255, 255, 255), mainScreen.screen, buttonplace4x + 25,
                            buttonplacey + 15)
        mainScreen.drawText('Save Level', mainScreen.font, (255, 255, 255), mainScreen.screen, buttonplace6x + 25,
                            buttonplacey + 15)
        click = False
        pygame.display.update()


def collisionDetection(rect, othersprites):
    newGroup = []
    for wall in othersprites:
        if rect not in wall:
            newGroup.append(wall)
    for x in newGroup:
        for y in x:
            if y.collideRect.colliderect(rect.collideRect):
                return True
    return False


def saveLevel(borderSprites, specialSprites, specialpillSprites, pacman, blue, red, pink, orange):
    path = 'Levels'
    file = 'blank'
    level = Level(layoutFilename=path + os.sep + file, wallSize=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE),
                  originPosition=(int(mainScreen.MAX_WIDTH / 5), int(mainScreen.MAX_HEIGHT / 12) - 2))

    for wall in borderSprites:
        level.walls.append(wall)
    for group in specialSprites:
        for wall in group:
            level.walls.append(wall)
    level.pills = []
    for pill in specialpillSprites:
        level.pills.append(pill)
    level.pacmanAndGhost = []
    level.pacmanAndGhost.append(pacman)
    level.pacmanAndGhost.append(blue)
    level.pacmanAndGhost.append(red)
    level.pacmanAndGhost.append(pink)
    level.pacmanAndGhost.append(orange)

    message = chooseName()
    connectDatabase()

    try:
        # create connection to database
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        # get the number of items in the database for the index
        query = """SELECT count(distinct id) from savedWalls"""
        cursor.execute(query)
        indexQuery = cursor.fetchall()
        index = indexQuery[0][0] + 1

        for x in level.walls:
            wallTuple = (index, message, x.imagePath, x.rect.centerx, x.rect.centery)
            wallArray = [wallTuple]
            cursor.executemany("INSERT INTO savedWalls (idx, id, image, xpos, ypos) VALUES (?, ?, ?, ?, ? );", wallArray)
            connection.commit()
        for x in level.pills:
            if x.powerPill:
                pillTuple = (index, message, 1, "PowerUpPointPill.png", x.rect.centerx, x.rect.centery)
                pillArray = [pillTuple]
            else:
                pillTuple = (index, message, 0, "PointPill.png", x.rect.centerx, x.rect.centery)
                pillArray = [pillTuple]
            cursor.executemany("INSERT INTO savedPoints (idx, id, powerPill, image, xpos, ypos) VALUES (?, ?, ?, ?, ?, ?);",
                               pillArray)
            connection.commit()
        i = 0
        while i < len(level.pacmanAndGhost):
            typeCharacter = ''
            if i == 0:
                typeCharacter = 'Pacman'
            elif i == 1:
                typeCharacter = 'BlueGhost'
            elif i == 2:
                typeCharacter = 'RedGhost'
            elif i == 3:
                typeCharacter = 'PinkGhost'
            elif i == 4:
                typeCharacter = 'OrangeGhost'

            Tuple = (index, message, typeCharacter, level.pacmanAndGhost[i].rect.centerx, level.pacmanAndGhost[i].rect.centery)
            Array = [Tuple]
            cursor.executemany("INSERT INTO savedCharacters (idx, id, characterType, xpos, ypos) VALUES (?, ?, ?, ?, ?);",
                               Array)
            connection.commit()
            i += 1

        for group in specialSprites:
            maxx = 0
            minx = 10000
            maxy = 10000
            miny = 0
            for x in group:
                if x.rect.top < maxy:
                    maxy = x.rect.top
                if x.rect.bottom > miny:
                    miny = x.rect.bottom
                if x.rect.right > maxx:
                    maxx = x.rect.right
                if x.rect.left < minx:
                    minx = x.rect.left

            Tuple = (
            index, message, maxx, minx, maxy, miny)
            Array = [Tuple]
            cursor.executemany(
                "INSERT INTO savedBlankSpace (idx, id, xmax, xmin, ymax, ymin) VALUES (?, ?, ?, ?, ?, ?);",
                Array)
            connection.commit()

        connection.close()

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)


def chooseName():
    click = False
    isRunning = True
    nameInputBox = InputBox(365, 150, 140, 32, "Save Level", "level")

    while isRunning:
        mainScreen.screen.fill(mainScreen.BACKGROUND_COLOR)
        mainScreen.drawText('Please enter a name for your level', mainScreen.font, (255, 255, 255), mainScreen.screen,
                            150, 80)
        mousePosition = pygame.mouse.get_pos()
        button = pygame.Rect(365, 225, 200, 50)

        if button.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                isRunning = False
                message = nameInputBox.text
                if message != '':
                    return message

        if 365 + 200 > mousePosition[0] > 365 and 225 + 50 > mousePosition[1] > 225:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button)

        mainScreen.drawText('Save', mainScreen.font, (255, 255, 255), mainScreen.screen, 425, 240)

        click = False
        for event in pygame.event.get():
            if event.type == mainScreen.QUIT:
                pygame.quit()
                mainScreen.sys.exit()
            if event.type == mainScreen.KEYDOWN:
                if event.key == mainScreen.K_ESCAPE:
                    isRunning = False
            if event.type == mainScreen.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            nameInputBox.handleEvent(event)

        nameInputBox.update()
        nameInputBox.draw(mainScreen.screen)
        mainScreen.drawText(nameInputBox.getMessage(), mainScreen.font2, (255, 255, 255), mainScreen.screen, 300, 20)

        pygame.display.update()
        mainScreen.mainClock.tick(10)


def connectDatabase():
    try:
        # Start DB connection
        connection = sqlite3.connect('HighScores.db')
        # create cursor object
        cursor = connection.cursor()

        # create levels table in the database
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='savedWalls' ''')

        # add the wall and position to the table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS savedWalls (idx INTEGER, id VARCHAR[64], image VARCHAR[64], xpos INTEGER, ypos INTEGER)")

        # create points table in the database
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='savedPoints' ''')

        # add the points and position to the table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS savedPoints (idx INTEGER, id VARCHAR[64], powerpill INTEGER, image VARCHAR[64], xpos INTEGER, ypos INTEGER)")

        # create character sprites table in the database
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='savedCharacters' ''')

        # add the character sprites and position to the table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS savedCharacters (idx INTEGER, id VARCHAR[64], characterType VARCHAR[64], xpos INTEGER, ypos INTEGER)")

        # create character sprites table in the database
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='savedBlankSpace' ''')

        # add the character sprites and position to the table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS savedBlankSpace (idx INTEGER, id VARCHAR[64], xmax INTEGER, xmin INTEGER, ymax INTEGER, ymin INTEGER)")

        # commit databases
        connection.commit()
        connection.close()

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)


def parseCustomLevel(message):
    path = 'Levels'
    file = 'blank'
    level = Level(layoutFilename=path + os.sep + file, wallSize=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE),
                  originPosition=(int(mainScreen.MAX_WIDTH / 5), int(mainScreen.MAX_HEIGHT / 12) - 2))
    try:
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()

        cursor.execute(
            "SELECT image, xpos, ypos FROM savedWalls WHERE id LIKE '" + message + "'")
        wallData = cursor.fetchall()

        cursor.execute(
            "SELECT powerpill, image, xpos, ypos FROM savedPoints WHERE id LIKE '" + message + "'")
        pointData = cursor.fetchall()

        cursor.execute(
            "SELECT characterType, xpos, ypos FROM savedCharacters WHERE id LIKE '" + message + "'")
        characterData = cursor.fetchall()

        cursor.execute(
            "SELECT xmax, xmin, ymax, ymin FROM savedBlankSpace WHERE id LIKE '" + message + "'")
        blankData = cursor.fetchall()

        connection.close()

        level.walls = []
        for data in wallData:
            img = data[0]
            xpos = data[1]
            ypos = data[2]
            image = pygame.image.load('WallSprites' + os.sep + img).convert_alpha()
            level.walls.append(Wall((xpos, ypos), (level.wallSize[0], level.wallSize[1]), image, img))

        for data in pointData:
            pp = data[0]
            image = data[1]
            xpos = data[2]
            ypos = data[3]
            if pp == 0:
                power = False
            else:
                power = True
            pillImage = pygame.image.load(image).convert_alpha()
            pillImage = pygame.transform.scale(pillImage, (16, 16))
            level.pills.append(Pill(power, pillImage, (xpos, ypos)))

        pacman = None
        blueGhost = None
        redGhost = None
        pinkGhost = None
        orangeGhost = None
        pathingGrid = PathingGridController(level, mainScreen.CELL_SIZE, mainScreen.CELL_SIZE, mainScreen.MAX_WIDTH,
                                            mainScreen.MAX_HEIGHT)
        for data in characterData:
            charType = data[0]
            xpos = data[1]
            ypos = data[2]
            if 'Pacman' in charType:
                images = mainScreen.loadImages(path='PacManSprites')
                pacman = PacMan(position=(xpos, ypos - 16), size=(2 * mainScreen.CELL_SIZE, 2 * mainScreen.CELL_SIZE),
                                images=images)
            elif 'BlueGhost' in charType:
                images = mainScreen.loadImages(path='BlueGhostSprites')
                blueGhost = Ghost('blue', position=(xpos, ypos),  moveSpeed=1,
                                  size=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE), images=images,
                                  pathingGridController=pathingGrid)
            elif 'RedGhost' in charType:
                images = mainScreen.loadImages(path='RedGhostSprites')
                redGhost = Ghost('red', position=(xpos, ypos),  moveSpeed=1.25,
                                 size=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE), images=images,
                                 pathingGridController=pathingGrid)
            elif 'PinkGhost' in charType:
                images = mainScreen.loadImages(path='PinkGhostSprites')
                pinkGhost = Ghost('pink', position=(xpos, ypos),  moveSpeed=2,
                                  size=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE), images=images,
                                  pathingGridController=pathingGrid)
            elif 'OrangeGhost' in charType:
                images = mainScreen.loadImages(path='OrangeGhostSprites')
                orangeGhost = Ghost('orange', position=(xpos, ypos),  moveSpeed=1.5,
                                    size=(mainScreen.CELL_SIZE, mainScreen.CELL_SIZE),
                                    images=images,
                                    pathingGridController=pathingGrid)

        level.pacmanAndGhost = [pacman, blueGhost, redGhost, pinkGhost, orangeGhost]

        for data in blankData:
            xmax = data[0]
            xmin = data[1]
            ymax = data[2]
            ymin = data[3]
            delta = 10
            group = level.pills
            for x in group:
                if xmin - delta <= x.rect.centerx <= xmax + delta and ymax - delta <= x.rect.centery <= ymin + delta:
                    level.pills.remove(x)
                    del x

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)
    return level


def getSavedLevels():
    levelArray = []
    try:
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DISTINCT id FROM savedWalls ORDER BY idx DESC LIMIT 0,12")
        allLevels = cursor.fetchall()

        connection.close()

        index = 0
        while index < len(allLevels):
            levelArray.append(allLevels[index][0])
            index += 1

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)
    return levelArray
