import pygame
import os
from pill import Pill
from Wall import Wall


class Level(pygame.sprite.Sprite):
    layout = [[]]
    walls = []
    pointPills = []
    powerUpPointPills = []
    layoutFile = 0
    wallSize = (4, 4)
    originPosition = (0, 0)
    wallBlocks = []
    levelWidth = 0
    levelHeight = 0
    pacmanAndGhost = []

    def __init__(self, layoutFilename, wallSize, originPosition):
        # initialize super class
        super(Level, self).__init__()
        layoutFile = open(layoutFilename, 'r', encoding='utf8')
        rows = layoutFile.read().splitlines()
        self.wallSize = wallSize
        self.originPosition = originPosition
        self.levelHeight = wallSize[1] * len(rows)
        self.levelWidth = wallSize[0] * len(rows[0])
        pillImage = pygame.image.load("PointPill.png").convert_alpha()
        pillImage = pygame.transform.scale(pillImage, (int(wallSize[0]), int(wallSize[1])))
        powerPillImage = pygame.image.load("PowerUpPointPill.png").convert_alpha()
        powerPillImage = pygame.transform.scale(powerPillImage, (int(wallSize[0]), int(wallSize[1])))
        self.pills = []
        self.layoutFilename = layoutFilename
        self.wallBlocks.clear()
        self.walls.clear()

        # create level objects based on characters in file
        for i in range(len(rows)):
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
                    self.pills.append(Pill(False, pillImage, ((j * self.wallSize[1]) + self.originPosition[0] + int(wallSize[0]/2), (i * self.wallSize[0]) + self.originPosition[1] + int(self.wallSize[0])/2)))
                elif rows[i][j] == "&":
                    self.pills.append(Pill(True, powerPillImage, ((j * self.wallSize[1]) + self.originPosition[0] + 5, (i * self.wallSize[0]) + self.originPosition[1])))
            self.layout.append([])

    def appendWall(self, imageFilename, rowIndex, colIndex):
        image = pygame.image.load('WallSprites' + os.sep + imageFilename).convert_alpha()
        tempWall = Wall(position=((colIndex * self.wallSize[0]) + self.originPosition[0], (rowIndex * self.wallSize[1]) + self.originPosition[1]), size=(self.wallSize[0], self.wallSize[1]), image=image, imagePath=imageFilename)
        self.walls.append(tempWall)
        self.layout[rowIndex].append(tempWall)
        self.wallBlocks.append(tempWall.rect)

    def __delete__(self, instance):
        del self.walls
        return True

