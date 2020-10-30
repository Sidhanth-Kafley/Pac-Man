import pygame
import random


class Ghost(pygame.sprite.Sprite):
    hitPacMan = False
    powerUpMode = False

    def __init__(self, color, position, images):
        # initialize super class
        super(Ghost, self).__init__()
        self.color = color

        # need to set the size of the images
        sizeOfImage = (64, 64)
        # index for looping through images
        self.index = 1
        # set the images
        self.images = images
        self.imagesDown = [self.images[0]]
        self.imagesLeft = [self.images[1]]
        self.imagesRight = [self.images[2]]
        self.imagesUp = [self.images[3]]
        self.image = self.images[0]

        self.rect = pygame.Rect(position, sizeOfImage)

        # set speed of the ghost
        self.velocity = pygame.math.Vector2()

    def update(self, dt):
        movements = random.randrange(10, 20)
        spacesMoved = 0

        if spacesMoved >= movements:
            self.velocity.x = 6*random.random() - 3
            self.velocity.y = 6*random.random() - 3
            movements = random.randrange(10, 20)
            spacesMoved = 0
        spacesMoved += 1

        if self.velocity.x > 0:
            self.images = self.imagesRight
        elif self.velocity.x < 0:
            self.images = self.imagesLeft
        elif self.velocity.y < 0:
            self.images = self.imagesUp
        elif self.velocity.y > 0:
            self.images = self.imagesDown

        # update the image
        if self.index >= len(self.images):
            self.index = 0
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

    # ghosts randomly moving in maze
    # def ghostMovements(self, movement):
    #     # determine what direction the ghost is moving and choose the correct image
    #     if movement == 'xRight':
    #         pass
    #     elif movement == 'xLeft':
    #         pass
    #     elif movement == 'yUp':
    #         pass
    #     elif movement == 'yDown':
    #         pass

