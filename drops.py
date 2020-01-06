# drops.py
# Random drops made by enemies/shuttles

import upygame as pygame
import urandom as random

class Drop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        self.dropType = random.getrandbits(2)
        if self.dropType > 2:
            self.dropType = 1
            
        
    def update(self):
        self.y += self.speed
        
        # Has dropped left the screen
        if self.y > 88:
            return True
        else:
            return False
            
    def draw (self, screen, shakeX, images):
        screen.blit(images[self.dropType], self.x + shakeX, self.y)
        
    def returnPos(self):
        return (self.x, self.y)
        
    def getType(self):
        return self.dropType