import pygame

class Wall(pygame.sprite.Sprite):
    position = (0, 0)
    size = (4, 4)
    colliding = False

    def __init__(self, position, size, image):
        # initialize super class
        super(Wall, self).__init__()
        self.position = position
        self.size = size

        # resize image scale with bounding box
        self.index = 0
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.rect = pygame.Rect(position, size)

    def collision(self, other):
        if self.rect.colliderect(other.rect) and not self.colliding:
            other.velocity.x = 0
            other.velocity.y = 0
            self.colliding = True
        elif not self.rect.colliderect(other.rect):
            self.colliding = False

