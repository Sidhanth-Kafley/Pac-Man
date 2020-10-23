

class PacMan:
    # all values subject to change
    startingHealth = 3
    moveSpeed = 10
    powerUp = False
    leftMotion = False
    rightMotion = False
    upMotion = False
    downMotion = False

   # def __init__(self):


    def setMotionDirection(self, direction):
        if direction == "up": # equality likely to change once i figure out what is actually passed to this function
            self.rightMotion = False
            self.leftMotion = False
            self.upMotion = True
            self.downMotion = False
        elif direction == "down":
            self.rightMotion = False
            self.leftMotion = False
            self.upMotion = False
            self.downMotion = True
        elif direction == "left":
            self.rightMotion = False
            self.leftMotion = True
            self.upMotion = False
            self.downMotion = False
        elif direction == "right":
            self.rightMotion = True
            self.leftMotion = False
            self.upMotion = False
            self.downMotion = False

    def hit(self):
        self.startingHealth -= self.startingHealth

    def setPowerUp(self):
        self.powerUp = not self.powerUp
