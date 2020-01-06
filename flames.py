# flames.py

import upygame as pygame
import urandom as random

class Flames:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.startY = y
        self.speed = speed
        self.colour = random.getrandbits(1)
        if self.colour == 0:
            self.colour = 1
        else:
            self.colour = 10
        
    def update(self, x, y):
        self.y += self.speed
        
        if abs(self.startY - self.y) > 15:
            self.y = y
            self.startY = y
            
            # Change speed and x pos
            self.x = x + random.getrandbits(3)
            self.speed = random.getrandbits(3)
            if self.speed < 3:
                self.speed = 3
                
            # Change colour
            self.colour = random.getrandbits(1)
            if self.colour == 0:
                self.colour = 1
            else:
                self.colour = 10
            
    def draw (self, shakeX):
        pygame.draw.pixel(self.x + shakeX + 4, self.y, self.colour)