# instructions.py
# Creates and draws the game interface itself and game instructions

import upygame as pygame
import graphics

class Instructions:
    def __init__(self):
        self.infoX = 2		# Start left pos
        self.infoYStart = 0
        self.ySpacing = 7	# Spacing between lines of text
        self.lines = ["Avoid asteroids or shoot", "Ammo is limited to max 9.", "Shooting shuttle/enemies", "gives drops.", "Enemies take one hit.", "Bosses take two hits.", "Spaceman = bonus points", "Crystals = bonus points.", "Green drop = full health.", "Orange drop = +2 bullets.", "Blue drop = bomb."]

    # Information text
    def showInstructions(self, umachine, colours):
        self.infoY = self.infoYStart
        ctr = 0
        
        for line in range(len(self.lines)):
            if ctr % 2 == 0:
                colour = colours[0]
            else:
                colour = colours[1]
                
            umachine.draw_text(self.infoX, self.infoY, self.lines[line], colour)
            self.infoY += self.ySpacing
            ctr += 1

        umachine.draw_text(self.infoX, self.infoY, "        - A for menu -", colours[2])