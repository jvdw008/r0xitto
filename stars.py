# stars.py
# Star class for bg movement

import upygame as pygame
import urandom as random

class Star:
    def __init__(self, x, y, speed, colour):
        self.x = x
        self.y = y
        self.speed = speed
        self.colour = colour
        #print (str(x) + ":" + str(y) + ":" + str(speed) + ":" + str(colour))
        
    def update(self):
        self.y += self.speed
        
        if self.y > 88:
            self.y = 0
            # Change speed and x pos
            self.x = random.getrandbits(7)
            self.speed = random.getrandbits(2)
            if self.speed == 0:
                self.speed = 1
            
    def draw (self, shakeX):
        pygame.draw.pixel(self.x + shakeX, self.y, self.colour)