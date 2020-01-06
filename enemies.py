# enemies.py

import upygame as pygame
import urandom as random

class Enemy:
    def __init__(self):
        #self.resetYPos()
        self.x = 0
        self.y = -30
        self.dir = 0
        self.maxX = 120
        self.minX = -40
        self.maxY = 90
        self.bulletShot = False             # Used in conjunction with the timer to shoot more bullets
        self.bulletTimer = 0
        self.bulletTimerMax = 0
        
        self.shipId = random.getrandbits(2)
        if self.shipId > 2:
            self.shipId = 2
            
        # Set horizontal speed
        self.xSpeed = random.getrandbits(1)
        
        # Set vertical if shipId > 0
        if self.shipId > 0:
            self.ySpeed = random.getrandbits(1)
            
            # Now set x pos
            self.x = random.getrandbits(7)
            if self.x > 55:
                self.dir = -1
            else:
                self.dir = 1
        
            # Sert boundaries
            if self.x > self.maxX:
                self.x = self.maxX
                
            if self.x < self.minX:
                self.x = self.minX
                
            # Bullet timer
            self.bulletTimerMax = 10
            
        else:
            # Now set horizontal ship
            self.y = random.getrandbits(5)
            self.dir = random.getrandbits(1)
            if self.dir == 0:
                # Move left
                self.dir = -1
                self.x = self.maxX
                
            else:
                # Move right
                self.x = self.minX
                
            # Bullet timer
            self.bulletTimerMax = 15
                
        #print("x: " + str(self.x) + " y:" + str(self.y))

    # Update movement
    def update(self):
        if self.dir < 0:
            self.x -= self.xSpeed
        else:
            self.x += self.xSpeed
            
        if self.shipId > 0:
            self.y += self.ySpeed
            
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
        if self.shipId > 0:
            if self.y >= self.maxY:
                return True
            else:
                return False
        else:
            if self.x <= self.minX or self.x >= self.maxX:
                return True
            else:
                return False
       
    # Draw enemy 
    def draw(self, screen, shakeX, images):
        if self.dir > 0:
            screen.blit(images[self.shipId], self.x + shakeX, self.y, 0, False)
            
        else:
            screen.blit(images[self.shipId], self.x + shakeX, self.y, 0, True)
    
    def returnPos(self):
        return (self.x, self.y)
        
    # Return size for hitboxes
    def getSize(self):
        return self.shipId
        
   