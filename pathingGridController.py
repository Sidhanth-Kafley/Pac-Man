import pygame
import os
from Level import Level


class PathingGridController(pygame.sprite.Sprite):
    currentLevel = 0
    cellWidth = 0
    cellHeight = 0

    def __init__(self, currentLevel, cellWidth, cellHeight):
        # initialize super class
        super(PathingGridController, self).__init__()
        
        self.currentLevel = currentLevel
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight



