import pygame
from highScores import HighScores

pygame.init()
# used for all the font written in input box
FONT = pygame.font.Font('8-BIT WONDER.TTF', 20)
FONT_COLOR = pygame.Color('white')


class InputBox():
    def __init__(self, xCoord, yCoord, width, height, score, text=''):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = width
        self.height = height
        self.score = score
        self.text = text
        self.active = False
        self.rect = pygame.Rect(self.xCoord, self.yCoord, self.width, self.height)
        self.textSurface = FONT.render(text, True, FONT_COLOR)

    def update(self):
        # determine if size of input box is too small
        widthOfBox = max(200, self.textSurface.get_width()+10)
        self.rect.w = widthOfBox

    def handleEvent(self, event):
        # the user has clicked on the input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        # if the user presses a key on the keyboard, then get the input
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    newScore = HighScores(self.score, self.text)
                    newScore.addScoreToDB()
                    self.text = ''
                # if the user hits the backspace key, then remove the last character
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.textSurface = FONT.render(self.text, True, FONT_COLOR)

    def draw(self, screen):
        # draw the input box on the screen
        screen.blit(self.textSurface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, FONT_COLOR, self.rect, 2)

    def getText(self):
        return self.text