import pygame


class PacMan(pygame.sprite.Sprite):
    # all values subject to change
    startingHealth = 3
    powerUp = 1

    def __init__(self, position, images):
        # initialize super class
        super(PacMan, self).__init__()
        # size of each image
        size = (64, 64)
        # set directional images
        self.images = images
        self.imagesRight = [self.images[1], self.images[0]]
        self.imagesLeft = [self.images[1], self.images[2]]
        self.imagesUp = [self.images[1], self.images[4]]
        self.imagesDown = [self.images[1], self.images[3]]
        self.imagesStop = [self.images[1]]
        # index for looping through images
        self.index = 0
        # sets the object's position and size on the background
        self.rect = pygame.Rect(position, size)
        # set direction and speed of the pac man
        self.velocity = pygame.math.Vector2()
        # sets the current image (closed circle to start)
        self.image = self.images[1]

    def update(self):
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

    def hit(self):
        self.startingHealth -= 1

    def setPowerUp(self):
        if self.powerUp == 1:
            self.powerUp = 1.5
        else:
            self.powerUp = 1
