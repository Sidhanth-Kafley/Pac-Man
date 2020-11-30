import pygame
import os
import math
from Wall import Wall
from Level import Level


class PathingGridController(pygame.sprite.Sprite):
    currentLevel = 0
    cellWidth = 0
    cellHeight = 0
    gridWidth = 0
    gridHeight = 0
    gridContents = []

    def __init__(self, currentLevel, cellWidth, cellHeight, roomWidth, roomHeight):
        # initialize super class
        super(PathingGridController, self).__init__()

        self.currentLevel = currentLevel
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.gridWidth = math.floor(roomWidth / cellWidth)
        self.gridHeight = math.floor(roomHeight / cellHeight)

        # Populate gridContents with empty cells
        for i in range(self.gridHeight):
            self.gridContents.append([])
            for j in range(self.gridWidth):
                self.gridContents[i].append([0])

        # Populate gridContents with wall cells
        for i in range(len(self.currentLevel.walls)):
            wallCellX = math.floor(self.currentLevel.walls[i].position[0] / self.cellWidth)
            wallCellY = math.floor(self.currentLevel.walls[i].position[1] / self.cellHeight)
            self.gridContents[wallCellY][wallCellX] = 1



