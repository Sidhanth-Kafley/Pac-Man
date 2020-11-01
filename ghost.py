import pygame
import random


class Ghost(pygame.sprite.Sprite):

    def __init__(self, color, position, images):
        # initialize super class
        super(Ghost, self).__init__()
        self.color = color
        self.powerUpMode = False
        self.hitPacMan = False
        self.position = position
        # set the size of the images
        sizeOfImage = (30, 30)

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
        self.rect = pygame.Rect(position, sizeOfImage)
        self.moveX = 0
        self.moveY = 0
        self.direction = 'up'
        self.changeDirection = False
        self.moving = True

        # set speed of the ghost
        self.velocity = pygame.math.Vector2()

    # reset the ghost to its original position
    def resetPosition(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    # update the ghost (position, image, etc.)
    def update(self):
        # if ghost can move, then move ghost
        if self.moving:
            self.moveGhosts()
            self.rect.x += self.moveX
            self.rect.y += self.moveY

        # power up ghost
        if self.powerUpMode:
            self.index = 4
        # ghost moving down
        elif self.moveX == 0 and self.moveY > 0:
            self.index = 0
        # ghost moving left
        elif self.moveX < 0 and self.moveY == 0:
            self.index = 1
        # ghost moving right
        elif self.moveX > 0 and self.moveY == 0:
            self.index = 2
        # ghost moving up
        elif self.moveX == 0 and self.moveY < 0:
            self.index = 3

        # update the image of ghost
        self.image = self.images[self.index]

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
    def powerUpMode(self):
        self.powerUpMode = True

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
