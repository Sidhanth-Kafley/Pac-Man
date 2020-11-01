import pygame


class Pill(pygame.sprite.Sprite):

    def __init__(self, power, image, position):
        super(Pill, self).__init__()
        self.size = (3, 3)
        self.powerPill = power
        self.position = position
        self.image = image
        self.rect = pygame.Rect(position, self.size)

    def __del__(self):
        return True

    def isPower(self):
        return self.powerPill
