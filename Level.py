import pygame
import os
from pill import Pill

from Wall import Wall

class Level():
    layout = [[]]
    walls = []
    pointPills = []
    powerUpPointPills = []
    layoutFile = 0
    wallSize = (16, 16)
    originPosition = (0, 0)
    wallBlocks = []

    def __init__(self, layoutFilename, wallSize, originPosition):
        # initialize super class
        super(Level, self).__init__()
        layoutFile = open(layoutFilename, 'r', encoding='utf8')
        rows = layoutFile.read().splitlines()
        self.wallSize = wallSize
        self.originPosition = originPosition
        pillImage = pygame.image.load("PointPill.png").convert_alpha()
        pillImage = pygame.transform.scale(pillImage, (int(20), int(20)))
        self.pills = []

        # create level objects based on characters in file
        print(len(rows))
        for i in range(len(rows)):
            print(rows[i])
            for j in range(len(rows[i])):
                if rows[i][j] == ' ':
                    self.layout[i].append('')
                elif rows[i][j] == '╔':
                    self.appendWall('CornerTopLeft.png', i, j)
                elif rows[i][j] == '╗':
                    self.appendWall('CornerTopRight.png', i, j)
                elif rows[i][j] == '╚':
                    self.appendWall('CornerBottomLeft.png', i, j)
                elif rows[i][j] == '╝':
                    self.appendWall('CornerBottomRight.png', i, j)
                elif rows[i][j] == '║':
                    self.appendWall('VerticalOpen.png', i, j)
                elif rows[i][j] == '┴':
                    self.appendWall('VerticalClosedBottom.png', i, j)
                elif rows[i][j] == '┬':
                    self.appendWall('VerticalClosedTop.png', i, j)
                elif rows[i][j] == '╠':
                    self.appendWall('VerticalIntersectionRight.png', i, j)
                elif rows[i][j] == '╣':
                    self.appendWall('VerticalIntersectionLeft.png', i, j)
                elif rows[i][j] == '═':
                    self.appendWall('HorizontalOpen.png', i, j)
                elif rows[i][j] == '├':
                    self.appendWall('HorizontalClosedLeft.png', i, j)
                elif rows[i][j] == '┤':
                    self.appendWall('HorizontalClosedRight.png', i, j)
                elif rows[i][j] == '╦':
                    self.appendWall('HorizontalIntersectionDown.png', i, j)
                elif rows[i][j] == '╩':
                    self.appendWall('HorizontalIntersectionUp.png', i, j)
                elif rows[i][j] == '_':
                    self.appendWall('Gate.png', i, j)
                elif rows[i][j] == "*":
                    self.pills.append(Pill(False, pillImage, ((j * self.wallSize[1]) + self.originPosition[0], (i * self.wallSize[0] + 13) + self.originPosition[1] - 7)))
                elif rows[i][j] == "&":
                    self.pills.append(Pill(True, pygame.transform.scale(pillImage, (50, 50)), ((j * self.wallSize[1]) + self.originPosition[0] - 10, (i * self.wallSize[0]) + self.originPosition[1] - 20)))
            self.layout.append([])

    def appendWall(self, imageFilename, rowIndex, colIndex):
        image = pygame.image.load('WallSprites' + os.sep + imageFilename).convert_alpha()
        tempWall = Wall(position=((colIndex * self.wallSize[0]) + self.originPosition[0], (rowIndex * self.wallSize[1]) + self.originPosition[1]), size=(self.wallSize[0], self.wallSize[1]), image=image)
        self.walls.append(tempWall)
        self.layout[rowIndex].append(tempWall)
        self.wallBlocks.append(tempWall.rect)