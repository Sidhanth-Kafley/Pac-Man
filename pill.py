import pygame


class Pill(pygame.sprite.Sprite):
    eaten = False

    def __init__(self, power, image, position):
        super(Pill, self).__init__()
        self.size = (5, 5)
        self.powerPill = power
        self.position = position
        self.image = image
        self.rect = pygame.Rect(position, self.size)

    def eat(self):
        eaten = True
        self.image = None

    def isPower(self):
        return self.powerPill
