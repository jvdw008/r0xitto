# rocks.py
# Display and randomize objects on screen

import upygame as pygame
import urandom as random

class Object:
    def __init__(self, x, y, xSpeed, ySpeed, id, size):
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.id = id
        self.size = size
        self.dir = 0
        
    def update(self, sizes):
        # Move Y
        self.y += 1
        if self.ySpeed > 1:
            self.y += 1
            
        # Move X
        if self.xSpeed != 0:
            self.x += self.dir
            
        if self.y > 100:
            tmpRnd = random.getrandbits(7)
            if tmpRnd > 125:
                self.resetYPos(sizes)
                self.y = -20
                
    def draw (self, screen, images, shakeX):
        if self.x > -20 and self.x < 130:
            screen.blit(images[self.id], self.x + shakeX, self.y)
            
    # Reset Y pos to top for a new game            
    def resetYPos(self, sizes):
        self.y = 90
        # Change speed and x pos
        self.x = random.getrandbits(7)
        self.ySpeed = random.getrandbits(2)
        self.xSpeed = random.getrandbits(1)
        self.id = random.getrandbits(3)
        
        # Only 5 rocks to choose from
        if self.id > 4:
            self.id = 0
            
        # Set size for this object
        self.size = sizes[self.id]
        
        # Make sure rocks always move down
        if self.ySpeed == 0:
            self.ySpeed = 1
        # Make sure rock moves horizontally
        if self.x > 55:
            self.dir = -1
        else:
            self.dir = 1
        
    def returnPos(self):
        return (self.x, self.y)
        
    def returnYSpd(self):
        return self.ySpeed
        
    # Return size for hitboxes
    def getSize(self):
        return self.size
        