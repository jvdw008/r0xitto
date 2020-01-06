# Made by Blackjet in 2020
# Graphics done using Aseprite
# Sfx done using BFXR, Pocket Operators and Audacity
# Music made using Korg Volca Sample
# Code, music, sfx, graphics by Jaco van der Walt

# The source code in this file is released under the GNU GPL V3 license.
# Go to https://choosealicense.com/licenses/gpl-3.0/ for the full license details.

import upygame as pygame
import urandom as random
import umachine                             # For on-screen text
import graphics		                        # Graphics
import sounds                               # Sfx
from audio import Audio                     # Audio class to play sounds
from instructions import Instructions       # Game instructions
from background import Background           # Background (aquarium)
from player import Player                   # Player class
from animation import Animation as Anim     # Animation class
from explosion import Explosion             # Explodey bits
from bullets import Bullet                  # Bullet class
from drops import Drop                      # Dropped objects
from flashtext import Text                  # On-screen text for important messages in-game
from shake import Shake                     # Screen shake
from stars import Star                      # Stars for bg
from flames import Flames                   # Rocket flames
from rocks import Object                    # Rocks for bg/collisions etc
from crystals import Crystal                # Crystals
from enemies import Enemy                   # Enemies
from bosses import Boss                     # Bosses

# Game specific imports below

# Check RAM use
import gc
gc.collect()

# Setup the screen buffer
pygame.display.init(False)

# Set colours in RGB formatted tuples
pygame.display.set_palette_16bit([
    000000, 0xffff, 0xf660, 0xdd40, 0xfd1d, 0xe017, 0x87de, 0x2e57, 0x9786, 0x5d60, 0xff80, 0xe840, 0xa554, 0x73ae, 0xe5ad, 0x130b
    
]);

# default mode of 110x88 @16 cols
screen = pygame.display.set_mode()

# Init audio
g_sound = pygame.mixer.Sound()

# Test for real h/w to prevent simulator from hanging
gpioPin = umachine.Pin ( umachine.Pin.EXT2, umachine.Pin.ANALOG_IN )
gpioPinValue = gpioPin.value()
if(gpioPinValue == 0):
    isThisRealHardware = False
    gameSong = ""
else:
    isThisRealHardware = True
    gameSong = "music/rox.wav"

# Version number of current game build
version = 27

# States
STATE_MENU = 1
STATE_INSTRUCTIONS = 2
STATE_GAME = 3
STATE_PAUSE = 4
STATE_GAMEOVER = 5

# Variables
waitOnLoad = 50                         # Use this to prevent A starting the game before player knows when game just loaded
gameState = STATE_MENU                  # Menu or game
gameOver = False
gameOverPlayed = False                  # Trigger to pay gameover sound when dead
startGame = False                       # Boolean for starting the game
showInstructions = False                # For showing instructions on menu screen
level = 1                               # The level of the game
score = 0                               # Player score
scoreCtr = 0                            # Used to count the framerate and update score 
playerPos = [50, 60, 8, 12]             # Player position x/y, hitbox x/y
starList = []                           # Stars on screen
flameList = []                          # Flames from player ship rocket
rockList = []                           # Rocks on screen
rockSizes = [12, 13, 16, 17, 20]        # Doimensions of each rock to have accurate hitboxes
crystalList = []                        # Crystal objects for player to collect
crystalSizes = [11, 18, 14, 17, 18, 18] # Dimensions of each crystal to have accurate hitboxes
enemyShipSizes = [14, 12, 15]           # Dimensions of each enemy object
bossShipSizes = [24, 20, 22, 32]        # Dimensions of each boss object
explosionList = []                      # Explosions on screen
shuttle = [30, -30, False]              # Shuttle x, y and visibility
spaceman = [0, 0, False]                # Spaceman x/y/visibility
enemyList = []                          # Enemies
bossList = []                           # Bosses
bulletList = []                         # Bullet objects
dropList = []                           # Dropped objects
upPressed = False                       # Modifiers for dpad
downPressed = False                     # As above
leftPressed = False
rightPressed = False
aPressed = False                        # As above
bPressed = False                
cPressed = False
pauseGame = False                       # Pause mode
musicPlaying = False                    # Toggle for music
flashTextTimer = 60                     # On-screen text timer
highscore = 500                         # Default highscore
shakeX = 0
health = 10                             # Health of ship
bulletCount = 9
bombs = 0                               # Bombs for player emergencies
gameMode = 0                            # 0 for arcade, 1 for survival
# Counters
shuttleTimer = 200
enemyTimer = 400
bossTimer = 500

# Init classes
instructions = Instructions()
bg = Background(0, 0)
player = Player(playerPos[0], playerPos[1], 0, 94, 0, 71)
audio = Audio(g_sound, isThisRealHardware)
shake = Shake()

# Sprites, images, objects
bg = graphics.g_background.bg
logo = graphics.g_items.logo
scoreChars = [graphics.g_numbers.number0, graphics.g_numbers.number1, graphics.g_numbers.number2, graphics.g_numbers.number3, graphics.g_numbers.number4, graphics.g_numbers.number5, graphics.g_numbers.number6, graphics.g_numbers.number7, graphics.g_numbers.number8, graphics.g_numbers.number9]
rockImages = [graphics.g_rocks.rock01, graphics.g_rocks.rock02, graphics.g_rocks.rock03, graphics.g_rocks.rock04, graphics.g_rocks.rock05]
crystalImages = [graphics.g_items.crystal01, graphics.g_items.crystal02, graphics.g_items.crystal03, graphics.g_items.crystal04, graphics.g_items.crystal05, graphics.g_items.crystal06]
playerShip = graphics.g_ships.playerShip
shuttleShip = graphics.g_ships.ship04
enemyShipImages = [graphics.g_ships.ship01, graphics.g_ships.ship02, graphics.g_ships.ship03]
bossShipImages = [graphics.g_ships.boss01, graphics.g_ships.boss02, graphics.g_ships.boss03, graphics.g_ships.boss04]
explosionFrames = [graphics.g_explosion.explode01, graphics.g_explosion.explode02, graphics.g_explosion.explode03, graphics.g_explosion.explode04, graphics.g_explosion.explode05, graphics.g_explosion.explode06, graphics.g_explosion.explode07, graphics.g_explosion.explode08, graphics.g_explosion.explode09, graphics.g_explosion.explode10, graphics.g_explosion.explode11]
dropImages = [graphics.g_items.drop01, graphics.g_items.drop02, graphics.g_items.drop03, graphics.g_items.spaceman]
bulletImages = [graphics.g_bullets.bullet01, graphics.g_bullets.bullet02, graphics.g_bullets.bullet03, graphics.g_bullets.bullet04, graphics.g_bullets.bullet05]

# Create stars
for i in range(10):
    tmpX = random.getrandbits(7)
    tmpY = random.getrandbits(6)
    tmpSpd = random.getrandbits(2)
    if tmpSpd == 0:
        tmpSpd = 1
    tmpClr = random.getrandbits(4)
    if tmpClr == 0:
        tmpClr = 15
    starList.append(Star(tmpX, tmpY, tmpSpd, tmpClr))

# Create ship flames
for i in range(4):
    tmpX = playerPos[0] + random.getrandbits(3)
    tmpY = playerPos[0] + 20
    tmpSpd = random.getrandbits(3)
    if tmpSpd == 0:
        tmpSpd = 1
    if tmpClr == 0:
        tmpClr = 15
    flameList.append(Flames(tmpX, tmpY, tmpSpd))

# Create rocks
for i in range(6):
    tmpX = random.getrandbits(7)
    tmpY = random.getrandbits(6)
    spdX = random.getrandbits(1)
    spdY = random.getrandbits(2)
    if spdY == 0:
        spdY = 1
    rockId = random.getrandbits(3)
    # Only 5 rocks to choose from
    if rockId > 4:
        rockId = 0
    rockList.append(Object(tmpX, tmpY, spdX, spdY, rockId, rockSizes[rockId]))

# Create an initial crystal object
crystalList.append(Crystal(50, -20, 0, 1, 0, crystalSizes[0]))

#print ("free",gc.mem_free())
# Start music
audio.playMusic(gameSong)

# save/load highscore to EEPROM
def updateScore(action, val):
    if action == "save":
        data =  val.to_bytes(3,'big')
        for i in range(len(data)): myCookieData[i]=data[i]
        
        # Save myCookieData to EEPROM.
        myCookie.save()
        
    if action == "load":
        # Load myCookieData from EEPROM.
        myCookie.load()
        
        # Parse the scores and the names from myCookieData.
        pos = 0
        highscr, pos = getIntFromByteArray(myCookieData, 0, 3)
        return highscr
        
# Gets a fixed size string from a byte array 
def getStringFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return str(data, "utf-8"), pos+length

# Gets an integer from a byte array 
def getIntFromByteArray(dataBuf, pos, length):
    data = bytearray(length)
    for i in range(length): data[i]=dataBuf[i+pos]
    return int.from_bytes(data, 'big'), pos+length
    
# Score funciton
def drawScore(startX, Y, score):
    global scoreChars
    spacer = 8
    tScore = str(score)
    i = 0
    
    while i < len(tScore):
        if tScore[i] == "0":
            screen.blit(scoreChars[0], startX, Y)
        elif tScore[i] == "1":
            screen.blit(scoreChars[1], startX, Y)
        elif tScore[i] == "2":
            screen.blit(scoreChars[2], startX, Y)
        elif tScore[i] == "3":
            screen.blit(scoreChars[3], startX, Y)
        elif tScore[i] == "4":
            screen.blit(scoreChars[4], startX, Y)
        elif tScore[i] == "5":
            screen.blit(scoreChars[5], startX, Y)
        elif tScore[i] == "6":
            screen.blit(scoreChars[6], startX, Y)
        elif tScore[i] == "7":
            screen.blit(scoreChars[7], startX, Y)
        elif tScore[i] == "8":
            screen.blit(scoreChars[8], startX, Y)
        elif tScore[i] == "9":
            screen.blit(scoreChars[9], startX, Y)
        
        startX += spacer
        i += 1
    
# Bullet total
def drawCounter(x, y, counter):
    global scoreChars
    tCounter = str(counter)
    
    if tCounter == "0":
        screen.blit(scoreChars[0], x, y)
    elif tCounter == "1":
        screen.blit(scoreChars[1], x, y)
    elif tCounter == "2":
        screen.blit(scoreChars[2], x, y)
    elif tCounter == "3":
        screen.blit(scoreChars[3], x, y)
    elif tCounter == "4":
        screen.blit(scoreChars[4], x, y)
    elif tCounter == "5":
        screen.blit(scoreChars[5], x, y)
    elif tCounter == "6":
        screen.blit(scoreChars[6], x, y)
    elif tCounter == "7":
        screen.blit(scoreChars[7], x, y)
    elif tCounter == "8":
        screen.blit(scoreChars[8], x, y)
    elif tCounter == "9":
        screen.blit(scoreChars[9], x, y)

# Health bar
def drawHealth(x, y, health):
    step = 2
    blockWidth = 2
    green = 9
    yellow = 10
    red = 11
    colour = 9
    if health < 6:
        colour = yellow
    
    if health < 3:
        colour = red
    #pygame.draw.rect(pygame.Rect(x, y,health * 4, 10), True, colour)
    for h in range(health):
        pygame.draw.rect(pygame.Rect(x + blockWidth, y, 2, 10), True, colour)
        blockWidth += step * 2

# Detect hitboxes
# onject x/y is single pixel that must be inside the "zone" to be a hit
def detectHit(objX, objY, targetX, targetY, targetSize): #x1, y1, x2, y2, size
    if (objX > targetX and objX < targetX + targetSize):
        if (objY > targetY and objY < targetY + targetSize):
            return True
            
    return False

# Reset game to start
def reset():
    global upPressed, downPressed, leftPressed, rightPressed, aPressed, bPressed, cPressed, level, score, scoreCtr, playerPos, player
    global explosionList, rockSizes, enemyList, bulletList, dropList, bombs, bossList, bulletCount, pauseGame, shuttleTimer, enemyTimer, bossTimer
    
    upPressed = False               # Modifiers for dpad
    downPressed = False             # As above
    leftPressed = False
    rightPressed = False
    aPressed = False                # As above
    bPressed = False                # As above
    cPressed = False
    pauseGame = False
    level = 1                       # The level of the game
    score = 0                       # Player score
    scoreCtr = 0                    # Used to count the framerate and update score 
    bombs = 0
    bulletCount = 9
    playerPos = [50, 60, 8, 12]     # Player position x/y, hitbox x/y
    player = Player(playerPos[0], playerPos[1], 0, 94, 0, 71)
    shuttleTimer = 200
    enemyTimer = 400
    bossTimer = 500
    
    # Reset rocks
    for boulders in rockList:
        boulders.resetYPos(rockSizes)
        
    # Reset explosions
    explosionList = []
    
    # Reset enemies
    enemyList = []
    
    # Reset bosses
    bossList = []
    
    # Reset bullets
    bulletList = []
    
    # Reset drops
    dropList = []

    gc.collect()

######################################
# Update state
######################################
def update():
    global aPressed, gameMode, bPressed, cPressed, shuttleTimer, enemyTimer, bossTimer
    global gameState, scoreCtr, score, highscore, shakeX, bulletCount, health, rockSizes, crystalSizes, enemyShipSizes, bossShipSizes
    global upPressed, downPressed, leftPressed, rightPressed, explosionList, explosionFrames
    global shuttle, enemyList, bulletList, dropList, bombs, bossList, spaceman, pauseGame
    destroyScreen = False
    shipHitShuttle = False
    
    # Get screen shake amount (use on all x positions of objects!)
    ######################################
    shakeX = shake.update()
    
    if gameState != STATE_PAUSE:
        # Update stars
        ######################################
        for star in starList:
            star.update()
            
        # Update rocks
        ######################################
        for boulders in rockList:
            boulders.update(rockSizes)
    
    ######################################
    # Game state
    ######################################
    if gameState == STATE_GAME:

        # Update the score for player survival
        ######################################
        scoreCtr += 1
        if scoreCtr % 10 == 0:
            score += 1
        
        if cPressed:
            gameState = STATE_PAUSE
            cPressed = False
            
        # Bomb button
        ######################################
        if bPressed:
            bPressed = False
            if bombs > 0:
                bombs -= 1
                destroyScreen = True
        
        # Move player
        ######################################
        shipXMove = 0
        shipYMove = 0
        if upPressed:
            shipYMove = -2
        if downPressed:
            shipYMove = 2
        if leftPressed:
            shipXMove = -2
        if rightPressed:
            shipXMove = 2

        player.movePlayer(shipXMove, shipYMove)
        
        # Update player ship flames
        ######################################
        for flame in flameList:
            flame.update(player.getPlayerPos()[0], player.getPlayerPos()[1] + 20)
            
        # Update drops
        ######################################
        if len(dropList) > 0:
            tmpCtr = 0
            for dropItem in dropList:
                
                # Delete drop if out of screen
                if dropItem.update():
                    del dropList[tmpCtr]
                    break
            
                # Check if player is over drop
                if detectHit(player.getPlayerPos()[0] + 7, player.getPlayerPos()[1] + 7, dropItem.returnPos()[0] - 2, dropItem.returnPos()[1] - 2, 14):
                    # Health / green
                    if dropItem.getType() == 0:
                        audio.playSfx(sounds.health)
                        health = 10
                    
                    # Extra bullet / orange
                    elif dropItem.getType() == 1:
                        audio.playSfx(sounds.extraBullet)
                        if bulletCount == 8:
                            bulletCount += 1
                        elif bulletCount < 8:
                            bulletCount += 2
                        
                    # Explosion/bonus / blue
                    else:
                        audio.playSfx(sounds.bonus)
                        score += 100
                        if bombs < 10:
                            bombs += 1
                        
                    del dropList[tmpCtr]
                    break
                    
                tmpCtr += 1
                
            # Delete drop object
            ######################################
            if tmpCtr > 0:
                gc.collect()
        
        # Check crystal collisions
        ######################################
        if len(crystalList) > 0:
            crystalCtr = 0
            delCrystal = False
            for crystal in crystalList:
                crystal.update()
                # Has player hit crystal?
                if detectHit(player.getPlayerPos()[0] + 7, player.getPlayerPos()[1] + 7, crystal.returnPos()[0], crystal.returnPos()[1], crystal.getSize()):
                    del crystalList[crystalCtr]
                    delCrystal = True
                    score += 50
                    audio.playSfx(sounds.bonus)
                
                if crystal.returnPos()[1] >= 100:
                    del crystalList[crystalCtr]
                    delCrystal = True
                    
                # Destroy if player bombed
                if destroyScreen:
                    explosionList.append(Explosion(crystal.returnPos()[0], crystal.returnPos()[1], len(explosionFrames)))
                    del crystalList[crystalCtr]
                    delCrystal = True
                    
                crystalCtr += 1
                
            if delCrystal:
                gc.collect()
            
        # Check to see if new crystals need to be spawned
        ######################################
        if random.getrandbits(7) > 126:
            tmpX = random.getrandbits(7)
            spdX = random.getrandbits(1)
            spdY = random.getrandbits(2)
            if spdY == 0:
                spdY = 1
            crystalId = random.getrandbits(3)
            # Only 6 crystals to choose from
            if crystalId > 5:
                crystalId = 0
            crystalList.append(Crystal(tmpX, -20, spdX, spdY, crystalId, crystalSizes[crystalId]))
        
        # Check rock collisions
        ######################################
        for boulders in rockList:
            if detectHit(player.getPlayerPos()[0] + 7, player.getPlayerPos()[1] + 7, boulders.returnPos()[0], boulders.returnPos()[1], boulders.getSize()) and not shake.isShaking():
                shake.setShake()
                explosionList.append(Explosion(boulders.returnPos()[0], boulders.returnPos()[1], len(explosionFrames)))
                boulders.resetYPos(rockSizes)    # Reset as if it has exploded
                health -= 1
                audio.playSfx(sounds.explosion01)
                if health <= 0:
                    gameState = STATE_GAMEOVER
                    audio.playSfx(sounds.gameOver)
                    
            # Destroy if player bombed
            if destroyScreen:
                shake.setShake()
                explosionList.append(Explosion(boulders.returnPos()[0], boulders.returnPos()[1], len(explosionFrames)))
                boulders.resetYPos(rockSizes)

        # Update explosion
        ######################################
        if len(explosionList) > 0:
            tmpId = 0
            tmpCtr = 0
            for explody in explosionList:
                tmpId += 1
                if explody.getFrame() >= len(explosionFrames):
                    tmpCtr = tmpId
                    break
                
                explody.update()
        
            # Delete explosion object
            ######################################
            if tmpCtr > 0:
                del explosionList[tmpCtr - 1]
                gc.collect()
        
        # Create random shuttle
        ######################################
        if scoreCtr % shuttleTimer == 0:
            if random.getrandbits(1) == 1:
                shuttle[2] = True
        
        # Update shuttle
        ######################################
        if shuttle[2]:
            shuttle[1] += 1
            if destroyScreen:
                explosionList.append(Explosion(shuttle[0], shuttle[1], len(explosionFrames)))
                audio.playSfx(sounds.explosion01)
                # Spawn drop
                dropList.append(Drop(shuttle[0], shuttle[1]))
                
            # Check if player ship hit shuttle
            if detectHit(player.getPlayerPos()[0] + 7, player.getPlayerPos()[1] + 7, shuttle[0], shuttle[1], 10):
                explosionList.append(Explosion(shuttle[0], shuttle[1], len(explosionFrames)))
                audio.playSfx(sounds.explosion01)
                # Spawn drop
                dropList.append(Drop(shuttle[0], shuttle[1]))
                shipHitShuttle = True
                health -= 1
                if health <= 0:
                    gameState = STATE_GAMEOVER
                    audio.playSfx(sounds.gameOver)
            
            if shuttle[1] > 90 or destroyScreen or shipHitShuttle:
                shuttle[2] = False                  # Hide it
                shuttle[1] = -30                    # Set y pos to top
                shuttle[0] = random.getrandbits(7)  # Random x pos
            
        # Update spaceman
        ######################################
        if spaceman[2]:
            spcX = 0
            spcY = 0
            
            # Check if player caught him
            if detectHit(player.getPlayerPos()[0] + 7, player.getPlayerPos()[1] + 7, spaceman[0], spaceman[1], 12):
                score += 50
                audio.playSfx(sounds.dropItem)
                # Reset him
                spaceman = [0, 0, False]
            
            # Move him down
            if spaceman[0] > -12 and spaceman[0] < 122:
                if spaceman[1] > -12 and spaceman[1] < 100:
                    spcX = random.getrandbits(3)
                    spcY = random.getrandbits(3)
                    if spcX < 3:
                        spcX = -1
                    else:
                        spcX = 1
                    if spcY < 3:
                        spcY = -1
                    else:
                        spcY = 1

            spaceman[0] += spcX
            spaceman[1] += spcY
            
            # disappear him if needed
            if spaceman[0] < 0 or spaceman[0] > 110:
                if spaceman[1] < 0 or spaceman[1] > 88:
                    spaceman = [0, 0, False]
            
        # Then update enemies
        ######################################
        if len(enemyList) > 0:
            tmpId = 0
            tmpCtr = 0
            for en in enemyList:
                tmpId += 1
                
                # Check if enemy can shoot
                if en.update():
                    
                    # Horizontal enemy
                    if en.getSize() == 0:
                        if en.returnPos()[0] > 0:
                            bulletList.append(Bullet(en.returnPos()[0] + 4, en.returnPos()[1] + 15, 0, 2, 1))
                            audio.playSfx(sounds.enemyShot)
                    # All others
                    else:
                        if en.returnPos()[1] > 0:
                            bulletList.append(Bullet(en.returnPos()[0] + 4, en.returnPos()[1] + 15, -1, 2, 2))
                            bulletList.append(Bullet(en.returnPos()[0] + 4, en.returnPos()[1] + 15, 1, 2, 2))
                            audio.playSfx(sounds.enemyShot)
                    
                # Is enemy out of the screen yet?
                if en.outOfScreen():
                    tmpCtr = tmpId
                    break
                
                if destroyScreen:
                    explosionList.append(Explosion(en.returnPos()[0], en.returnPos()[1], len(explosionFrames)))
                    # Spawn drop
                    dropList.append(Drop(en.returnPos()[0], en.returnPos()[1]))
                    del enemyList[tmpCtr - 1]
                    
            # Delete enemy object
            ######################################
            if tmpCtr > 0:
                del enemyList[tmpCtr - 1]
                gc.collect()
            
        # Create random enemies
        ######################################
        if scoreCtr % enemyTimer == 0:
            
            if len(enemyList) > 3:
                enemyListTmp = enemyList[len(enemyList) - 1]
                enemyList = [enemyListTmp]
            else:
                enemyList.append(Enemy())
            
        # Create random bosses
        ######################################
        if len(bossList) > 0:
            tmpId = 0
            tmpCtr = 0
            for boss in bossList:
                tmpId += 1
                bossId = boss.getId()
                bossX = boss.returnPos()[0]
                bossY = boss.returnPos()[1]
                
                # Check if enemy can shoot
                if boss.update():
                    
                    # Horizontal enemy
                    if boss.getId() == 0 or boss.getId() == 2:
                        if boss.returnPos()[0] > 0:
                            bulletList.append(Bullet(bossX + (bossShipSizes[bossId] // 2), bossY + 17, 0, 2, bossId + 1))
                            audio.playSfx(sounds.enemyShot)
                    # All others
                    else:
                        if boss.returnPos()[1] > 0:
                            bulletList.append(Bullet(bossX + (bossShipSizes[bossId] // 2), bossY + 17, -1, 2, bossId + 1))
                            bulletList.append(Bullet(bossX + (bossShipSizes[bossId] // 2), bossY + 17, 1, 2, bossId + 1))
                            audio.playSfx(sounds.enemyShot)
                    
                # Is enemy out of the screen yet?
                if boss.outOfScreen():
                    tmpCtr = tmpId
                    break
                
                if destroyScreen:
                    explosionList.append(Explosion(boss.returnPos()[0], boss.returnPos()[1], len(explosionFrames)))
                    # Spawn drop
                    dropList.append(Drop(boss.returnPos()[0], boss.returnPos()[1]))
                    del bossList[tmpCtr - 1]
                    
            # Delete enemy object
            ######################################
            if tmpCtr > 0:
                del bossList[tmpCtr - 1]
                gc.collect()
        
        # Create random bosses
        ######################################
        if scoreCtr % bossTimer == 0:
            
            if len(bossList) > 1:
                bossListTmp = bossList[len(bossList) - 1]
                bossList = [bossListTmp]
            else:
                bossList.append(Boss())
        
        # Fire button
        ######################################
        if aPressed:
            aPressed = False
            if bulletCount > 0:
                bulletList.append(Bullet(player.getPlayerPos()[0] + 5, player.getPlayerPos()[1], 0, -3, 0))
                bulletCount -= 1
                audio.playSfx(sounds.playerShot)
            
        # Update bullet positions
        ######################################
        if len(bulletList) > 0:
            tmpId = 0
            tmpCtr = 0
            for bul in bulletList:
                tmpId += 1
                bullX = bul.returnPos()[0] + 3
                bullY = bul.returnPos()[1] + 2
                bullId = bul.getId()
                
                # Check bullet collisions
                ######################################
                # Check against shuttle
                if detectHit(bullX, bullY, shuttle[0], shuttle[1], 10) and bullId == 0:
                    explosionList.append(Explosion(shuttle[0], shuttle[1], len(explosionFrames)))
                    # Spawn drop
                    dropList.append(Drop(shuttle[0], shuttle[1]))
                    # Spawn spaceman
                    spaceman[0] = shuttle[0]
                    spaceman[1] = shuttle[1]
                    spaceman[2] = True
                    # Reset shuttle
                    shuttle[2] = False                  # Hide it
                    shuttle[1] = -20                    # Set y pos to top
                    shuttle[0] = random.getrandbits(7)  # Random x pos
                    tmpCtr = tmpId                      # Kill this bullet
                    audio.playSfx(sounds.explosion01)   # Explosion
                    break
                
                # Check against enemies
                ######################################
                tmpId2 = 0
                tmpCtr2 = 0
                for en in enemyList:
                    tmpId2 += 1
                    enX = en.returnPos()[0]
                    enY = en.returnPos()[1]
                    
                    if detectHit(bullX, bullY, enX, enY, enemyShipSizes[en.getSize()]) and bullId == 0:
                        explosionList.append(Explosion(enX, enY, len(explosionFrames)))
                        tmpCtr = tmpId                      # Kill this bullet
                        tmpCtr2 = tmpId2                    # Kill this enemy
                        audio.playSfx(sounds.explosion01)   # Explosion
                        # Spawn drop
                        dropList.append(Drop(enX, enY))
                        break
                
                # Delete enemy object
                ######################################
                if tmpCtr2 > 0:
                    del enemyList[tmpCtr2 - 1]
                
                # Check against bosses
                ######################################
                tmpId3 = 0
                tmpCtr3 = 0
                for boss in bossList:
                    tmpId3 += 1
                    bossId = boss.getId()
                    bossX = boss.returnPos()[0]
                    bossY = boss.returnPos()[1]
                
                    if detectHit(bullX, bullY, bossX, bossY, bossShipSizes[bossId]) and bullId == 0:
                        explosionList.append(Explosion(bossX + (bossShipSizes[bossId] // 2), bossY + 10, len(explosionFrames)))
                        tmpCtr = tmpId                      # Kill this bullet
                        # Check boss hitpoints
                        if boss.getHitPoints() > 0:
                            boss.addHitPoint(1)
                        else:
                            tmpCtr3 = tmpId3                    # Kill this boss
                            audio.playSfx(sounds.explosion01)   # Explosion
                            # Spawn drop
                            dropList.append(Drop(bossX + (bossShipSizes[bossId] // 2), bossY + 10))
                            break
                
                # Delete boss object
                ######################################
                if tmpCtr3 > 0:
                    del bossList[tmpCtr3 - 1]
                    
                # Check against rocks
                ######################################
                for boulders in rockList:
                    boulderX = boulders.returnPos()[0]
                    boulderY = boulders.returnPos()[1]
                    if detectHit(bullX, bullY, boulderX, boulderY, boulders.getSize()) and bullId == 0:
                        explosionList.append(Explosion(boulderX, boulderY, len(explosionFrames)))
                        tmpCtr = tmpId                      # Kill this bullet
                        boulders.resetYPos(rockSizes)       # Reset as if it has exploded
                        audio.playSfx(sounds.explosion01)   # Explosion
                        break
                
                # Check against player
                ######################################
                if detectHit(bullX, bullY, player.getPlayerPos()[0], player.getPlayerPos()[1], 16) and not shake.isShaking() and bullId != 0:
                    shake.setShake()
                    explosionList.append(Explosion(player.getPlayerPos()[0] + 7, player.getPlayerPos()[1] + 7, len(explosionFrames)))
                    audio.playSfx(sounds.explosion01)   # Explosion
                    health -= 1
                    if health <= 0:
                        gameState = STATE_GAMEOVER
                        audio.playSfx(sounds.gameOver)   # Explosion
                    
                
                # Check if bullet is out of screen bounds
                ######################################
                if bul.update():
                    tmpCtr = tmpId
                    break
                
            # Delete bullet object
            ######################################
            if tmpCtr > 0:
                del bulletList[tmpCtr - 1]
                gc.collect()

        # Slowly speed up object timers to make game harder over time
        ######################################
        if scoreCtr % 80 == 0:
            if enemyTimer > 100:
                enemyTimer -= 1
                
            if bossTimer > 200:
                bossTimer -=1
    
    ######################################
    # PAUSE
    ######################################
    if gameState == STATE_PAUSE:
        if cPressed:
            cPressed = False
            gameState = STATE_GAME
    
    ######################################
    # Game over state
    ######################################
    if gameState == STATE_GAMEOVER:
        # Save score if more than highscore
        if score > highscore:
            updateScore("save", score)
            highscore = score
            
        if cPressed:
            cPressed = False
            gameState = STATE_MENU

######################################
# Render graphics
######################################
def render():
    screen.blit(bg, 0 + shakeX, 0)
    
    # Always draw stars
    for star in starList:
        star.draw(shakeX)
    
    # Always draw rocks
    for boulders in rockList:
        boulders.draw(screen, rockImages, shakeX)
        
    ######################################
    # Menu state
    ######################################
    if gameState == STATE_MENU:
        
        # Logo
        screen.blit(logo, 3, 5)
        
        # Version
        modV = version % 10
        umachine.draw_text(3, 25, "v0." + str(version // 10) + "." + str(modV), 12)
        
        # Text
        umachine.draw_text(40, 30, "A: Arcade", 1)
        umachine.draw_text(40, 38, "B: Survival", 1)
        umachine.draw_text(40, 46, "C: Info", 1)
        
        # Info
        umachine.draw_text(40, 55, "In-game:", 8)
        umachine.draw_text(5, 63, "A: fire, B: bomb, C: pause", 8)
        
        # Scores
        umachine.draw_text(40, 72, "Highscore:", 10)
        drawScore(40, 82, highscore)
            
    ######################################
    # Game state
    ######################################
    elif gameState == STATE_GAME:
        # Draw crystals
        for crystal in crystalList:
            crystal.draw(screen, crystalImages, shakeX)
        
        # Display score
        umachine.draw_text(0, 1, "S:", 1)
        drawScore(10, 2, score)
        
        # Health
        if gameMode == 0:
            umachine.draw_text(0, 80, "H:", 1)
            drawHealth(10, 81, health)
        
        # Display bomb count
        umachine.draw_text(80, 80, "Bmb:", 1)
        drawCounter(100, 81, bombs)
        
        # Display bullet count
        umachine.draw_text(55, 80, "Bul:", 1)
        drawCounter(70, 81, bulletCount)
        
        # Drops
        for dropItem in dropList:
            dropItem.draw(screen, shakeX, dropImages)
        
        # Bullet
        for bul in bulletList:
            bul.draw(screen, shakeX, bulletImages)
        
        # Draw enemies
        for en in enemyList:
            en.draw(screen, shakeX, enemyShipImages)
        
        # Draw bosses
        for boss in bossList:
            boss.draw(screen, shakeX, bossShipImages)
        
        # Draw shuttle
        if (shuttle[2]):
            screen.blit(shuttleShip, shuttle[0] + shakeX, shuttle[1])
            
        # Draw spacemane
        if (spaceman[2]):
            screen.blit(dropImages[3], spaceman[0] + shakeX, spaceman[1])
        
        # Draw player ship flames
        for flame in flameList:
            flame.draw(shakeX)
            
        # Draw player
        player.draw(screen, playerShip, shakeX)
        
        # Draw explosion
        for explody in explosionList:
            explody.draw(screen, explosionFrames)
    
    ######################################
    # Game over state
    ######################################
    elif gameState == STATE_GAMEOVER:
        umachine.draw_text(40, 30, "Game over", 1)
        umachine.draw_text(12, 38, "Your final score was:", 10)
        drawScore(40, 48, score)
        umachine.draw_text(40, 60, "C: Menu", 1)
        

    elif gameState == STATE_INSTRUCTIONS:
        instructions.showInstructions(umachine, [4, 7, 2])
    
    elif gameState == STATE_PAUSE:
        umachine.draw_text(30, 30, "Game paused", 11)
        umachine.draw_text(20, 40, "A or C to resume", 1)
        
    
# Initialize the cookie.
myCookieDataSize = 10
myCookieData = bytearray(myCookieDataSize)
myCookie = umachine.Cookie("r0xitto", myCookieData)

# Temp test
#updateScore("save", 12345)

# Load the highscore if exists
tHighscore = updateScore("load", highscore)
if tHighscore > highscore:
    highscore = tHighscore

# Main loop
while True:
    if waitOnLoad > 0:
        waitOnLoad -= 1
    else:
        # Read keys
        eventtype = pygame.event.poll()
        if eventtype != pygame.NOEVENT:
    
    				# Keydown events
            if eventtype.type == pygame.KEYDOWN:
        		if (eventtype.key == pygame.K_UP):
        		    if gameState == STATE_GAME:
        		        upPressed = True
    
        		if (eventtype.key == pygame.K_RIGHT):
        		    if gameState == STATE_GAME:
        		        rightPressed = True
    
        		if (eventtype.key == pygame.K_DOWN):
        		    if gameState == STATE_GAME:
        		        downPressed = True
    
        		if (eventtype.key == pygame.K_LEFT):
        		    if gameState == STATE_GAME:
        		        leftPressed = True
    
        		if (eventtype.key == pygame.BUT_C):
        		    if not cPressed:
        		        cPressed = True
        		    
        		    if gameState == STATE_MENU:
                		gameState = STATE_INSTRUCTIONS
        		
        		if (eventtype.key == pygame.BUT_B):
        		    if gameState == STATE_GAME:
        		        bPressed = True
        		        
        		    if gameState == STATE_MENU:
        		        health = 1
        		        gameMode = 1
        		        gameState = STATE_GAME
        		        reset() # Reset game
    
        		if (eventtype.key == pygame.BUT_A):
        		    if gameState == STATE_PAUSE:
        		        gameState = STATE_GAME
        		        
        		    if gameState == STATE_GAME:
        		        aPressed = True
        		        
        		    if gameState == STATE_MENU:
        		        health = 10
        		        gameMode = 0
        		        gameState = STATE_GAME
        		        reset()
        		        
        		    if gameState == STATE_INSTRUCTIONS:
        		        gameState = STATE_MENU

            # Keyup events
            if eventtype.type == pygame.KEYUP:
        		if (eventtype.key == pygame.K_UP):
        		    if gameState == STATE_GAME:
        		        upPressed = False
    
        		if (eventtype.key == pygame.K_RIGHT):
        		    if gameState == STATE_GAME:
        		        rightPressed = False
    
        		if (eventtype.key == pygame.K_DOWN):
        		    if gameState == STATE_GAME:
        		        downPressed = False
    
        		if (eventtype.key == pygame.K_LEFT):
        		    if gameState == STATE_GAME:
        		        leftPressed = False

        		if (eventtype.key == pygame.BUT_C):
        		    cPressed = False

	# Update classes/objects
    update()
    
    # Clear screen
    screen.fill(0)
	
	# Render classes/objects
    render()

	# Sync screen
    pygame.display.flip()
