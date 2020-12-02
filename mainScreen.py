import pygame
import pygame_gui
import sys
import os
import math
import LevelEditor
from PacMan import PacMan
from ghost import Ghost
from pygame.locals import *
from Level import Level
from PathingGridController import PathingGridController
from highScores import HighScores
from inputBox import InputBox

pygame.init()

MAX_HEIGHT = 800
MAX_WIDTH = 1000
BACKGROUND_COLOR = pygame.Color('black')
CELL_SIZE = 16
SPRITE_SIZE = 2 * CELL_SIZE

click = False
mainClock = pygame.time.Clock()
font = pygame.font.Font('8-BIT WONDER.TTF', 20)
font2 = pygame.font.Font(None, 40)
titleFont = pygame.font.Font('8-BIT WONDER.TTF', 30)

pygame.display.set_caption('Pac Man')
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT), 0, 32)
window = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
windowRect = window.get_rect()
background = pygame.Surface((MAX_WIDTH, MAX_HEIGHT))
background.fill(BACKGROUND_COLOR)
manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))


# function to draw text onto the screen
def drawText(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (int(x), int(y))
    surface.blit(textObj, textRect)


def main():
    mainMenu()


def mainMenu():
    running = True
    global click
    click = False

    while running:

        screen.fill(BACKGROUND_COLOR)
        drawText('main menu', titleFont, (255, 255, 255), screen, MAX_HEIGHT / 2.5, MAX_WIDTH / 4)

        # get mousePosition for collision detection
        mousePosition = pygame.mouse.get_pos()

        # create buttons
        button1 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 3.0), 250, 50)
        button3 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 2.4), 250, 50)
        button2 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 2.0), 250, 50)
        button4 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 1.7), 250, 50)

        # if button is clicked call corresponding functions
        if button2.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                credits()

        if button3.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                LevelEditor.mainEditor()

        if button4.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                leaderBoards()

        if button1.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                levels()

        # draw buttons and add hover effect
        # got logic for button hovering from pythonprogramming.net
        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 3.0 + 50 > mousePosition[
            1] > MAX_WIDTH / 3.0:
            pygame.draw.rect(screen, (0, 190, 0), button1)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button1)

        drawText('start game', font, (255, 255, 255), screen, MAX_HEIGHT / 2.3, MAX_WIDTH / 2.9)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 2.4 + 50 > mousePosition[
            1] > MAX_WIDTH / 2.4:
            pygame.draw.rect(screen, (0, 190, 0), button3)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button3)

        drawText('Creative Mode', font, (255, 255, 255), screen, MAX_HEIGHT / 2.5, MAX_WIDTH / 2.32)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 2.0 + 50 > mousePosition[
            1] > MAX_WIDTH / 2.0:
            pygame.draw.rect(screen, (0, 190, 0), button2)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button2)

        drawText('Credits', font, (255, 255, 255), screen, MAX_HEIGHT / 2.2, MAX_WIDTH / 1.95)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 1.7 + 50 > mousePosition[
            1] > MAX_WIDTH / 1.7:
            pygame.draw.rect(screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button4)

        drawText('Leaderboards', font, (255, 255, 255), screen, MAX_HEIGHT / 2.5, MAX_WIDTH / 1.67)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def loadImages(path):
    images = []
    if path == 'PacManSprites':
        images = [0, 0, 0, 0, 0]
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert_alpha()
            image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
            if 'Down' in file:
                images[0] = image
            elif 'Left' in file:
                images[1] = image
            elif 'Right' in file:
                images[2] = image
            elif 'Up' in file:
                images[3] = image
            elif 'Closed' in file:
                images[4] = image
    elif 'GhostSprites' in path:
        images = [0, 0, 0, 0, 0]
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert_alpha()
            image = pygame.transform.scale(image, (SPRITE_SIZE, SPRITE_SIZE))
            if 'Down' in file:
                images[0] = image
            elif 'Left' in file:
                images[1] = image
            elif 'Right' in file:
                images[2] = image
            elif 'Up' in file:
                if 'Power' in file:
                    images[4] = image
                else:
                    images[3] = image
    return images


# Function to show who contributed to this project
def credits():
    isRunning = True
    click = False
    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('Game made by', titleFont, (255, 255, 255), screen, 300, 250)
        drawText('Jaden Varin', font, (255, 255, 255), screen, 350, 340)
        drawText('Michelle Wehrle', font, (255, 255, 255), screen, 350, 380)
        drawText('Sidhanth Kafley', font, (255, 255, 255), screen, 350, 420)
        drawText('Cam Brown', font, (255, 255, 255), screen, 350, 460)

        mousePosition = pygame.mouse.get_pos()
        button = pygame.Rect(350, 540, 250, 50)

        if button.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                isRunning = False

        if 350 + 250 > mousePosition[0] > 350 and 540 + 50 > mousePosition[1] > 540:
            pygame.draw.rect(screen, (0, 190, 0), button)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button)

        drawText('Main Menu', font, (255, 255, 255), screen, 370, 555)

        for event in pygame.event.get():
            if event.type == QUIT:
                isRunning = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(10)


def pauseGame():

    pause = True

    click = False
    while pause:
        screen.fill((BACKGROUND_COLOR))
        drawText('Game Paused', titleFont, (255, 255, 255), screen, 300, 250)

        mousePosition = pygame.mouse.get_pos()

        button9 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 3.0), 250, 50)
        button10 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 2.4), 250, 50)

        if button9.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                pause = False


        if button10.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                mainMenu()

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 3.0 + 50 > mousePosition[
            1] > MAX_WIDTH / 3.0:
            pygame.draw.rect(screen, (0, 190, 0), button9)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button9)

        drawText('Play', font, (255, 255, 255), screen, MAX_HEIGHT / 2.0, MAX_WIDTH / 2.9)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 2.4 + 50 > mousePosition[
            1] > MAX_WIDTH / 2.4:
            pygame.draw.rect(screen, (0, 190, 0), button10)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button10)

        drawText('Main Menu', font, (255, 255, 255), screen, MAX_HEIGHT / 2.3, MAX_WIDTH / 2.32)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def game(game="1"):
    # Initiate game and window
    pygame.init()

    # create level object
    customLevel = False
    levelOriginX = int(MAX_WIDTH / 5) + int(MAX_WIDTH / 5) % CELL_SIZE
    levelOriginY = int(MAX_HEIGHT / 12) - int(MAX_HEIGHT / 12) % CELL_SIZE
    if game == "1":
        level = Level(layoutFilename='Levels/level1alt.txt', wallSize=(CELL_SIZE, CELL_SIZE),
                      originPosition=(levelOriginX, levelOriginY))
    elif game == "2":
        level = Level(layoutFilename='Levels/level2.txt', wallSize=(CELL_SIZE, CELL_SIZE),
                      originPosition=(levelOriginX, levelOriginY))
    else:
        # call level parser to create custom level object
        level = LevelEditor.parseCustomLevel(game)
        customLevel = True

    pillGroup = pygame.sprite.Group(level.pills)

    images = loadImages(path='PacManSprites')
    ghosts = []

    if not customLevel:
        pathingGrid = PathingGridController(level, CELL_SIZE, CELL_SIZE, MAX_WIDTH, MAX_HEIGHT)

        # create pacman object
        pacMan = PacMan(position=(MAX_WIDTH / 3, MAX_HEIGHT / 2), size=(2 * CELL_SIZE, 2 * CELL_SIZE), images=images)

        # create blue ghost object
        blueGhostImages = loadImages(path='BlueGhostSprites')
        blueGhost = Ghost('blue', position=(524, 390), moveSpeed=1, size=(CELL_SIZE, CELL_SIZE), images=blueGhostImages,
                          pathingGridController=pathingGrid)
        ghosts.append(blueGhost)

        # create orange ghost object
        orangeGhostImages = loadImages(path='OrangeGhostSprites')
        orangeGhost = Ghost('orange', position=(464, 390), moveSpeed=1, size=(CELL_SIZE, CELL_SIZE), images=orangeGhostImages,
                            pathingGridController=pathingGrid)
        ghosts.append(orangeGhost)

        # create pink ghost object
        pinkGhostImages = loadImages(path='PinkGhostSprites')
        pinkGhost = Ghost('pink', position=(434, 390), moveSpeed=1, size=(CELL_SIZE, CELL_SIZE), images=pinkGhostImages,
                          pathingGridController=pathingGrid)
        ghosts.append(pinkGhost)

        # create red ghost object
        redGhostImages = loadImages(path='RedGhostSprites')
        redGhost = Ghost('red', position=(494, 390), moveSpeed=1, size=(CELL_SIZE, CELL_SIZE), images=redGhostImages,
                         pathingGridController=pathingGrid)
        ghosts.append(redGhost)
    else:
        pathingGrid = PathingGridController(level, CELL_SIZE, CELL_SIZE, MAX_WIDTH, MAX_HEIGHT)
        pacMan = level.pacmanAndGhost[0]
        blueGhost = level.pacmanAndGhost[1]
        redGhost = level.pacmanAndGhost[2]
        pinkGhost = level.pacmanAndGhost[3]
        orangeGhost = level.pacmanAndGhost[4]
        ghosts.append(blueGhost)
        ghosts.append(orangeGhost)
        ghosts.append(pinkGhost)
        ghosts.append(redGhost)

    # health bar at the top of the screen
    healthBar = pygame.transform.scale(images[2], (int(24), int(24)))

    # portals to go to other side of screen
    leftPortal = pygame.Rect(160, 200, 40, 500)
    rightPortal = pygame.Rect(760, 200, 40, 500)

    allSprites = pygame.sprite.Group(pacMan, blueGhost, orangeGhost, pinkGhost, redGhost, level.walls)

    # clock used for framerate
    clock = pygame.time.Clock()
    isRunning = True

    # start main background music
    backgroundMusic = pygame.mixer.Sound("Music/PacManBeginning.wav")
    backgroundMusic.play(0)
    backgroundMusic.set_volume(0.25)

    count = 0
    pathfindingTimer = 0
    
    # initial wait until game starts
    pygame.time.delay(2000)
    while isRunning:
        # times per second this loop runs
        time_delta = clock.tick_busy_loop(60) / 1000.0

        screen.fill(BACKGROUND_COLOR)

        # determine if a wall is colliding
        # check if pacman is running into any walls
        pacMan.checkMotion(level)

        # handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pacMan.checkMove("left", level):
                    pacMan.velocity.y = 0
                    pacMan.velocity.x = (-1.5)
                elif event.key == pygame.K_RIGHT and pacMan.checkMove("right", level):
                    pacMan.velocity.y = 0
                    pacMan.velocity.x = 1.5
                elif event.key == pygame.K_UP and pacMan.checkMove("up", level):
                    pacMan.velocity.x = 0
                    pacMan.velocity.y = (-1.5)
                elif event.key == pygame.K_DOWN and pacMan.checkMove("down", level):
                    pacMan.velocity.x = 0
                    pacMan.velocity.y = 1.5
                elif event.key == pygame.K_ESCAPE:
                    pauseGame()

            manager.process_events(event)

        if pygame.sprite.spritecollide(pacMan, ghosts, False):
            pacManEatGhost = pygame.mixer.Sound("Music/PacManEatGhost.wav")
            for ghost in ghosts:
                if pacMan.rect.colliderect(ghost.rect) and ghost.powerUpMode:
                    if not ghost.eaten and ghost.powerUpMode:
                        pacManEatGhost.set_volume(0.25)
                        pacManEatGhost.play(0)
                        pacMan.eatGhost(ghost)
                        pygame.time.delay(400)
                elif pacMan.rect.colliderect(ghost.rect) and not ghost.powerUpMode:
                    if not pacMan.death:
                        pacManDeath = pygame.mixer.Sound("Music/PacManDeath.wav")
                        pacManDeath.set_volume(0.25)
                        pacManDeath.play(0)
                        for ghost in ghosts:
                            ghost.resetGhost()
                        pacMan.deathAnimation()

        if pygame.sprite.spritecollide(pacMan, pillGroup, False):
            pacManChomp = pygame.mixer.Sound("Music/PacManChomp.wav")
            pacManChomp.set_volume(0.25)
            pacManChomp.play(0)

            for x in pillGroup:
                if pacMan.rect.colliderect(x.rect):
                    if pacMan.eatPill(x):
                        pacMan.powerUp = True
                        for ghost in ghosts:
                            ghost.powerUpMode = True
                    pillGroup.remove(x)

        if len(pillGroup) == 0:
            displayGameOver(pacMan, window, game)

        # only run the powerup for 700 loops
        if pacMan.powerUp:
            count += 1

        if count == 700:
            count = 0
            pacMan.setPowerUp()
            for ghost in ghosts:
                ghost.powerUpMode = False

        # activate ghost pathfinding
        pacCellX = math.floor(pacMan.rect.x / pathingGrid.cellWidth)
        pacCellY = math.floor(pacMan.rect.y / pathingGrid.cellHeight)

        pathfindingTimer += 1
        if pathfindingTimer == 30:
            pathfindingTimer = 0
            for ghost in ghosts:
                if not ghost.powerUpMode:
                    ghost.pathfindToPoint(pacCellX, pacCellY)
                else:
                    ghost.pathfindToPoint(math.floor(ghost.spawnX / pathingGrid.cellWidth), math.floor(ghost.spawnY / pathingGrid.cellHeight))
        #pathingGrid.drawCellsList(background, ghosts[3].closedCells, (255, 255, 0))
        #pathingGrid.drawCellsList(background, ghosts[2].pathCells, (0, 255, 255))

        # pacMan portal code
        if pacMan.collisionRectRight.right == leftPortal.right and pacMan.collisionRect.colliderect(leftPortal):
            pacMan.rect.right = rightPortal.centerx
        elif pacMan.collisionRectLeft.left == rightPortal.left and pacMan.collisionRect.colliderect(rightPortal):
            pacMan.rect.left = leftPortal.centerx

        # manager.update(time_delta)
        window.blit(background, (0, 0))
        manager.draw_ui(window)
        # ADDED TO RESET SCREEN
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, 800, 1000))
        # display the health bar at the bottom
        if pacMan.startingHealth - 1 == 2:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
            window.blit(healthBar, (50, MAX_HEIGHT - 50))
        elif pacMan.startingHealth - 1 == 1:
            window.blit(healthBar, (20, MAX_HEIGHT - 50))
        elif pacMan.startingHealth == 0:
            displayGameOver(pacMan, window, game)
        # display score
        window.blit(pacMan.renderScore(32), (10, 10))

        # ensures that the pacMan and ghosts won't go off screen
        pacMan.rect.clamp_ip(windowRect)
        blueGhost.rect.clamp_ip(windowRect)
        orangeGhost.rect.clamp_ip(windowRect)
        pinkGhost.rect.clamp_ip(windowRect)
        redGhost.rect.clamp_ip(windowRect)

        pillGroup.draw(window)
        # update the sprite
        allSprites.update()
        # update the image on screen
        allSprites.draw(window)
        pathingGrid.update()
        # used in custom level
        if customLevel:
            # TODO: Not the best way to cover up old game
            pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 100, 202, 620))
            pygame.draw.rect(screen, BACKGROUND_COLOR, (800, 200, 100, 300))
        pygame.draw.rect(screen, (0, 0, 0), leftPortal)
        pygame.draw.rect(screen, (0, 0, 0), rightPortal)
        pygame.display.update()

    pygame.mixer.music.stop()
    sys.exit(0)


def displayGameOver(pacMan, window, msg):

    click = False
    isRunning = True
    highScoreInputBox = InputBox(365, 150, 140, 32, pacMan.getTotalPoints(), "scores")

    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('GameOver', titleFont, (255, 255, 255), screen, 340, 250)
        drawText('Please enter your initials to record your score', font, (255, 255, 255), screen, 70, 80)
        drawText('then press the enter key', font, (255, 255, 255), screen, 250, 110)
        window.blit(pacMan.renderScore(100), (370, 350))
        mousePosition = pygame.mouse.get_pos()
        button = pygame.Rect(340, 500, 250, 50)
        button1 = pygame.Rect(340, 600, 250, 50)
        # display button to play again
        if button.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                game(msg)
        if button1.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                mainMenu()

        if 340 + 250 > mousePosition[0] > 340 and 500 + 50 > mousePosition[1] > 500:
            pygame.draw.rect(screen, (0, 190, 0), button)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button)
        if 340 + 250 > mousePosition[0] > 340 and 600 + 50 > mousePosition[1] > 600:
            pygame.draw.rect(screen, (0, 190, 0), button1)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button1)

        drawText('Play again', font, (255, 255, 255), screen, 360, 515)
        drawText('Main Menu', font, (255, 255, 255), screen, 360, 615)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            highScoreInputBox.handleEvent(event)

        highScoreInputBox.update()
        highScoreInputBox.draw(screen)
        message = highScoreInputBox.getMessage()
        drawText(message, font2, (255, 255, 255), screen, 300, 20)

        pygame.display.update()
        mainClock.tick(10)


def creativeMode():
    click = False
    isRunning = True
    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('Creative Mode', titleFont, (255, 255, 255), screen, 300, 50)
        mousePosition = pygame.mouse.get_pos()
        button4 = pygame.Rect(700, 700, 250, 50)

        if button4.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                isRunning = False

        if 700 + 250 > mousePosition[0] > 700 and 700 + 50 > mousePosition[1] > 700:
            pygame.draw.rect(screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button4)

        drawText('Main menu', font, (255, 255, 255), screen, 725, 715)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(10)


def leaderBoards():
    click = False
    isRunning = True

    # get high scores and make sure they are in order
    topHighScores = HighScores()
    topHighScores.determineNewHighScore()
    dictOfScores = topHighScores.getTop5HighScores()

    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('Leaderboards', titleFont, (255, 255, 255), screen, 300, 50)

        # display the top 5 scores
        scoreXCoord = 350
        scoreYCoord = 200

        # display headers for leaderboard
        headers = 'Initials             Scores'
        drawText(headers, font2, (255, 255, 255), screen, 325, scoreYCoord)
        scoreYCoord += 75

        # go through each score in the top high scores dictionary and display them
        for key in dictOfScores:
            initial = dictOfScores[key][1]
            userScore = dictOfScores[key][2]
            if initial != 'No Scores':
                highScoreDisplay = initial + '                      ' + str(userScore)
                drawText(highScoreDisplay, font2, (255, 255, 255), screen, scoreXCoord, scoreYCoord)
                # need to make sure scores are spaced out
                scoreYCoord += 75

        mousePosition = pygame.mouse.get_pos()
        button4 = pygame.Rect(700, 700, 250, 50)

        if button4.collidepoint(mousePosition[0], mousePosition[1]):
            if click:
                isRunning = False

        if 700 + 250 > mousePosition[0] > 700 and 700 + 50 > mousePosition[1] > 700:
            pygame.draw.rect(screen, (0, 190, 0), button4)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button4)

        drawText('Main menu', font, (255, 255, 255), screen, 725, 715)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    isRunning = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(10)


def levels():
    click = False
    isRunning = True
    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('Select Difficulty', titleFont, (255, 255, 255), screen, 260, 150)
        mousePosition = pygame.mouse.get_pos()

        button5 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 3.0), 250, 50)
        button6 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 2.4), 250, 50)
        button7 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 2.0), 250, 50)
        button8 = pygame.Rect(int(MAX_HEIGHT / 2.5), int(MAX_WIDTH / 1.7), 250, 50)

        # if button is clicked call corresponding functions
        if button5.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                game(game="1")

        if button6.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                game(game="2")

        if button7.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                renderCustomLevels()

        if button8.collidepoint((mousePosition[0], mousePosition[1])):
            if click:
                isRunning = False

        # draw buttons and add hover effect
        # got logic for button hovering from pythonprogramming.net
        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 3.0 + 50 > mousePosition[
            1] > MAX_WIDTH / 3.0:
            pygame.draw.rect(screen, (0, 190, 0), button5)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button5)

        drawText('Level1', font, (255, 255, 255), screen, MAX_HEIGHT / 2.1, MAX_WIDTH / 2.9)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 2.4 + 50 > mousePosition[
            1] > MAX_WIDTH / 2.4:
            pygame.draw.rect(screen, (0, 190, 0), button6)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button6)

        drawText('Level2', font, (255, 255, 255), screen, MAX_HEIGHT / 2.1, MAX_WIDTH / 2.32)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 2.0 + 50 > mousePosition[
            1] > MAX_WIDTH / 2.0:
            pygame.draw.rect(screen, (0, 190, 0), button7)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button7)

        drawText('Custom', font, (255, 255, 255), screen, MAX_HEIGHT / 2.1, MAX_WIDTH / 1.95)

        if MAX_HEIGHT / 2.5 + 250 > mousePosition[0] > MAX_HEIGHT / 2.5 and MAX_WIDTH / 1.7 + 50 > mousePosition[
            1] > MAX_WIDTH / 1.7:
            pygame.draw.rect(screen, (0, 190, 0), button8)
        else:
            pygame.draw.rect(screen, (0, 255, 0), button8)

        drawText('Main Menu', font, (255, 255, 255), screen, MAX_HEIGHT / 2.2, MAX_WIDTH / 1.66)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def renderCustomLevels():
    click = False
    isRunning = True
    levelArray = LevelEditor.getSavedLevels()

    while isRunning:
        screen.fill(BACKGROUND_COLOR)
        drawText('Select Level', titleFont, (255, 255, 255), screen, 300, 50)
        mousePosition = pygame.mouse.get_pos()
        index = 1
        ycount = 0
        xcount = 0
        for level in levelArray:
            if index % 5 == 0:
                ycount += 1
                xcount = 0
            xpos = int(MAX_HEIGHT / 5.5) + (200 * xcount)
            ypos = int(MAX_WIDTH / 5.5) + (200 * ycount)
            button = pygame.Rect(xpos, ypos, 150, 150)

            if button.collidepoint((mousePosition[0], mousePosition[1])):
                if click:
                    game(game=level)

            if xpos + 150 > mousePosition[0] > xpos and ypos + 150 > mousePosition[
                1] > ypos:
                pygame.draw.rect(screen, (0, 190, 0), button)
            else:
                pygame.draw.rect(screen, (0, 255, 0), button)

            drawText(level, font, (255, 255, 255), screen, xpos + 10, ypos + 25)
            index += 1
            xcount += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    levels()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


if __name__ == '__main__':
    main()
