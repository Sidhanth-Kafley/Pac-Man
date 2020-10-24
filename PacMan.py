import pygame

class PacMan(pygame.sprite.Sprite):
    # all values subject to change

    IMAGE_DOWN = pygame.image.load('Pac_Man_Down.png').convert_alpha()
    IMAGE_LEFT = pygame.image.load('Pac_Man_Left.png').convert_alpha()
    IMAGE_RIGHT = pygame.image.load('Pac_Man_Right.png').convert_alpha()
    IMAGE_UP = pygame.image.load('Pac_Man_Up.png').convert_alpha()
    IMAGE_CIRCLE = pygame.image.load('Pac_Man_Circle.png').convert_alpha()

    startingHealth = 3
    moveSpeed = 10
    powerUp = False
    leftMotion = False
    rightMotion = False
    upMotion = False
    downMotion = False
    location = [0, 0]

    def __init__(self):
        self.images = []
        self.images.append(self.IMAGE_CIRCLE)
        self.index = 0
        self.rect = pygame.Rect(5, 5, 64, 64)
        self.image = self.images[self.index]
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def setMotionDirection(self, direction):
        if direction == "up": # equality likely to change once i figure out what is actually passed to this function
            self.image = [self.IMAGE_CIRCLE, self.IMAGE_UP]
            self.rightMotion = False
            self.leftMotion = False
            self.upMotion = True
            self.downMotion = False
        elif direction == "down":
            self.image = [self.IMAGE_CIRCLE, self.IMAGE_DOWN]
            self.rightMotion = False
            self.leftMotion = False
            self.upMotion = False
            self.downMotion = True
        elif direction == "left":
            self.image = [self.IMAGE_CIRCLE, self.IMAGE_LEFT]
            self.rightMotion = False
            self.leftMotion = True
            self.upMotion = False
            self.downMotion = False
        elif direction == "right":
            self.image = [self.IMAGE_CIRCLE, self.IMAGE_RIGHT]
            self.rightMotion = True
            self.leftMotion = False
            self.upMotion = False
            self.downMotion = False

    def hit(self):
        self.startingHealth -= 1

    def setPowerUp(self):
        self.powerUp = not self.powerUp
