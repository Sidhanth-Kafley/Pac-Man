import pygame
import random
import math
from PathingGridController import PathingGridController

class Ghost(pygame.sprite.Sprite):

    def __init__(self, color, position, size, images, pathingGridController):
        # initialize super class
        super(Ghost, self).__init__()
        self.color = color
        self.powerUpMode = False
        self.hitPacMan = False
        self.position = position

        # index for looping through images
        self.index = 1
        # set the images
        self.images = images
        self.powerUpImage = [self.images[4]]
        self.imagesDown = [self.images[0]]
        self.imagesLeft = [self.images[1]]
        self.imagesRight = [self.images[2]]
        self.imagesUp = [self.images[3]]
        self.image = self.images[0]

        # initialize variables
        self.rect = pygame.Rect(position, size)
        self.moveX = 0
        self.moveY = 0
        self.direction = 'up'
        self.changeDirection = False
        self.moving = True
        self.drag = False
        self.pathingController = pathingGridController
        self.cellX = math.floor(self.rect.x / self.pathingController.cellWidth)
        self.cellY = math.floor(self.rect.y / self.pathingController.cellHeight)
        self.prevCellX = self.cellX
        self.prevCellY = self.cellY

        # initialize pathfinding variables
        self.pathingController.gridContents[self.cellY][self.cellX] = 1
        self.isPathing = False
        self.currentPathCell = [-1, 0, 0, 0, 0, 0]
        self.closedCells = []
        self.openCells = []
        self.pathCells = []
        self.nextPathCell = []
        self.nextPathCellIterator = 1

        # set speed of the ghost
        self.velocity = pygame.math.Vector2()

    # reset the ghost to its original position
    def resetPosition(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    # update the ghost (position, image, etc.)
    def update(self):

        self.prevCellX = self.cellX
        self.prevCellY = self.cellY
        self.cellX = math.floor(self.rect.x / self.pathingController.cellWidth)
        self.cellY = math.floor(self.rect.y / self.pathingController.cellHeight)
        cw = self.pathingController.cellWidth
        ch = self.pathingController.cellHeight

        if len(self.pathCells) > 1:
            self.nextPathCell = self.pathCells[len(self.pathCells) - self.nextPathCellIterator]
            if self.moveToPoint(self.nextPathCell[0] * cw, self.nextPathCell[1] * ch, 2):
                self.nextPathCellIterator += 1

            if self.rect.x == self.pathCells[0][0] * cw and self.rect.y == self.pathCells[0][1] * ch:
                self.nextPathCell = []
                self.nextPathCellIterator = 1
                self.pathCells.clear()

        # # move the ghost to its next path cell if a path is found
        # if len(self.pathCells) > 1:
        #     if self.nextPathCell == []:
        #         self.nextPathCell = self.pathCells[len(self.pathCells) - 1]
        #
        #     if self.rect.x != self.nextPathCell[0] * cw:
        #         self.velocity.x = 1 * math.copysign(1, self.nextPathCell[0] * cw - self.rect.x)
        #         self.velocity.y = 0
        #     if self.rect.y != self.nextPathCell[1] * ch:
        #         self.velocity.y = 1 * math.copysign(1, self.nextPathCell[1] * ch - self.rect.y)
        #         self.velocity.x = 0
        #
        #     # begin moving to the next cell in the path
        #     if self.rect.x == self.nextPathCell[0] * cw and self.rect.y == self.nextPathCell[1] * ch:
        #     #if self.rect.x == self.nextPathCell[0] * cw:
        #         self.nextPathCellIterator += 1
        #         self.nextPathCell = self.pathCells[len(self.pathCells) - self.nextPathCellIterator]
        #
        #     # stop the ghost once it reaches its target cell
        #     if self.rect.x == self.pathCells[0][0] * cw:
        #         self.velocity.x = 0
        #     if self.rect.y == self.pathCells[0][1] * ch:
        #         self.velocity.y = 0
        #     if self.rect.x == self.pathCells[0][0] * cw and self.rect.y == self.pathCells[0][1] * ch:
        #         self.nextPathCell = []
        #         self.nextPathCellIterator = 1
        #         self.pathCells.clear()

        # power up ghost
        if self.powerUpMode:
            self.index = 4
        elif not self.powerUpMode:
            self.index = 1
        # ghost moving down
        elif self.velocity.x == 0 and self.velocity.y > 0:
            self.index = 0
        # ghost moving left
        elif self.velocity.x < 0 and self.velocity.y == 0:
            self.index = 1
        # ghost moving right
        elif self.velocity.x > 0 and self.velocity.y == 0:
            self.index = 2
        # ghost moving up
        elif self.velocity.x == 0 and self.velocity.y < 0:
            self.index = 3

        # update location in pathing controller grid, clear past location
        if self.prevCellX != self.cellX or self.prevCellY != self.cellY:
            self.pathingController.gridContents[self.cellY][self.cellX] = 1
            self.pathingController.gridContents[self.prevCellY][self.prevCellX] = 0

        self.rect.move_ip(*self.velocity)

        # update the image of ghost
        self.image = self.images[self.index]

    def moveToPoint(self, targetX, targetY, magnitude):
        if self.rect.x > targetX:
            self.velocity.x = -magnitude
        if self.rect.x < targetX:
            self.velocity.x = magnitude
        if self.rect.y > targetY:
            self.velocity.y = -magnitude
        if self.rect.y < targetY:
            self.velocity.y = magnitude
        if abs(self.rect.x - targetX) <= magnitude and abs(self.rect.y - targetY) <= magnitude:
            self.velocity.x = 0
            self.velocity.y = 0
            return True

    # helper function for pathfindToPoint for searching through a list
    def isInOpenCells(self, list, element):
        for item in list:
            if element[0] == item[0] and element[1] == item[1]:
                return True
        return False

    # helper function for pathfindToPoint for searching through a list
    def getPrevClosedCellIndex(self, list, element):
        for i in range(len(list)):
            if element[2] == list[i][0] and element[3] == list[i][1]:
                return i
        return -1

    # use A* to pathfind to a given cell in the grid
    def pathfindToPoint(self, targetCellX, targetCellY):
        self.isPathing = True
        self.closedCells.clear()
        self.openCells.clear()
        openCellsHistory = []

        # re-initialize currentPathCell
        self.currentPathCell = [self.cellX, self.cellY, self.cellX, self.cellY, 0, 0]

        pathingAttemptLimiter = 0
        while self.isPathing:
            pathingAttemptLimiter += 1
            # check if target cell has been reached
            if abs(self.currentPathCell[0] - targetCellX) <= 1 and abs(self.currentPathCell[1] - targetCellY) <= 1:
                self.isPathing = False
                break

            # add current cell to closed cells
            if len(self.closedCells) == 0:
                self.closedCells.append([self.cellX, self.cellY, self.cellX, self.cellY, 0, 0])

            # some local variables for convenience
            roomH = self.pathingController.roomHeight
            roomW = self.pathingController.roomWidth
            pathingGrid = self.pathingController.gridContents

            # initialize f and h score variables
            # (initial values here don't really matter that much as long as they're absurdly large)
            minFScore = roomW * roomW + roomH * roomH
            tempGScore = minFScore
            tempHScore = minFScore
            tempFScore = tempGScore + tempHScore
            cpc = self.currentPathCell

            # check neighboring cells, add free neighbor cells to openCells list
            if pathingGrid[cpc[1]-1][cpc[0]] == 0 and not self.isInOpenCells(openCellsHistory, [cpc[0], cpc[1]-1]):
                tempGScore = math.sqrt(pow(self.cellX - cpc[0], 2) + pow(self.cellY - cpc[1]-1, 2))
                tempHScore = math.sqrt(pow(cpc[0] - targetCellX, 2) + pow(cpc[1]-1 - targetCellY, 2))
                tempFScore = tempGScore + tempHScore
                self.openCells.append([cpc[0], cpc[1]-1, cpc[0], cpc[1], tempFScore])
                openCellsHistory.append([cpc[0], cpc[1]-1, cpc[0], cpc[1], tempFScore])

            if pathingGrid[cpc[1]][cpc[0]+1] == 0 and not self.isInOpenCells(openCellsHistory, [cpc[0]+1, cpc[1]]):
                tempGScore = math.sqrt(pow(self.cellX - cpc[0]+1, 2) + pow(self.cellY - cpc[1], 2))
                tempHScore = math.sqrt(pow(cpc[0]+1 - targetCellX, 2) + pow(cpc[1] - targetCellY, 2))
                tempFScore = tempGScore + tempHScore
                self.openCells.append([cpc[0]+1, cpc[1], cpc[0], cpc[1], tempFScore])
                openCellsHistory.append([cpc[0]+1, cpc[1], cpc[0], cpc[1], tempFScore])

            if pathingGrid[cpc[1]+1][cpc[0]] == 0 and not self.isInOpenCells(openCellsHistory, [cpc[0], cpc[1]+1]):
                tempGScore = math.sqrt(pow(self.cellX - cpc[0], 2) + pow(self.cellY - cpc[1]+1, 2))
                tempHScore = math.sqrt(pow(cpc[0] - targetCellX, 2) + pow(cpc[1]+1 - targetCellY, 2))
                tempFScore = tempGScore + tempHScore
                self.openCells.append([cpc[0], cpc[1]+1, cpc[0], cpc[1], tempFScore])
                openCellsHistory.append([cpc[0], cpc[1]+1, cpc[0], cpc[1], tempFScore])

            if pathingGrid[cpc[1]][cpc[0]-1] == 0 and not self.isInOpenCells(openCellsHistory, [cpc[0]-1, cpc[1]]):
                tempGScore = math.sqrt(pow(self.cellX - cpc[0]-1, 2) + pow(self.cellY - cpc[1], 2))
                tempHScore = math.sqrt(pow(cpc[0]-1 - targetCellX, 2) + pow(cpc[1] - targetCellY, 2))
                tempFScore = tempGScore + tempHScore
                self.openCells.append([cpc[0]-1, cpc[1], cpc[0], cpc[1], tempFScore])
                openCellsHistory.append([cpc[0]-1, cpc[1], cpc[0], cpc[1], tempFScore])

            # identify the open cell with the lowest f score, update currentPathCell
            # TODO: optimize this with a priority queue
            for i in range(len(self.openCells)):
                if self.openCells[i][4] < minFScore:
                    minFScore = self.openCells[i][4]
                    self.currentPathCell = self.openCells[i].copy()
            self.openCells.remove(self.currentPathCell)

            # add neighboring cell with smallest f score to closedCells
            self.closedCells.append(self.currentPathCell)
            if pathingAttemptLimiter == len(pathingGrid) * len(pathingGrid[0]):
                self.isPathing = False

        # retrace the path through the closed cells
        if len(self.closedCells) > 0:
            self.pathCells.clear()
            self.nextPathCellIterator = 1
            self.pathCells.append(self.closedCells[len(self.closedCells) - 1])
            for i in range(len(self.closedCells) - 1):
                prevIndex = self.getPrevClosedCellIndex(self.closedCells, self.pathCells[i])
                self.pathCells.append(self.closedCells[prevIndex])

                # break once the starting cell is reached
                if self.closedCells[prevIndex] == self.closedCells[0]:
                    break

        # note: ghosts will move automatically to their next path cell in their update function


    # get the color of the ghost
    def getGhostColor(self):
        return self.color

    # get the direction of the ghost
    def getGhostDirection(self):
        return self.direction

    # get the x position of the ghost
    def getXPosition(self):
        return self.rect.x

    # get the y position of the ghost
    def getYPosition(self):
        return self.rect.y

    # set the x position of the ghost
    def setXPosition(self, xPosition):
        self.rect.x = xPosition

    # set the y position of the ghost
    def setYPosition(self, yPosition):
        self.rect.y = yPosition

    # ghost hits pac-man
    def hitPacMan(self):
        # pac-man loses a life
        self.hitPacMan = True

    # pac-man is in power-up mode and can eat the ghosts
    def setPowerUpMode(self):
        self.powerUpMode = not self.powerUpMode

    # move ghosts in maze in the selected direction
    def moveGhosts(self):
        if self.moving:
            if self.direction == 'right':
                self.moveX = 5
            elif self.direction == 'left':
                self.moveX = -5
            elif self.direction == 'down':
                self.moveY = 5
            elif self.direction == 'up':
                self.moveY = -5

    # ghost hit a wall
    def ghostHitWall(self, ghostStopMoving):
        self.moving = ghostStopMoving
        self.changeDirection = True

    # ghost needs to choose a new direction
    def chooseDirection(self):
        self.direction = random.choice(['right', 'left', 'down', 'up'])
        return self.direction
