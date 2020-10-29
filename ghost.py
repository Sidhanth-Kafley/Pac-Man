import pygame
import random


class Ghost(pygame.sprite.Sprite):
    hitPacMan = False
    powerUpMode = False

    def __init__(self, color, position, images):
        # initialize super class
        super(Ghost, self).__init__()
        self.color = color
        self.position = position
        # set the size of the images
        sizeOfImage = (64, 64)

        # index for looping through images
        self.index = 1
        # set the images
        self.images = images
        self.imagesDown = [self.images[0]]
        self.imagesLeft = [self.images[1]]
        self.imagesRight = [self.images[2]]
        self.imagesUp = [self.images[3]]

        self.rect = pygame.Rect(position, sizeOfImage)
        self.moveX = 0
        self.moveY = 0

        # set speed of the ghost
        self.velocity = pygame.math.Vector2()

    # reset the ghost to its original position
    def resetPosition(self):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    # update the ghost (position, image, etc.)
    def update(self):
        # movements = random.randrange(10, 20)
        # spacesMoved = 0
        #
        # if spacesMoved >= movements:
        #     self.velocity.x = 6*random.random() - 3
        #     self.velocity.y = 6*random.random() - 3
        #     movements = random.randrange(10, 20)
        #     spacesMoved = 0
        # spacesMoved += 1

        #self.moveX = random.randint(-5, 5)
        #self.moveY = random.randrange(-5, 5)

        self.rect.x += self.moveX
        self.rect.y += self.moveY

        # make sure the ghost doesn't leave the screen
        if self.rect.y > 700 or self.rect.x > 900:
            self.resetPosition()

        # ghost moving down
        if self.moveX == 0 and self.moveY > 0:
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

