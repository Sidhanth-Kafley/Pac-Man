import pygame
import os

from Wall import Wall

class Level():
    layout = [[]]
    walls = []
    pointPills = []
    powerUpPointPills = []
    layoutFile = 0
    wallSize = (16, 16)

    def __init__(self, layoutFilename, wallSize):
        # initialize super class
        super(Level, self).__init__()
        layoutFile = open(layoutFilename, 'r', encoding='utf8')
        rows = layoutFile.read().splitlines()

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
            self.layout.append([])

    def appendWall(self, imageFilename, rowIndex, colIndex):
        image = pygame.image.load('WallSprites' + os.sep + imageFilename).convert_alpha()
        tempWall = Wall(position=(colIndex * self.wallSize[0], rowIndex * self.wallSize[1]), size=(self.wallSize[0], self.wallSize[1]), image=image)
        self.walls.append(tempWall)
        self.layout[rowIndex].append(tempWall)