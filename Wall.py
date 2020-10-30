import pygame

class Wall(pygame.sprite.Sprite):
    position = (0, 0)
    size = (16, 16)
    colliding = False

    def __init__(self, position, size, images):
        # initialize super class
        super(Wall, self).__init__()
        self.position = position
        self.size = size
        tempImages = []

        # resize image scale with bounding box
        for image in images:
            tempImages.append(pygame.transform.scale(image, (size[0], size[1])))
        images = tempImages
        self.images = images
        self.index = 0
        self.image = images[10]
        self.rect = pygame.Rect(position, size)

    def collision(self, other):
        #print(self.colliding)
        #print(type(self) == Wall)
        if self.rect.colliderect(other.rect) and not self.colliding:
            other.velocity.x = 0
            other.velocity.y = 0
            self.colliding = True
        elif not self.rect.colliderect(other.rect):
            self.colliding = False

