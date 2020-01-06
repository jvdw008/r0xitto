# player.py
# Handle player control and management

import upygame as pygame
import graphics

class Player:
    def __init__(self, startX, startY, minX, maxX, minY, maxY):
        self.playerX = startX		# Start X
        self.playerY = startY		# Start Y
        self.minX = minX			# Left clamp
        self.maxX = maxX			# Right clamp
        self.minY = minY            # Top clamp
        self.maxY = maxY            # Btm clamp

    # Draw player
    def draw(self, screen, image, shakeX):
        screen.blit(image, self.playerX + shakeX, self.playerY)

    # Move player
    def movePlayer(self, x, y):
        self.playerX += x
        self.playerY += y

        if (self.playerX > self.maxX):
            self.playerX = self.maxX

        if (self.playerX < self.minX):
            self.playerX = self.minX
            
        if (self.playerY > self.maxY):
            self.playerY = self.maxY

        if (self.playerY < self.minY):
            self.playerY = self.minY
        
    def getPlayerPos(self):
        return (self.playerX, self.playerY)
