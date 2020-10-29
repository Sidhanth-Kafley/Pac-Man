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
        sizeOfImage = (64, 64)

        # index for looping through images
        self.index = 1
        # set the images
        self.images = images
        self.powerUpImage = [self.images[4]]
        self.imagesDown = [self.images[0]]
        self.imagesLeft = [self.images[1]]
        self.imagesRight = [self.images[2]]
        self.imagesUp = [self.images[3]]

        # initialize variables
        self.rect = pygame.Rect(position, sizeOfImage)
        self.moveX = 0
        self.moveY = 0
        self.direction = 'up'

        # set speed of the ghost
        self.velocity = pygame.math.Vector2()

    # reset the ghost to its original position
    def resetPosition(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    # update the ghost (position, image, etc.)
    def update(self):
        # self.moveX = random.randint(-5, 5)
        # self.moveY = random.randrange(-5, 5)
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

    # ghost hits pac-man
    def hitPacMan(self):
        # pac-man loses a life
        self.hitPacMan = True

    # pac-man is in power-up mode and can eat the ghosts
    def powerUpMode(self):
        self.powerUpMode = True

    def moveGhosts(self):
        if self.direction == 'right':
            self.moveX = 5
        elif self.direction == 'left':
            self.moveX = -5
        elif self.direction == 'down':
            self.moveY = 5
        elif self.direction == 'up':
            self.moveY = -5


