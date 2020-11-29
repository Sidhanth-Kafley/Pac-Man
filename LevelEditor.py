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


def mainEditor():
    tf = True

    window = pygame.display.set_mode((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    background = pygame.Surface((mainScreen.MAX_WIDTH, mainScreen.MAX_HEIGHT))
    background.fill(mainScreen.BACKGROUND_COLOR)

    # initiate background surface
    basicBox = pygame.Rect((50, 100), (700, 675))
    placeableArea = pygame.Rect((200, 100), (550, 675))
    otherSideBasicBox = pygame.Rect((200, 100), (700, 675))

    # left hand side objects
    borderSprites = []
    ghosthouseSprites = []
    rectangleSprites = []
    squareSprites = []
    straightbarSprites = []
    straightbarsmallSprites = []
    tSprites = []
    wallSprites = []
    specialSprites = []

    # right hand side objects
    pill = []
    specialpillSprites = []
    ghostsAndPacman = []

    # sprite groups to draw everything
    spriteGroup = pygame.sprite.Group()
    characterSpriteGroup = pygame.sprite.Group()
    pillSpriteGroup = pygame.sprite.Group()

    SPRITE_SIZE = 3 * mainScreen.CELL_SIZE

    # load Pacman object
    imgs = mainScreen.loadImages(path="PacManSprites")
    pcmn = PacMan(position=(800, 200), size=(SPRITE_SIZE, SPRITE_SIZE), images=imgs)
    characterSpriteGroup.add(pcmn)
    ghostsAndPacman.append(pcmn)

    powerPillImage = pygame.image.load("PowerUpPointPill.png").convert_alpha()
    powerPillImage = pygame.transform.scale(powerPillImage, (24, 24))
    pll = Pill(True, powerPillImage, (803, 453))
    pll.rect.size = (24, 24)
    pill.append(pll)
    pillSpriteGroup.add(pll)

    # create ghost objects
    blueGhostImages = mainScreen.loadImages(path='BlueGhostSprites')
    blueGhost = Ghost('blue', position=(800, 350), size=(SPRITE_SIZE, SPRITE_SIZE),
                      images=blueGhostImages)
    ghostsAndPacman.append(blueGhost)
    characterSpriteGroup.add(blueGhost)

    orangeGhostImages = mainScreen.loadImages(path='OrangeGhostSprites')
    orangeGhost = Ghost('orange', position=(800, 300), size=(SPRITE_SIZE, SPRITE_SIZE),
                        images=orangeGhostImages)
    ghostsAndPacman.append(orangeGhost)
    characterSpriteGroup.add(orangeGhost)

    pinkGhostImages = mainScreen.loadImages(path='PinkGhostSprites')
    pinkGhost = Ghost('pink', position=(800, 250), size=(SPRITE_SIZE, SPRITE_SIZE),
                      images=pinkGhostImages)
    ghostsAndPacman.append(pinkGhost)
    characterSpriteGroup.add(pinkGhost)

    redGhostImages = mainScreen.loadImages(path='RedGhostSprites')
    redGhost = Ghost('red', position=(800, 400), size=(SPRITE_SIZE, SPRITE_SIZE),
                     images=redGhostImages)
    ghostsAndPacman.append(redGhost)
    characterSpriteGroup.add(redGhost)

    # initialize the wall objects
    path = 'WallObjects'
    for file in os.listdir(path):
        if "border" in file:
            brdr = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(200, 100))
            for wall in brdr.walls:
                if wall not in spriteGroup:
                    borderSprites.append(wall)
                    spriteGroup.add(wall)
            del brdr
        elif "ghosthouse" in file and "Down" not in file:
            gh = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 100))
            for wall in gh.walls:
                if wall not in spriteGroup:
                    ghosthouseSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(ghosthouseSprites)
            del gh
        elif "rectangle" in file and "Vertical" not in file:
            rect = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 200))
            for wall in rect.walls:
                if wall not in spriteGroup:
                    rectangleSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(rectangleSprites)
            del rect
        elif "square" in file:
            sqr = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 300))
            for wall in sqr.walls:
                if wall not in spriteGroup:
                    squareSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(squareSprites)
            del sqr
        elif "straightBar" in file and file != "straightBarSmall" and "Vertical" not in file:
            strt = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 400))
            for wall in strt.walls:
                if wall not in spriteGroup:
                    straightbarSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(straightbarSprites)
            del strt
        elif "straightBarSmall" in file and "Vertical" not in file:
            small = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 500))
            for wall in small.walls:
                if wall not in spriteGroup:
                    straightbarsmallSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(straightbarsmallSprites)
            del small
        elif "T" in file and "Down" not in file:
            t = Level(layoutFilename=path + os.sep + file, wallSize=(16, 16), originPosition=(50, 600))
            for wall in t.walls:
                if wall not in spriteGroup:
                    tSprites.append(wall)
                    spriteGroup.add(wall)
            wallSprites.append(tSprites)
            del t

    click = False
    while tf:

        # time_delta = clock.tick_busy_loop(60) / 1000.0
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
                                            walls.setCollideRect()
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

                # FIGURE OUT HOW TO MAKE THE OBJECTS ROTATE AROUND A POINT
                elif event.button == 3:
                    check = False
                    for group in wallSprites:
                        if not check:
                            for wall in group:
                                if wall.drag:
                                    wallSprites.remove(group)
                                    specialSprites.remove(group)
                                    group = rotate(group)
                                    wallSprites.append(group)
                                    specialSprites.append(group)
                                    check = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    checker1 = False
                    for group in wallSprites:
                        for wall in group:
                            if not checker1:
                                if wall.drag:
                                    if collisionDetection(wall, specialSprites):
                                        wall.drag = False
                                        wallSprites.remove(group)
                                        specialSprites.remove(group)
                                        for x in group:
                                            spriteGroup.remove(x)
                                        checker1 = True
                                wall.drag = False
                                if not wall.rect.colliderect(placeableArea) and group in specialSprites:
                                    wallSprites.remove(group)
                                    specialSprites.remove(group)
                                    for x in group:
                                        spriteGroup.remove(x)
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

        # draw the background box on the screen
        window.blit(background, (0, 0))

        grayColor = (30, 30, 30)
        pygame.draw.rect(background, grayColor, basicBox)
        pygame.draw.rect(background, grayColor, otherSideBasicBox)
        pygame.draw.rect(background, (0, 30, 30), placeableArea)

        # make the sprites stay within their respective boxes
        for x in spriteGroup:
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
        spriteGroup.draw(window)
        characterSpriteGroup.draw(window)
        pillSpriteGroup.draw(window)

        # Buttons
        buttonplace4x = 200
        buttonplace6x = 500
        button4 = pygame.Rect(buttonplace4x, 30, 250, 50)
        button6 = pygame.Rect(buttonplace6x, 30, 250, 50)
        mousePosition = pygame.mouse.get_pos()

        if button4.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                tf = False
        if button6.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                saveLevel(borderSprites, specialSprites, specialpillSprites, pcmn, blueGhost, redGhost,
                          pinkGhost, orangeGhost)
                tf = False

        if buttonplace4x + 250 > mousePosition[0] > buttonplace4x and 30 + 50 > mousePosition[1] > 30:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button4)

        if buttonplace6x + 250 > mousePosition[0] > buttonplace6x and 30 + 50 > mousePosition[1] > 30:
            pygame.draw.rect(mainScreen.screen, (0, 190, 0), button6)
        else:
            pygame.draw.rect(mainScreen.screen, (0, 255, 0), button6)

        mainScreen.drawText('Main menu', mainScreen.font, (255, 255, 255), mainScreen.screen, buttonplace4x + 25, 45)
        mainScreen.drawText('Save Level', mainScreen.font, (255, 255, 255), mainScreen.screen, buttonplace6x + 25, 45)
        click = False

        pygame.display.update()

    background.fill(mainScreen.BACKGROUND_COLOR)
    # FIGURE OUT HOW TO MAKE THE WINDOW RESET AFTER EXITING


def rotate(group):
    # this function is used to rotate the the wall objects around the center
    mouse = pygame.mouse.get_pos()
    totalpointx = 0
    totalpointy = 0
    angle = (1 * math.pi) / 180
    for x in group:
        totalpointx += x.distancex
        totalpointy += x.distancey
    avgx = mouse[0] - totalpointx / len(group)
    avgy = mouse[1] - totalpointy / len(group)
    for x in group:
        x.rect.centerx -= avgx
        x.rect.centery -= avgy
        pointx = x.rect.centerx
        pointy = x.rect.centery
        newpointx = pointx * (math.cos(angle)) - pointy * math.sin(angle)
        newpointy = pointx * math.sin(angle) + pointy * math.cos(angle)
        x.rect.centerx = newpointx + avgx
        x.rect.centery = newpointy + avgy
        x.collideRect.centerx = x.rect.centerx
        x.collideRect.centery = x.rect.centery
        pygame.transform.rotate(x.image, angle)
    return group


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
    for pill in specialpillSprites:
        level.pills.append(pill)
    # level.pacmanAndGhost = [0, 0, 0, 0, 0]
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

        for x in level.walls:
            wallTuple = (message, x.imagePath, x.rect.centerx, x.rect.centery)
            wallArray = [wallTuple]
            cursor.executemany("INSERT INTO savedWalls (id, image, xpos, ypos) VALUES (?, ?, ?, ? );", wallArray)
            connection.commit()
        for x in level.pills:
            if x.powerPill:
                pillTuple = (message, 1, "PowerUpPointPill.png", x.rect.centerx, x.rect.centery)
                pillArray = [pillTuple]
            else:
                pillTuple = (message, 0, "PointPill.png", x.rect.centerx, x.rect.centery)
                pillArray = [pillTuple]
            cursor.executemany("INSERT INTO savedPoints (id, powerPill, image, xpos, ypos) VALUES (?, ?, ?, ?, ?);",
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

            Tuple = (message, typeCharacter, level.pacmanAndGhost[i].rect.centerx, level.pacmanAndGhost[i].rect.centery)
            Array = [Tuple]
            cursor.executemany("INSERT INTO savedCharacters (id, characterType, xpos, ypos) VALUES (?, ?, ?, ?);",
                               Array)
            connection.commit()
            i += 1
        connection.close()

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)


def chooseName():
    click = False
    isRunning = True
    nameInputBox = InputBox(365, 150, 140, 32, "Save Level")

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
            "CREATE TABLE IF NOT EXISTS savedWalls (id VARCHAR[64], image VARCHAR[64], xpos INTEGER, ypos INTEGER)")

        # create points table in the database
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='savedPoints' ''')

        # add the points and position to the table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS savedPoints (id VARCHAR[64], powerpill INTEGER, image VARCHAR[64], xpos INTEGER, ypos INTEGER)")

        # create character sprites table in the database
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='savedCharacters' ''')

        # add the character sprites and position to the table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS savedCharacters (id VARCHAR[64], characterType VARCHAR[64], xpos INTEGER, ypos INTEGER)")

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

        connection.close()

        level.walls = []
        for data in wallData:
            img = data[0]
            xpos = data[1]
            ypos = data[2]
            image = pygame.image.load('WallSprites' + os.sep + img).convert_alpha()
            level.walls.append(Wall((xpos, ypos), (level.wallSize[0], level.wallSize[1]), image, img))

        level.pills = []
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
        for data in characterData:
            charType = data[0]
            xpos = data[1]
            ypos = data[2]
            if 'Pacman' in charType:
                images = mainScreen.loadImages(path='PacManSprites')
                pacman = PacMan(position=(xpos, ypos), size=(2 * mainScreen.CELL_SIZE, 2 * mainScreen.CELL_SIZE),
                                images=images)
            elif 'BlueGhost' in charType:
                images = mainScreen.loadImages(path='BlueGhostSprites')
                blueGhost = Ghost('blue', position=(xpos, ypos),
                                  size=(2 * mainScreen.CELL_SIZE, 2 * mainScreen.CELL_SIZE), images=images)
            elif 'RedGhost' in charType:
                images = mainScreen.loadImages(path='RedGhostSprites')
                redGhost = Ghost('red', position=(xpos, ypos),
                                 size=(2 * mainScreen.CELL_SIZE, 2 * mainScreen.CELL_SIZE), images=images)
            elif 'PinkGhost' in charType:
                images = mainScreen.loadImages(path='PinkGhostSprites')
                pinkGhost = Ghost('pink', position=(xpos, ypos),
                                  size=(2 * mainScreen.CELL_SIZE, 2 * mainScreen.CELL_SIZE), images=images)
            elif 'OrangeGhost' in charType:
                images = mainScreen.loadImages(path='OrangeGhostSprites')
                orangeGhost = Ghost('orange', position=(xpos, ypos),
                                    size=(2 * mainScreen.CELL_SIZE, 2 * mainScreen.CELL_SIZE),
                                    images=images)

        level.pacmanAndGhost = [pacman, blueGhost, redGhost, pinkGhost, orangeGhost]

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)
    return level


def getSavedLevels():
    levelArray = []
    try:
        connection = sqlite3.connect('HighScores.db')
        cursor = connection.cursor()
        cursor.execute(
            "SELECT DISTINCT id FROM savedWalls")
        allLevels = cursor.fetchall()

        connection.close()

        index = 0
        while index < len(allLevels):
            levelArray.append(allLevels[index][0])
            index += 1

    except Error as error:
        print('Cannot connect to database. The following error occurred: ', error)
    return levelArray
