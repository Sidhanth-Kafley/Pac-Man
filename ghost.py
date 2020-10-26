import pygame


class Ghost(pygame.sprite.Sprite):
    hitPacMan = False

    def __init__(self, color):
        # initialize super class
        super(Ghost, self).__init__()
        self.color = color

        # need to set the size of the images

    def update(self):
        pass

    # getters
    def getGhostColor(self):
        return self.color

    def determineGhostSpites(self):
        ghostColor = self.color
        # determine what images to open based on the color of the ghost
        GHOST_DOWN = pygame.image.load(ghostColor + 'Ghost_Down.png').convert_alpha()
        GHOST_LEFT = pygame.image.load(ghostColor + 'Ghost_Left.png').convert_alpha()
        GHOST_RIGHT = pygame.image.load(ghostColor + 'Ghost_Right.png').convert_alpha()
        GHOST_UP = pygame.image.load(ghostColor + 'Ghost_Up.png').convert_alpha()

    # ghost hits pac-man
    def touchesPacMan(self):
        # pac-man loses a life
        pass

    # pac-man is in power-up mode and can eat the ghosts
    def powerUpMode(self):
        pass

    # ghosts randomly moving in maze
    def ghostMovements(self, movement):
        # determine what direction the ghost is moving and choose the correct image
        if movement == 'xRight':
            pass
        elif movement == 'xLeft':
            pass
        elif movement == 'yUp':
            pass
        elif movement == 'yDown':
            pass

