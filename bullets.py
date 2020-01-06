# bullets.py

import upygame as pygame

class Bullet:
    def __init__(self, x, y, xSpeed, ySpeed, id):
        self.x = x
        self.y = y
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.id = id
        
        #print("x:" + str(x) + " y:" + str(y) + " id:" + str(id))
        
    def update(self):
        # Move Y
        self.y += self.ySpeed
            
        # Move X
        self.x += self.xSpeed
            
        # Check if out of bounds, return True if out
        if self.x < -10 or self.x > 120 or self.y < -10 or self.y > 98:
            return True
        else:
            return False

    def draw (self, screen, shakeX, images):
        if self.x > -20 and self.x < 130:
            screen.blit(images[self.id], self.x + shakeX, self.y)
            
    def returnPos(self):
        return (self.x, self.y)
        
    def getId(self):
        return self.id