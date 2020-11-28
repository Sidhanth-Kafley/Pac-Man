import pygame


class Pill(pygame.sprite.Sprite):

    def __init__(self, power, image, position):
        super(Pill, self).__init__()
        if not power:
            self.size = (3, 3)
        else:
            self.size = (10, 10)
        self.powerPill = power
        self.position = position
        self.image = image
        self.rect = pygame.Rect(position, self.size)
        self.drag = False

    def __del__(self):
        return True

    def isPower(self):
        return self.powerPill
