# explosion.py

import urandom as random

class Explosion:
    def __init__(self, x, y, maxFrames):
        self.x = x
        self.y = y
        self.currentFrame = 0
        self.maxFrames = maxFrames
        self.movement = random.getrandbits(2)
        if self.movement > 1:
            self.movement = -1
        
    # Update frame
    def update(self):
        self.y += self.movement
        
        if self.currentFrame <= self.maxFrames:
            self.currentFrame += 1
            
    # Draw frame
    def draw (self, screen, img):
        screen.blit(img[self.currentFrame - 1], self.x, self.y)
        
    # Get frame state
    def getFrame(self):
        return self.currentFrame