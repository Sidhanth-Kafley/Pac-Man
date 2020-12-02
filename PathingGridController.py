import pygame
import os
import math
from Wall import Wall
from Level import Level


class PathingGridController(pygame.sprite.Sprite):
    currentLevel = 0
    cellWidth = 0
    cellHeight = 0
    roomWidth = 0
    roomHeight = 0
    gridWidth = 0
    gridHeight = 0
    gridContents = []

    def __init__(self, currentLevel, cellWidth, cellHeight, roomWidth, roomHeight):

        # initialize super class
        super(PathingGridController, self).__init__()

        # initialize fields
        self.currentLevel = currentLevel
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.roomWidth = roomWidth
        self.roomHeight = roomHeight
        self.gridWidth = math.floor(roomWidth / cellWidth)
        self.gridHeight = math.floor(roomHeight / cellHeight)

        # populate gridContents with empty cells
        for i in range(self.gridHeight):
            self.gridContents.append([])
            for j in range(self.gridWidth):
                self.gridContents[i].append(0)

        # populate gridContents with wall cells
        for i in range(len(self.currentLevel.walls)):
            wallCellX = math.floor(self.currentLevel.walls[i].position[0] / self.cellWidth)
            wallCellY = math.floor(self.currentLevel.walls[i].position[1] / self.cellHeight)
            if self.currentLevel.walls[i].imagePath != 'Gate.png':
                self.gridContents[wallCellY][wallCellX] = 1

    # function draws grid for debugging and level building
    def drawGrid(self, background):
        for i in range(self.gridHeight):
            pygame.draw.line(background, (255, 255, 255), (0, i * self.cellHeight), (self.roomWidth, i * self.cellHeight))
        for i in range(self.gridWidth):
            pygame.draw.line(background, (255, 255, 255), (i * self.cellWidth, 0), (i * self.cellWidth, self.roomHeight))

        for i in range(len(self.gridContents)):
            for j in range(len(self.gridContents[i])):
                if self.gridContents[i][j] == 1:
                    pygame.draw.rect(background, (255, 0, 0), pygame.Rect(j * self.cellWidth, i * self.cellHeight, self.cellWidth, self.cellHeight))

    def drawCellsList(self, background, cellsList, color):
        for i in range(len(cellsList)):
            pygame.draw.rect(background, color, pygame.Rect(cellsList[i][0] * self.cellWidth, cellsList[i][1] * self.cellHeight, self.cellWidth, self.cellHeight))
