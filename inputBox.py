import pygame
from highScores import HighScores
import time

pygame.init()
# used for all the font written in input box
FONT_SIZE = 20
FONT = pygame.font.Font('8-BIT WONDER.TTF', FONT_SIZE)
FONT_COLOR = pygame.Color('white')
FONT_COLOR_ACTIVE = pygame.Color('blue')


class InputBox:
    def __init__(self, xCoord, yCoord, width, height, score, text=''):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.width = width
        self.height = height
        self.score = score
        self.text = text
        self.active = False
        self.color = FONT_COLOR
        self.rect = pygame.Rect(self.xCoord, self.yCoord, self.width, self.height)
        self.textSurface = FONT.render(text, True, FONT_COLOR)
        self.message = ''

        # initialize variables for cursor
        self.cursorColor = FONT_COLOR
        self.cursor = pygame.Rect((self.xCoord, self.yCoord), (3, self.height))

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

            self.cursorVisible = True

            # need to show the input box is active by changing colors
            if self.active:
                self.color = FONT_COLOR_ACTIVE
            else:
                self.color = FONT_COLOR

        # if the user presses a key on the keyboard, then get the input
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    newScore = HighScores()
                    # add the user's score to the database
                    newScore.addScoreToDB(self.score, self.text)
                    # determine if it is the top score
                    self.message = newScore.determineTopScore(self.score)
                    self.text = ''
                # if the user hits the backspace key, then remove the last character
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) != 0:
                        characterRemoved = self.text[-1]
                        self.text = self.text[:-1]
                        width, height = FONT.size(characterRemoved)
                        self.cursor.x -= width
                else:
                    self.text += event.unicode
                    width, height = FONT.size(event.unicode)
                    self.cursor.x += width
                self.textSurface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # draw the input box on the screen
        screen.blit(self.textSurface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, FONT_COLOR, self.cursor)

    def getText(self):
        return self.text

    def getMessage(self):
        return self.message
