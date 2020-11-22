import pygame
import math


class Wall(pygame.sprite.Sprite):
    position = (0, 0)
    size = (4, 4)
    colliding = False
    drag = False

    def __init__(self, position, size, image):
        # initialize super class
        super(Wall, self).__init__()
        self.position = position
        self.size = size

        # resize image scale with bounding box
        self.index = 0
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = pygame.Rect(position, size)
        self.distancex = None
        self.distancey = None
        self.distance = None

    def collision(self, other):
        if self.rect.colliderect(other.rect) and not self.colliding:
            other.velocity.x = 0
            other.velocity.y = 0
            self.colliding = True
        elif not self.rect.colliderect(other.rect):
            self.colliding = False

    def copy(self):
        copy = Wall(self.position, self.size, self.image)
        return copy

    def calculateDistance(self):
        mouse = pygame.mouse.get_pos()
        x1 = mouse[0]
        y1 = mouse[1]
        x2 = self.rect.centerx
        y2 = self.rect.centery
        self.distancex = x1 - x2
        self.distancey = y1 - y2
