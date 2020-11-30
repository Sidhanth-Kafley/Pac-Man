import pygame
import os
from Wall import Wall
from Level import Level


class PathingGridController(pygame.sprite.Sprite):
    currentLevel = 0
    cellWidth = 0
    cellHeight = 0
    gridWidth = 0
    gridHeight = 0
    gridContents = []

    def __init__(self, currentLevel, cellWidth, cellHeight):
        # initialize super class
        super(PathingGridController, self).__init__()

        self.currentLevel = currentLevel
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.gridWidth = len(self.currentLevel.layout[0])
        self.gridHeight = len(self.currentLevel.layout)

        # Populate gridContents
        # 0 represents an empty cell, 1 a wall, and a different higher number for any other object occupying a cell
        for i in range(self.gridHeight):
            self.gridContents.append([])
            for j in range(self.gridWidth):
                try:
                    layoutCell = self.currentLevel.layout[i][j]
                    if type(layoutCell) == Wall:
                        self.gridContents[i].append(1)
                    elif layoutCell == '' or layoutCell == '*' or layoutCell == '&':
                        self.gridContents[i].append(0)
                except IndexError:
                    self.gridContents[i].append(0)


