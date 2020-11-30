import pygame
import os


class PacMan(pygame.sprite.Sprite):
    startingHealth = 3
    powerUp = False
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
        self.collisionRect = pygame.Rect(position, (16, 16))
        self.collisionRectTop = pygame.Rect(position, (16, 16))
        self.collisionRectTop.bottom = self.collisionRect.top
        self.collisionRectBottom = pygame.Rect(position, (16, 16))
        self.collisionRectBottom.top = self.collisionRect.bottom
        self.collisionRectLeft = pygame.Rect(position, (16, 16))
        self.collisionRectLeft.right = self.collisionRect.left
        self.collisionRectRight = pygame.Rect(position, (16, 16))
        self.collisionRectRight.left = self.collisionRect.right
        # sets the current image (closed circle to start)
        self.image = self.images[1]
        self.loadDeathImages()
        self.drag = False
        self.timer = 0

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
            if self.timer % 10 == 0:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
                self.timer = 1
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
            if self.timer % 10 == 0:
                self.index += 1
                if self.index >= len(self.images):
                    self.newLife()
                self.image = self.images[self.index]
                self.timer = 1
        # moves the image on the screen according to the set velocity
        self.rect.move_ip(*self.velocity)
        self.collisionRect.center = self.rect.center
        self.collisionRectTop.bottom = self.collisionRect.top
        self.collisionRectTop.left = self.collisionRect.left
        self.collisionRectBottom.top = self.collisionRect.bottom
        self.collisionRectBottom.left = self.collisionRect.left
        self.collisionRectLeft.right = self.collisionRect.left
        self.collisionRectLeft.top = self.collisionRect.top
        self.collisionRectRight.left = self.collisionRect.right
        self.collisionRectRight.top = self.collisionRect.top
        self.timer += 1
        # stop chomping on wall impact
        if self.velocity.x == 0 and self.velocity.y == 0 and not self.death:
            self.image = self.imagesStop[0]

    def hit(self):
        self.startingHealth -= 1

    def setPowerUp(self):
        self.powerUp = not self.powerUp

    def eatGhost(self, ghost):
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

    def checkMove(self, direction, level):
        for wall in level.walls:
            if direction == "up":
                if wall.rect.colliderect(self.collisionRectTop):
                    return False
            elif direction == "down":
                if wall.rect.colliderect(self.collisionRectBottom):
                    return False
            elif direction == "left":
                if wall.rect.colliderect(self.collisionRectLeft):
                    return False
            elif direction == "right":
                if wall.rect.colliderect(self.collisionRectRight):
                    return False
        return True

    def checkMotion(self, level):
        check = False
        for wall in level.walls:
            if not check:
                if self.velocity.x > 0:
                    if self.collisionRectRight.left + 5 == wall.rect.left and self.collisionRectRight.colliderect(wall.rect):
                        check = True
                if self.velocity.x < 0:
                    if self.collisionRectLeft.right - 5 == wall.rect.right and self.collisionRectLeft.colliderect(wall.rect):
                        check = True
                if self.velocity.y > 0:
                    if self.collisionRectBottom.top + 5 == wall.rect.top and self.collisionRectBottom.colliderect(wall.rect):
                        check = True
                if self.velocity.y < 0:
                    if self.collisionRectTop.bottom - 5 == wall.rect.bottom and self.collisionRectTop.colliderect(wall.rect):
                        check = True
        if check:
            self.velocity.x = 0
            self.velocity.y = 0

    def getTotalPoints(self):
        return self.totalPoints
