# bosses.py

import upygame as pygame
import urandom as random

class Boss:
    def __init__(self):
        self.hitPoints = 1
        self.x = 0
        self.y = -30
        self.dir = 0
        self.maxX = 80
        self.minX = 0
        self.maxY = 30
        self.minY = -30
        self.bulletShot = False             # Used in conjunction with the timer to shoot more bullets
        self.bulletTimer = 0
        self.bulletTimerMax = 10
        self.onScreenTimer = 150             # How long enemy is on screen before disappearing
        self.shipId = random.getrandbits(2) # Ship type
            
        # Set horizontal speed
        self.xSpeed = random.getrandbits(1)
        self.ySpeed = 1
            
        # Now set x pos
        self.x = random.getrandbits(7)
        
        # Sert boundaries
        if self.x > self.maxX:
            self.x = self.maxX
            
        if self.x < self.minX:
            self.x = self.minX

    # Update movement
    def update(self):
        self.y += self.ySpeed
        
        if self.y > self.maxY:
            self.ySpeed = 0
            self.y = self.maxY
            self.dir = random.getrandbits(1)
            if self.dir == 0:
                self.dir = -1
            else:
                self.dir = 1
        
        if self.dir < 0:
            self.x -= self.xSpeed
        else:
            self.x += self.xSpeed
            
        if self.x < self.minX:
            self.dir = 1
            
        if self.x > self.maxX:
            self.dir = -1
            
        # Update onscreen timer
        self.onScreenTimer -= 1
        if self.onScreenTimer <= 0:
            self.ySpeed = -1
        
        # Update bullet timer
        if self.bulletTimer > 0:
            self.bulletTimer -=1
            self.bulletShot = False
        else:
            self.bulletTimer = self.bulletTimerMax
            self.bulletShot = True
            
        # Return if enemy can shoot or not
        return self.bulletShot
    
    # Check screen position
    def outOfScreen(self):
        if self.ySpeed == -1 and self.y < self.minY:
            return True
            
        return False
       
    # Draw enemy 
    def draw(self, screen, shakeX, images):
        if self.dir > 0:
            screen.blit(images[self.shipId], self.x + shakeX, self.y, 0, False)
            
        else:
            screen.blit(images[self.shipId], self.x + shakeX, self.y, 0, True)
    
    def returnPos(self):
        return (self.x, self.y)
        
    # Get id for shooting logic in main
    def getId(self):
        return self.shipId
        
    # take hit
    def addHitPoint(self, qty):
        self.hitPoints -= 1
        
    # Return hit total
    def getHitPoints(self):
        return self.hitPoints
       