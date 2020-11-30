import pygame


class Wall(pygame.sprite.Sprite):
    position = (0, 0)
    size = (4, 4)
    colliding = False
    drag = False

    def __init__(self, position, size, image, imagePath):
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
        self.collideRect = None
        self.imagePath = imagePath

    def collision(self, other):
        if self.rect.colliderect(other.rect) and not self.colliding:
            other.velocity.x = 0
            other.velocity.y = 0
            self.colliding = True
        elif not self.rect.colliderect(other.rect):
            self.colliding = False

    def copy(self):
        copy = Wall(self.position, self.size, self.image, self.imagePath)
        return copy

    def calculateDistance(self):
        mouse = pygame.mouse.get_pos()
        x1 = mouse[0]
        y1 = mouse[1]
        x2 = self.rect.centerx
        y2 = self.rect.centery
        self.distancex = x1 - x2
        self.distancey = y1 - y2

    def setCollideRect(self):
        self.collideRect = pygame.Rect(self.rect.center, (self.size[0] * 3, self.size[1] * 3))

    def __del__(self):
        return True
