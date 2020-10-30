import pygame

class Wall(pygame.sprite.Sprite):
    position = (0, 0)
    size = (64, 64)

    def __init__(self, position, size, images):
        # initialize super class
        super(Wall, self).__init__()
        self.position = position
        self.size = size
        tempImages = []
        for image in images:
            tempImages.append(pygame.transform.scale(image, (16, 16)))
        images = tempImages
        self.images = images
        self.index = 0
        self.image = images[10]
        self.rect = pygame.Rect(position, size)

    def collision(self, other):
        print(other.rect.top)
