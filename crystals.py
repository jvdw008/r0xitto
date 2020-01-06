# crystals.py

import upygame as pygame
import urandom as random

class Crystal:
    def __init__(self, x, y, xSpeed, ySpeed, id, size):
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.id = id
        self.size = size
        if self.x > 55:
            self.dir = -1
        else:
            self.dir = 1
        
    def update(self):
        # Move Y
        self.y += 1
        if self.ySpeed > 1:
            self.y += 1
            
        # Move X
        if self.xSpeed != 0:
            self.x += self.dir

    def draw (self, screen, images, shakeX):
        if self.x > -20 and self.x < 130:
            screen.blit(images[self.id], self.x + shakeX, self.y)
            
    def returnPos(self):
        return (self.x, self.y)
        
    def getId(self):
        return self.id
        
    # Return object size for hit detection
    def getSize(self):
        return self.size
        