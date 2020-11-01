import pygame
import random
moving = True


class Ghost(pygame.sprite.Sprite):
    moving = True
    direction = 'up'

    def __init__(self, color, position, images):
        # initialize super class
        super(Ghost, self).__init__()
        self.color = color
        self.powerUpMode = False
        self.hitPacMan = False
        self.position = position
        # set the size of the images
        sizeOfImage = (40, 40)

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
        #self.direction = 'up'
        self.changeDirection = False
        #self.moving = True

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
        print(self.changeDirection)
        if self.changeDirection:
            self.chooseDirection()
        self.moveGhosts()
        #print(self.getColorOfPixelsAhead())
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
        #print(self.moving)
        if moving:
            if self.direction == 'right':
                self.moveX = 5
            elif self.direction == 'left':
                self.moveX = -5
            elif self.direction == 'down':
                self.moveY = 5
            elif self.direction == 'up':
                self.moveY = -5

        #self.moveX = random.choice([-2, 2])
        #self.moveY = random.choice([-2, 2])

    def getColorOfPixelsAhead(self, ahead=1):
        rect = pygame.Rect(self.rect.x, self.rect.y, 40, 40)
        xyAhead = []
        if self.direction == 'right':
            xyAhead = (rect.midright[0] + ahead, rect.midright[1])
        elif self.direction == 'left':
            xyAhead = (rect.midleft[0] - ahead, rect.midleft[1])
        elif self.direction == 'down':
            xyAhead = (rect.midbottom[0], rect.midbottom[1] + 1)
        elif self.direction == 'up':
            xyAhead = (rect.midtop[0], rect.midtop[1] - ahead)

        return xyAhead

    def ghostHitWall(self, ghostStopMoving):
        self.moving = ghostStopMoving
        self.changeDirection = True

    def chooseDirection(self):
        self.direction = random.choice(['right', 'left', 'down', 'up'])
