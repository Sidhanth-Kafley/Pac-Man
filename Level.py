import pygame

class Level():
    walls = []
    pointPills = []
    powerUpPointPills = []
    layoutFile = 0

    def __init__(self, layoutFilename):
        # initialize super class
        super(Level, self).__init__()
        layoutFile = open(layoutFilename, 'r')
        rowStrings = layoutFile.read().splitlines()
        for row in rowStrings:
            print(row)

