import pygame
import os


class PacMan(pygame.sprite.Sprite):
    startingHealth = 3
    powerUp = 1
    baseMoveSpeed = 3
    eatenGhosts = 0
    totalPoints = 0
    ghostPoints = 200
    deathDown = []
    deathUp = []
    deathLeft = []
    deathRight = []
    imagesDeath = []
    death = False
    index = 0
    size = (8, 8)
    velocity = pygame.math.Vector2()

    def __init__(self, position, size, images):
        # initialize super class
        super(PacMan, self).__init__()
        # set image streams for moving in respective directions
        self.images = images
        self.size = size
        self.imagesRight = [self.images[4], self.images[2]]
        self.imagesLeft = [self.images[4], self.images[1]]
        self.imagesUp = [self.images[4], self.images[3]]
        self.imagesDown = [self.images[4], self.images[0]]
        self.imagesStop = [self.images[4]]
        # sets the object's position and size on the background
        self.position = position
        self.rect = pygame.Rect(position, self.size)
        self.collisionRect = pygame.Rect(position, (32, 32))
        # sets the current image (closed circle to start)
        self.image = self.images[1]
        self.loadDeathImages()
        self.imagesDeath = self.deathRight
        self.drag = False

    def update(self):
        if not self.death:
            # set the array of images to the appropriate direction
            if self.velocity.x > 0:
                self.images = self.imagesRight
            elif self.velocity.x < 0:
                self.images = self.imagesLeft
            elif self.velocity.y < 0:
                self.images = self.imagesUp
            elif self.velocity.y > 0:
                self.images = self.imagesDown
            elif self.velocity.x == self.velocity.y:
                self.images = self.imagesStop
            # loop through the images of the index
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            # moves the image on the screen according to the set velocity
            self.rect.move_ip(*self.velocity)
            self.collisionRect.move_ip(*self.velocity)
        else:
            if self.velocity.x > 0:
                self.imagesDeath = self.deathRight
            elif self.velocity.x < 0:
                self.imagesDeath = self.deathLeft
            elif self.velocity.y < 0:
                self.imagesDeath = self.deathUp
            elif self.velocity.y > 0:
                self.imagesDeath = self.deathDown
            self.images = self.imagesDeath
            self.velocity.x = 0
            self.velocity.y = 0
            self.index += 1
            if self.index >= len(self.images):
                self.newLife()
            self.image = self.images[self.index]
            # moves the image on the screen according to the set velocity
            self.rect.move_ip(*self.velocity)
            self.collisionRect.move_ip(*self.velocity)
        # stop chomping on wall impact
        if self.velocity.x == 0 and self.velocity.y == 0:
            self.image = self.imagesStop[0]

    def hit(self):
        self.startingHealth -= 1

    def setPowerUp(self):
        if self.powerUp == 1:
            self.powerUp = 1.5
        else:
            self.powerUp = 1

    def eatGhost(self, ghost):
        # ghost.hit()
        ghost.resetGhost()
        ghost.powerUpMode = False
        self.totalPoints += self.ghostPoints
        self.ghostPoints = self.ghostPoints*2

    def resetGhostPoints(self):
        self.ghostPoints = 200

    def renderScore(self, size):
        fontName = pygame.font.match_font('arial')
        font = pygame.font.Font(fontName, size)
        text = font.render(str(self.totalPoints), True, (25, 25, 166))
        return text

    def deathAnimation(self):
        self.death = True

    def loadDeathImages(self):
        path = "PacManDeath"
        images = [0, 0, 0, 0, 0, 0, 0, 0]
        for file in os.listdir(path):
            image = pygame.image.load(path + os.sep + file).convert_alpha()
            image = pygame.transform.scale(image, self.size)
            if "1" in file:
                images[0] = image
            elif "2" in file:
                images[1] = image
            elif "3" in file:
                images[2] = image
            elif "4" in file:
                images[3] = image
            elif "5" in file:
                images[4] = image
            elif "6" in file:
                images[5] = image
            elif "7" in file:
                images[6] = image
            elif "8" in file:
                images[7] = image
        for x in images:
            self.deathLeft.append(pygame.transform.rotate(x, 180))
            self.deathUp.append(pygame.transform.rotate(x, 90))
            self.deathDown.append(pygame.transform.rotate(x, 270))
            self.deathRight.append(x)

    def newLife(self):
        self.death = False
        self.startingHealth -= 1
        self.rect = pygame.Rect(self.position, self.size)
        self.image = self.images[1]
        self.index = 0

    def eatPill(self, pill):
        if pill.isPower():
            if self.powerUp != 1.5:
                self.setPowerUp()
                return True
        self.totalPoints += 10
        del pill
        return False

    def checkMove(self, direction, potentialCollidingWalls, level1):
        # for wallIndex in potentialCollidingWalls.walls:
        #     if self.collisionRect.colliderect(wallIndex):
        #         if "left" in direction:
        #             if self.collisionRect.left == wallIndex.rect.right: # self.collisionRect.collidepoint(wallIndex.rect.x, wallIndex.rect.y) and wallIndex.rect.center[0] < self.collisionRect.center[0]:
        #                 return False
        #         elif "right" in direction:
        #             if self.collisionRect.right == wallIndex.rect.left: # self.collisionRect.collidepoint(wallIndex.rect.x, wallIndex.rect.y) and wallIndex.rect.center[0] > self.collisionRect.center[0]:
        #                 return False
        #         elif "up" in direction:
        #             if self.collisionRect.top == wallIndex.rect.bottom: # self.collisionRect.collidepoint(wallIndex.rect.x, wallIndex.rect.y) and wallIndex.rect.center[1] < self.collisionRect.center[1]:
        #                 return False
        #         elif "down" in direction:
        #             if self.collisionRect.bottom == wallIndex.rect.top: # self.collisionRect.collidepoint(wallIndex.rect.x, wallIndex.rect.y) and wallIndex.rect.center[1] > self.collisionRect.center[1]:
        #                 return False
           # if self.rect.colliderect(level1.walls[wallIndex]):
        return True

    def getTotalPoints(self):
        return self.totalPoints
