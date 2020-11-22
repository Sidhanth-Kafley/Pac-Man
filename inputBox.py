import pygame
from highScores import HighScores

pygame.init()
# used for all the font written in input box
FONT_SIZE = 20
FONT = pygame.font.Font('8-BIT WONDER.TTF', FONT_SIZE)
FONT_COLOR = pygame.Color('white')
FONT_COLOR_ACTIVE = pygame.Color('blue')


class InputBox():
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

        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        self.cursorColor = (255, 255, 255)
        self.cursorVisible = True
        self.cursorMSCounter = 0
        self.cursorSwitchMS = 500
        self.cursorPosition = len(self.text)
        self.cursorSurface = pygame.Surface((int(FONT_SIZE / 20 + 1), FONT_SIZE))
        self.clock = pygame.time.Clock()

    def update(self):
        # determine if size of input box is too small
        widthOfBox = max(200, self.textSurface.get_width()+10)
        self.rect.w = widthOfBox

        # update the cursor
        self.cursorMSCounter += self.clock.get_time()
        if self.cursorMSCounter >= self.cursorSwitchMS:
            self.cursorMSCounter %= self.cursorSwitchMS
            self.cursorVisible = not self.cursorVisible

        if self.cursorVisible:
            cursorYPosition = FONT.size(self.text[:self.cursorPosition])
            if self.cursorPosition > 0:
                cursorYPosition -= self.cursorSurface.get_width()
            self.surface.blit(self.cursorSurface, (150, 150))
        self.clock.tick()

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
                    newScore.addScoreToDB(self.score, self.text)
                    self.message = newScore.determineTopScore(self.score)
                    self.text = ''
                # if the user hits the backspace key, then remove the last character
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.textSurface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # draw the input box on the screen
        screen.blit(self.textSurface, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, FONT_COLOR, self.rect, 2)

    def getText(self):
        return self.text

    def getMessage(self):
        return self.message