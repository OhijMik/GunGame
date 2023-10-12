import pygame
import random

pygame.init()
# The font
font = pygame.font.SysFont("Roboto", 26)
title = pygame.font.SysFont("Roboto", 100)

# The main function
def main():
    '''
    This function is the main setup/loop of the program.
    
    This function includes all the variables, the setups, and a loop that continuously runs.
  
    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = [1300, 1000]   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower
    frameRate = 60               #Slowing down the program
    frameCount = 0               #Count the number of frames that have occurred
    
    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize[0], surfaceSize[1]))
    
    # Lives
    lives = [3,3]
    
    # Scale and the colour of the sprites
    scale = 3
    colour = "Blue"
    colour1 = "Black"
    
    # Position of the player
    playerPos = [[50,608], [1100,608]]
    
    #Image animation
    playerRect = [[0*scale,0*scale,48*scale,39*scale], [0*scale,0*scale,48*scale,39*scale]]
    characterRect = [pygame.Rect((playerPos[0][0]+35,playerPos[0][1]+20,48*scale-80,39*scale-20)), \
                        pygame.Rect((playerPos[1][0]+35,playerPos[1][1]+20,48*scale-80,39*scale-20))]
    playerPatchNumber = [0, 0]
    playerSpeed = [4, 4]
    gravities = [10, 10]
    playerFrameRate = 5
    
    # Bullet position
    bulletPos = [[playerPos[0][0]+80, playerPos[0][1]+63], [playerPos[1][0]+80, playerPos[1][1]+63], [playerPos[0][0]+80, playerPos[0][1]+63], \
                 [playerPos[1][0]+80, playerPos[1][1]+63], [playerPos[0][0]+80, playerPos[0][1]+63], [playerPos[1][0]+80, playerPos[1][1]+63]]
    gun = ['Pistol', 'Pistol']
    
    # Player booleans
    playerMove = [False, False]
    playerJump = [False, False]
    playerShoot = [False, False]
    playerDirection = ['Right', 'Left']
    bulletDirection = ['Right', 'Left']
    
    # Time
    moveTime = 0
    reloadTime = [0, 0]
    mapTime = 0
    mouseTime = 0
    jumpTime = [0, 0]
    
    # ProgramState
    programState = 'start'
    lastPlayed = ''
    
    # Map variable
    maps = 1
    mapSelection = 1

    # Map 1
    map1 = [(100, 525, 200, 30), (1000, 525, 200, 30), (350, 325, 600, 50)]
    map1Image = pygame.transform.smoothscale(pygame.image.load("images/Map 1 background.jpg"), (surfaceSize[0], surfaceSize[1]))
    map1SelectionImage = pygame.transform.smoothscale(pygame.image.load("images/Map 1 background.jpg"), (400,200))
    map1Platform = pygame.transform.scale(pygame.image.load("images/Map 1 platform.png"), (200, 30))
    map1MainPlatform = pygame.transform.scale(pygame.image.load("images/Map 1 platform.png"), (600, 50))

    # Map 2
    map2 = [(150, 525, 300, 10), (850, 525, 300, 10)]
    map2Image = pygame.transform.smoothscale(pygame.image.load("images/Map 2 background.png"), (surfaceSize[0], surfaceSize[1]))
    map2SelectionImage = pygame.transform.smoothscale(pygame.image.load("images/Map 2 background.png"), (400,200))
    map2Platform = pygame.transform.scale(pygame.image.load("images/Map 2 platform.png"), (300, 60))

    # Map 3
    map3 = [(45, 515, 190, 30), (1055, 515, 200, 30), (380, 315, 510, 50), (290, 740, 690, 200), (50, 575, 150, 100), (1080, 575, 150, 100)]
    map3Image = pygame.transform.smoothscale(pygame.image.load("images/Map 3 background.jpg"), (surfaceSize[0], surfaceSize[1]))
    map3SelectionImage = pygame.transform.smoothscale(pygame.image.load("images/Map 3 background.jpg"), (400,200))
    
    # File reading/writing
    readFile = open("Highscore.txt", "r")
    bestTime = [0, 0, 0]
    
    for i in range(3):
        theLine = readFile.readline()   # Try to read next line
        bestTime[i] = float(theLine)
        if len(theLine) == 0:              # If there are no more lines
            break                          
    
    # Function to reset the map
    def mapReset():
        '''
        This function sets the variables of the 2 players.

        This function sets the boolean, direction, and the position of the bullet whenever the game is restarted.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        bulletPos[0] = [playerPos[0][0]+80, playerPos[0][1]+63]
        bulletPos[1] = [playerPos[1][0]+80, playerPos[1][1]+63]
        playerMove[0] = False
        playerMove[1] = False
        playerJump[0] = False
        playerJump[1] = False
        playerShoot[0] = False
        playerShoot[1] = False
        playerDirection[0] = 'Right'
        playerDirection[1] = 'Left'
        bulletDirection[0] = 'Right'
        bulletDirection[1] = 'Left'

    # Function for the animation
    def animation(rect, frameCount, frameRate, patch, numPatches):
        '''
        This function sets the variables of the 2 players.

        This function sets the boolean, direction, and the position of the bullet whenever the game is restarted.

        Parameters
        ----------
        parameter1 : list
        The x, y position, width, and height of the character sprite rectangle
        parameter2 : int
        The frame count
        parameter3 : int
        The frame rate of the animation
        parameter4 : int
        The current patch number it is in
        parameter5 : int
        How many patchs there are

        Returns
        -------
        int
        The current patch number it is in
        '''
        if (frameCount % frameRate == 0):    
            if (patch < numPatches-1) :
                patch += 1
                rect[0] += rect[2]  
            else:
                patch = 0           
                rect[0] = 0
        return patch
        
    
    # Collision detection function
    def collision(character, platform, pos, gravity, jump, direction, speed):
        '''
        This function checks if the player is colliding with the platforms.

        This function checks the position of the player and the position of the platform to see if it is colliding.

        Parameters
        ----------
        parameter1 : list
        The x, y position, width, and height of the character sprite rectangle
        parameter2 : list
        The rectangle position of the platform
        parameter3 : int
        The x, y position of the player
        parameter4 : int
        The gravity affecting the players
        parameter5 : boolean
        The player is jumping or not jumping
        parameter6 : string
        What direction the player is looking
        parameter7 : int
        The speed of the players

        Returns
        -------
        None
        '''
        global characterPosition
        global characterGravity
        global characterJump
        global characterDirection
        global characterSpeed
        
        # Collision with the small platforms
        # Bottom collision with the platforms
        if character.colliderect(pygame.Rect((platform[0]+10, platform[1]+15, platform[2]-20, 15))):        
            jump = False
            jumpTime[0] = -0.2
            jumpTime[1] = -0.2
        # Top collision with the platforms
        elif character.colliderect(pygame.Rect((platform[0]+10, platform[1], platform[2]-20, 15))):        
            jump = False
            pos[1] = platform[1]-117
            gravity = 0
        # Collision with the side of the platforms
        elif character.colliderect(pygame.Rect(((platform[0]+platform[2]-10), platform[1], 10, platform[3]))):        
            speed = 0
            if character[0] <= (platform[0] + platform[2]) and character[0] >= (platform[0] + platform[2] - 50) and direction == 'Right':
                speed = 4
        
        elif character.colliderect(pygame.Rect((platform[0], platform[1], 10, platform[3]))):        
            speed = 0
            if character[0] >= (platform[0]-100) and character[0] <= (platform[0]-50) and direction == 'Left':
                speed = 4
        
        else:
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a] or \
                pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
                speed = 4
        
        characterPosition = pos
        characterGravity = gravity
        characterJump = jump
        characterDirection = direction
        characterSpeed = speed
    
    # Function for the players
    def player(pos, rect, patchNum, speed, gravity, frameRate, move, jump, shoot, bullet, bulletDirection, direction, sprite):
        '''
        This function has all of the character animation

        This function does the animations for when the player is idle, moving, and jumping.

        Parameters
        ----------
        parameter1 : list
        The x, y position of the player
        parameter2 : list
        The x, y position, width, and height of the character sprite rectangle
        parameter3 : int
        The current patch number it is in
        parameter4 : int
        The speed of the players
        parameter5 : int
        The gravity affecting the players
        parameter6 : int
        The frame rate of the animation
        parameter7 : boolean
        The player is moving or not moving
        parameter8 : boolean
        The player is jumping or not jumping
        parameter9 : boolean
        The player is shooting or not shooting
        parameter10 : list
        The x and y position of the bullet
        parameter11 : string
        The bullet is towards the right or the left
        parameter12 : string
        The direction of the player
        parameter13 : int
        The sprite of the player to change the colour

        Returns
        -------
        None
        '''
        global patchNumbers
        global bulletState 
        global acceleration

        # If the player is moving
        if move == True and jump == False:
            if direction =='Right':
                pos[0] += speed    
                mainSurface.blit(spriteSheetMove[sprite], pos, rect)
                patchNumbers = animation(rect, frameCount, frameRate, patchNum, 6)
              
            elif direction == 'Left':
                pos[0] -= speed     
                tempSurface = pygame.Surface( (rect[2], rect[3]) ) 
                tempSurface.fill((0,0,0))
                tempSurface.set_colorkey((0,0,0))                                      
                tempSurface.blit(spriteSheetMove[sprite], (0,0), rect)                      

                tempSurface = pygame.transform.flip(tempSurface,True,False)
                mainSurface.blit(tempSurface, pos)  
                patchNumbers = animation(rect, frameCount, frameRate, patchNum, 6)
                    
        # If the player isn't moving
        elif move == False and jump == False:
            if direction =='Right': #player goes right
                mainSurface.blit(spriteSheetIdle[sprite], pos, rect)
                patchNumbers = animation(rect, frameCount, frameRate, patchNum, 5)

            elif direction == 'Left':
                tempSurface = pygame.Surface( (rect[2], rect[3]) ) #Make a temp Surface using the width and height of the rect
                tempSurface.fill((0,0,0))
                tempSurface.set_colorkey((0,0,0))                                      #Set the color black to be transparent
                tempSurface.blit(spriteSheetIdle[sprite], (0,0),  rect)                      #Copy the player image to the temp surface

                tempSurface = pygame.transform.flip(tempSurface,True,False)
                mainSurface.blit(tempSurface, pos)
                patchNumbers = animation(rect, frameCount, frameRate, patchNum, 5)
        
        # If the player is jumping
        elif jump == True:
            if direction =='Right':
                mainSurface.blit(spriteSheetJump[sprite], pos, [0, 0, 144, 117])
                pos[1] -= 11

                if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                    pos[0] += speed
                        
            elif direction == 'Left':
                tempSurface = pygame.Surface((144, 117)) #Make a temp Surface using the width and height of the rect
                tempSurface.fill((0,0,0))
                tempSurface.set_colorkey((0,0,0))                                      #Set the color black to be transparent
                tempSurface.blit(spriteSheetJump[sprite], (0,0),  [0, 0, 144, 117])                      #Copy the player image to the temp surface

                tempSurface = pygame.transform.flip(tempSurface,True,False)
                mainSurface.blit(tempSurface, pos)
                pos[1] -= 11
                
                if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                    pos[0] -= speed
        
        else:
            mainSurface.blit(spriteSheetJump[sprite], pos, rect)
            
        # Gravity
        pos[1] += gravity
        gravity += 0.25
        acceleration = gravity

        bulletState = shoot
    
    # The main loop
    spriteSheetMove = pygame.image.load(f"Images/TeamGunner_By_SecretHideout_060519/CHARACTER_SPRITES/{colour}/Gunner_{colour}_Run.png")
    spriteSheetMove1 = pygame.image.load(f"Images/TeamGunner_By_SecretHideout_060519/CHARACTER_SPRITES/{colour1}/Gunner_{colour1}_Run.png")
    spriteSheetMove = [pygame.transform.smoothscale(spriteSheetMove, (scale*spriteSheetMove.get_width(),scale*spriteSheetMove.get_height())), \
                           pygame.transform.smoothscale(spriteSheetMove1, (scale*spriteSheetMove1.get_width(),scale*spriteSheetMove1.get_height()))]

    while True:
        ev = pygame.event.poll()   
        if ev.type == pygame.QUIT:  
            break
        # When ESC is pressed, go back to main menu
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            programState = 'start'
            playerShoot[0] = False
            playerShoot[1] = False
            
        # When the key is pressed
        if ev.type == pygame.KEYDOWN and mapTime >= 3:          
            if ev.key == pygame.K_a:
                playerDirection[0] = 'Left'
                playerMove[0] = True

            elif ev.key == pygame.K_d:
                playerDirection[0] = 'Right'
                playerMove[0] = True
                
            if ev.key == pygame.K_w and jumpTime[0] >= 0.1:
                playerJump[0] = True
                playerRect[0][0] = 0*scale
            
            # If it is custom game
            if programState == 'customGame':
                if ev.key == pygame.K_LEFT:
                    playerDirection[1] = 'Left'
                    playerMove[1] = True
                elif ev.key == pygame.K_RIGHT:
                    playerDirection[1] = 'Right'
                    playerMove[1] = True
                if ev.key == pygame.K_UP and jumpTime[1] >= 0.1:
                    playerJump[1] = True
                    playerRect[1][0] = 0*scale
            # Player 1 shooting
            if ev.key == pygame.K_SPACE and playerShoot[0] == False:
                if gun[0] == 'Pistol' and reloadTime[0] >= 0.2:
                    playerShoot[0] = True
                    bulletPos[0][1] = playerPos[0][1] + 63
                    bulletPos[0][0] = playerPos[0][0] + 80
                    if playerDirection[0] == 'Right':
                        bulletDirection[0] = 'Right'
                    else:
                        bulletDirection[0] = 'Left'
                    reloadTime[0] = 0
                elif gun[0] == 'Sniper' and reloadTime[0] >= 4:
                    playerShoot[0] = True
                    bulletPos[0][1] = playerPos[0][1] + 63
                    bulletPos[0][0] = playerPos[0][0] + 80
                    if playerDirection[0] == 'Right':
                        bulletDirection[0] = 'Right'
                    else:
                        bulletDirection[0] = 'Left'
                    reloadTime[0] = 0
                elif gun[0] == 'Shotgun' and reloadTime[0] >= 2:
                    playerShoot[0] = True
                    bulletPos[0][1] = playerPos[0][1] + 63
                    bulletPos[0][0] = playerPos[0][0] + 80
                    bulletPos[2][1] = playerPos[0][1] + 63
                    bulletPos[2][0] = playerPos[0][0] + 80
                    bulletPos[4][1] = playerPos[0][1] + 63
                    bulletPos[4][0] = playerPos[0][0] + 80
                    
                    if playerDirection[0] == 'Right':
                        bulletDirection[0] = 'Right'
                    else:
                        bulletDirection[0] = 'Left'
                    reloadTime[0] = 0
                    
        # When you let go of the keys
        elif ev.type == pygame.KEYUP and mapTime >= 3:
            if ev.key == pygame.K_a or ev.key == pygame.K_d:
                playerMove[0] = False
                playerPatchNumber = [0, 0]
                playerRect = [[0*scale,0*scale,48*scale,39*scale], [0*scale,0*scale,48*scale,39*scale]]
            # In a custom game 
            elif programState == 'customGame':
                if ev.key == pygame.K_LEFT or ev.key == pygame.K_RIGHT:
                    playerMove[1] = False
                    playerPatchNumber = [0, 0]
                    playerRect = [[0*scale,0*scale,48*scale,39*scale], [0*scale,0*scale,48*scale,39*scale]]
        
        # Player 2 shooting
        elif ev.type == pygame.MOUSEBUTTONDOWN and programState == 'customGame':
            if ev.button == 1 and playerShoot[1] == False and mapTime >= 3:
                if gun[1] == 'Pistol' and reloadTime[1] >= 0.2:
                    playerShoot[1] = True
                    bulletPos[1][1] = playerPos[1][1] + 63
                    bulletPos[1][0] = playerPos[1][0] + 80
                    if playerDirection[1] == 'Right':
                        bulletDirection[1] = 'Right'
                    else:
                        bulletDirection[1] = 'Left'
                    reloadTime[1] = 0
                elif gun[1] == 'Sniper' and reloadTime[1] >= 4:
                    playerShoot[1] = True
                    bulletPos[1][1] = playerPos[1][1] + 63
                    bulletPos[1][0] = playerPos[1][0] + 80
                    if playerDirection[1] == 'Right':
                        bulletDirection[1] = 'Right'
                    else:
                        bulletDirection[1] = 'Left'
                    reloadTime[1] = 0
                elif gun[1] == 'Shotgun' and reloadTime[1] >= 2:
                    playerShoot[1] = True
                    bulletPos[1][1] = playerPos[1][1] + 63
                    bulletPos[1][0] = playerPos[1][0] + 80
                    bulletPos[3][1] = playerPos[1][1] + 63
                    bulletPos[3][0] = playerPos[1][0] + 80
                    bulletPos[5][1] = playerPos[1][1] + 63
                    bulletPos[5][0] = playerPos[1][0] + 80
                    if playerDirection[1] == 'Right':
                        bulletDirection[1] = 'Right'
                    else:
                        bulletDirection[1] = 'Left'
                    reloadTime[1] = 0
                
        
        # Getting the position of the mouse
        mousePos = pygame.mouse.get_pos()
        
        # The sprites

        spriteSheetIdle = pygame.image.load(f"Images/TeamGunner_By_SecretHideout_060519/CHARACTER_SPRITES/{colour}/Gunner_{colour}_Idle.png")
        spriteSheetIdle1 = pygame.image.load(f"Images/TeamGunner_By_SecretHideout_060519/CHARACTER_SPRITES/{colour1}/Gunner_{colour1}_Idle.png")
        spriteSheetIdle = [pygame.transform.smoothscale(spriteSheetIdle, (scale*spriteSheetIdle.get_width(),scale*spriteSheetIdle.get_height())), \
                           pygame.transform.smoothscale(spriteSheetIdle1, (scale*spriteSheetIdle1.get_width(),scale*spriteSheetIdle1.get_height()))]
        
        spriteSheetJump = pygame.image.load(f"Images/TeamGunner_By_SecretHideout_060519/CHARACTER_SPRITES/{colour}/Gunner_{colour}_Jump.png")
        spriteSheetJump1 = pygame.image.load(f"Images/TeamGunner_By_SecretHideout_060519/CHARACTER_SPRITES/{colour1}/Gunner_{colour1}_Jump.png")
        spriteSheetJump = [pygame.transform.smoothscale(spriteSheetJump, (scale*spriteSheetJump.get_width(),scale*spriteSheetJump.get_height())), \
                          pygame.transform.smoothscale(spriteSheetJump1, (scale*spriteSheetJump1.get_width(),scale*spriteSheetJump1.get_height()))]
        
        # Time
        if frameCount >= 6:
            if programState == 'level 1' or programState == 'level 2' or programState == 'level 3' or programState == 'customGame':
                mapTime += 0.1
            moveTime += 0.1
            reloadTime[0] += 0.1
            reloadTime[1] += 0.1
            jumpTime[0] += 0.1
            jumpTime[1] += 0.1
            mouseTime += 0.1
            frameCount = 0
        
        # Jump time delay
        if playerJump[0] == True:
            jumpTime[0] = 0
        if playerJump[1] == True:
            jumpTime[1] = 0
            

        # Program is at start screen
        if programState == 'start':
            # Filling the screen
            mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Background.webp"), (surfaceSize[0], surfaceSize[1])), (0, 0))
            
            # Words on the screen
            renderedText = title.render("Gun Game", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (480,200))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Levels", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (580,430))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Custom", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (570,550))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Help", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (600,670))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Quit", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (600,790))
            
            # Button rectangle
            for i in range(400, 880, 120):
                pygame.draw.rect(mainSurface, [255, 255, 255], [450,i,400,100], 2)
                
            # If the mouse is touching the button
            if mousePos[0] >= 450 and mousePos[0] <= 850:
                if mousePos[1] >= 400 and mousePos[1] <= 500:
                    pygame.draw.rect(mainSurface, (255, 170, 0), [450,400,400,100], 2)
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        programState = 'levels'
                        mouseTime = 0
                elif mousePos[1] >= 520 and mousePos[1] <= 620:
                    pygame.draw.rect(mainSurface, (255, 170, 0), [450,520,400,100], 2)
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        programState = 'custom'
                        lastPlayed = 'custom'
                elif mousePos[1] >= 640 and mousePos[1] <= 740:
                    pygame.draw.rect(mainSurface, (255, 170, 0), [450,640,400,100], 2)
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        programState = 'help'
                elif mousePos[1] >= 760 and mousePos[1] <= 860:
                    pygame.draw.rect(mainSurface, (255, 170, 0), [450,760,400,100], 2)
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        break

        elif programState == 'help':
            # Filling the screen
            mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Background.webp"), (surfaceSize[0], surfaceSize[1])), (0, 0))

            # Words on the screen
            renderedText = title.render("Help", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (560,200))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Player 1 controls: ", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (140,300))
            renderedText = pygame.font.SysFont("Roboto", 60).render("W = Jump", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (160,450))
            renderedText = pygame.font.SysFont("Roboto", 60).render("A = Move left", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (160,500))
            renderedText = pygame.font.SysFont("Roboto", 60).render("D = Move Right", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (160,550))
            renderedText = pygame.font.SysFont("Roboto", 60).render("SPACE = Shoot", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (160,600))

            renderedText = pygame.font.SysFont("Roboto", 60).render("Player 2 controls: ", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (750,300))
            renderedText = pygame.font.SysFont("Roboto", 60).render("UP key = Jump", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (770,450))
            renderedText = pygame.font.SysFont("Roboto", 60).render("LEFT key = Move left", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (770,500))
            renderedText = pygame.font.SysFont("Roboto", 60).render("RIGHT key = Move Right", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (770,550))
            renderedText = pygame.font.SysFont("Roboto", 60).render("LEFT mouse = Shoot", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (770,600))

            renderedText = pygame.font.SysFont("Roboto", 60).render("ESC = Exit to main menu", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (400,700))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Each level has a harder A.I to fight against", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (220,750))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Or you can play with your friend with your keyboard", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (130,800))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Back", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (50,900))
            
            pygame.draw.rect(mainSurface, [255, 255, 255], [20,890,150,60], 2)
                
            # If the mouse is touching the button
            if mousePos[0] >= 20 and mousePos[0] <= 170 and mousePos[1] >= 890 and mousePos[1] <= 950:
                pygame.draw.rect(mainSurface, (255, 170, 0), [20,890,150,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    programState = 'start'
        
        elif programState == 'custom':
            # Filling the screen
            mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Background.webp"), (surfaceSize[0], surfaceSize[1])), (0, 0))
            
            # Words on the screen
            renderedText = title.render("Custom", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (510,150))
            renderedText = pygame.font.SysFont("Roboto", 80).render("Start", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (580,825))
            renderedText = pygame.font.SysFont("Roboto", 80).render("Maps", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (575,420))
            renderedText = pygame.font.SysFont("Roboto", 80).render("Player 1", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (100,300))
            renderedText = pygame.font.SysFont("Roboto", 80).render("Player 2", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (1000,300))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Back", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (50,900))
            
            # Character selection
            mainSurface.blit(spriteSheetIdle[0], (140, 390), playerRect[0])
            mainSurface.blit(spriteSheetIdle[1], (1050, 390), playerRect[1])
            
            if gun[0] == 'Pistol':
                mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Pistol.webp"), (100, 150)), (160, 580))
            elif gun[0] == 'Sniper':
                mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Sniper.webp"), (150, 100)), (135, 600))
            else:
                mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Shotgun.webp"), (150, 100)), (135, 600))
            
            if gun[1] == 'Pistol':
                mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Pistol.webp"), (100, 150)), (1065, 580))
            elif gun[1] == 'Sniper':
                mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Sniper.webp"), (150, 100)), (1040, 600))
            else:
                mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Shotgun.webp"), (150, 100)), (1040, 600))
            
            # Map selection
            if mapSelection == 1:
                mainSurface.blit(map1SelectionImage, (450, 500))
            elif mapSelection == 2:
                mainSurface.blit(map2SelectionImage, (450, 500))
            elif mapSelection == 3:
                mainSurface.blit(map3SelectionImage, (450, 500))
            
            # Buttons
            pygame.draw.rect(mainSurface, [255, 255, 255], [500,800,300,100], 2)
            
            # Map selection button
            pygame.draw.rect(mainSurface, [255, 255, 255], [875,550,50,100], 2)
            pygame.draw.rect(mainSurface, [255, 255, 255], [375,550,50,100], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(920,600), (880,575), (880,625)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(920,600), (880,575), (880,625)], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(380,600), (420,575), (420,625)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(380,600), (420,575), (420,625)], 2)
            
            # Colour change button
            pygame.draw.rect(mainSurface, [255, 255, 255], [280,420,30,60], 2)
            pygame.draw.rect(mainSurface, [255, 255, 255], [105,420,30,60], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(305,450), (285,435), (285,465)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(305,450), (285,435), (285,465)], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(110,450), (130,435), (130,465)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(110,450), (130,435), (130,465)], 2)
            
            pygame.draw.rect(mainSurface, [255, 255, 255], [1190,420,30,60], 2)
            pygame.draw.rect(mainSurface, [255, 255, 255], [1015,420,30,60], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(1215,450), (1195,435), (1195,465)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(1215,450), (1195,435), (1195,465)], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(1020,450), (1040,435), (1040,465)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(1020,450), (1040,435), (1040,465)], 2)
            
            # Gun change button
            pygame.draw.rect(mainSurface, [255, 255, 255], [280,620,30,60], 2)
            pygame.draw.rect(mainSurface, [255, 255, 255], [105,620,30,60], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(305,650), (285,635), (285,665)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(305,650), (285,635), (285,665)], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(110,650), (130,635), (130,665)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(110,650), (130,635), (130,665)], 2)
            
            pygame.draw.rect(mainSurface, [255, 255, 255], [1190,620,30,60], 2)
            pygame.draw.rect(mainSurface, [255, 255, 255], [1015,620,30,60], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(1215,650), (1195,635), (1195,665)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(1215,650), (1195,635), (1195,665)], 2)
            pygame.draw.polygon(mainSurface, [255, 255, 255], [(1020,650), (1040,635), (1040,665)])
            pygame.draw.polygon(mainSurface, [0, 0, 0], [(1020,650), (1040,635), (1040,665)], 2)
            
            pygame.draw.rect(mainSurface, [255, 255, 255], [20,890,150,60], 2)
            
            # If the button is pressed
            # Map selection button
            if mousePos[0] >= 875 and mousePos[0] <= 925 and mousePos[1] >= 550 and mousePos[1] <= 650:
                pygame.draw.rect(mainSurface, (255, 170, 0), [875,550,50,100], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if mapSelection == 1:
                        mapSelection = 2
                    elif mapSelection == 2:
                        mapSelection = 3
                    else:
                        mapSelection = 1
            elif mousePos[0] >= 375 and mousePos[0] <= 425 and mousePos[1] >= 550 and mousePos[1] <= 650:
                pygame.draw.rect(mainSurface, (255, 170, 0), [375,550,50,100], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if mapSelection == 1:
                        mapSelection = 3
                    elif mapSelection == 3:
                        mapSelection = 2
                    else:
                        mapSelection = 1
            # Colour change button
            elif mousePos[0] >= 280 and mousePos[0] <= 310 and mousePos[1] >= 420 and mousePos[1] <= 480:
                pygame.draw.rect(mainSurface, (255, 170, 0), [280,420,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if colour == 'Black':
                        colour = 'Blue'
                    elif colour == 'Blue':
                        colour = 'Green'
                    elif colour == 'Green':
                        colour = 'Red'
                    elif colour == 'Red':
                        colour = 'Yellow'
                    else:
                        colour = 'Black'
            elif mousePos[0] >= 105 and mousePos[0] <= 135 and mousePos[1] >= 420 and mousePos[1] <= 480:
                pygame.draw.rect(mainSurface, (255, 170, 0), [105,420,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if colour == 'Black':
                        colour = 'Yellow'
                    elif colour == 'Yellow':
                        colour = 'Red'
                    elif colour == 'Red':
                        colour = 'Green'
                    elif colour == 'Green':
                        colour = 'Blue'
                    else:
                        colour = 'Black'
            
            elif mousePos[0] >= 1190 and mousePos[0] <= 1220 and mousePos[1] >= 420 and mousePos[1] <= 480:
                pygame.draw.rect(mainSurface, (255, 170, 0), [1190,420,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if colour1 == 'Black':
                        colour1 = 'Blue'
                    elif colour1 == 'Blue':
                        colour1 = 'Green'
                    elif colour1 == 'Green':
                        colour1 = 'Red'
                    elif colour1 == 'Red':
                        colour1 = 'Yellow'
                    else:
                        colour1 = 'Black'
            elif mousePos[0] >= 1015 and mousePos[0] <= 1045 and mousePos[1] >= 420 and mousePos[1] <= 480:
                pygame.draw.rect(mainSurface, (255, 170, 0), [1015,420,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if colour1 == 'Black':
                        colour1 = 'Yellow'
                    elif colour1 == 'Yellow':
                        colour1 = 'Red'
                    elif colour1 == 'Red':
                        colour1 = 'Green'
                    elif colour1 == 'Green':
                        colour1 = 'Blue'
                    else:
                        colour1 = 'Black'
            
            # Gun change button
            elif mousePos[0] >= 280 and mousePos[0] <= 310 and mousePos[1] >= 620 and mousePos[1] <= 680:
                pygame.draw.rect(mainSurface, (255, 170, 0), [280,620,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if gun[0] == 'Pistol':
                        gun[0] = 'Sniper'
                    elif gun[0] == 'Sniper':
                        gun[0] = 'Shotgun'
                    else:
                        gun[0] = 'Pistol'
                    
            elif mousePos[0] >= 105 and mousePos[0] <= 135 and mousePos[1] >= 620 and mousePos[1] <= 680:
                pygame.draw.rect(mainSurface, (255, 170, 0), [105,620,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if gun[0] == 'Pistol':
                        gun[0] = 'Shotgun'
                    elif gun[0] == 'Shotgun':
                        gun[0] = 'Sniper'
                    else:
                        gun[0] = 'Pistol'
            
            elif mousePos[0] >= 1190 and mousePos[0] <= 1220 and mousePos[1] >= 620 and mousePos[1] <= 680:
                pygame.draw.rect(mainSurface, (255, 170, 0), [1190,620,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if gun[1] == 'Pistol':
                        gun[1] = 'Sniper'
                    elif gun[1] == 'Sniper':
                        gun[1] = 'Shotgun'
                    else:
                        gun[1] = 'Pistol'
                    
            elif mousePos[0] >= 1015 and mousePos[0] <= 1045 and mousePos[1] >= 620 and mousePos[1] <= 680:
                pygame.draw.rect(mainSurface, (255, 170, 0), [1015,620,30,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if gun[1] == 'Pistol':
                        gun[1] = 'Shotgun'
                    elif gun[1] == 'Shotgun':
                        gun[1] = 'Sniper'
                    else:
                        gun[1] = 'Pistol'
            
            elif mousePos[0] >= 20 and mousePos[0] <= 170 and mousePos[1] >= 890 and mousePos[1] <= 950:
                pygame.draw.rect(mainSurface, (255, 170, 0), [20,890,150,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    programState = 'start'
            
            # Start button
            elif mousePos[0] >= 500 and mousePos[0] <= 800 and mousePos[1] >= 800 and mousePos[1] <= 900:
                pygame.draw.rect(mainSurface, (255, 170, 0), [500,800,300,100], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    if mapSelection == 1:
                        maps = 1
                        lives = [3, 3]
                        playerPos[0] = [50,608]
                        playerPos[1] = [1100,608]
                        mapReset()
                    elif mapSelection == 2:
                        maps = 2
                        lives = [3, 3]
                        playerPos[0] = [50,608]
                        playerPos[1] = [1100,608]
                        mapReset()
                    else:
                        maps = 3
                        lives = [3, 3]
                        playerPos[0] = [300,608]
                        playerPos[1] = [850,608]
                        mapReset()
                    programState = 'customGame'
                    lastPlayed = 'custom'
                    mapTime = 0
                    
        elif programState == 'levels':
            # Filling the screen
            mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Background.webp"), (surfaceSize[0], surfaceSize[1])), (0, 0))

            # Words on the screen
            renderedText = title.render("Levels", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (530,200))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Level 1", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (580,430))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Level 2", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (580,550))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Level 3", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (580,670))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Back", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (50,900))
            
            # Buttons
            for i in range(400, 760, 120):
                pygame.draw.rect(mainSurface, [255, 255, 255], [450,i,400,100], 2)
            
            pygame.draw.rect(mainSurface, [255, 255, 255], [20,890,150,60], 2)
                
            # Changing the color if the mouse touches the button and changing the program state if clicked
            if mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 400 and mousePos[1] <= 500:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,400,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and mouseTime >= 0.2:
                    programState = 'level 1'
                    lastPlayed = 'level 1'
                    mapTime = 0
                    maps = 1
                    gun[0] = 'Pistol'
                    gun[1] = 'Pistol'
                    lives = [3, 3]
                    playerPos = [[50,608], [1100,608]]
                    mapReset()

            elif mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 520 and mousePos[1] <= 620:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,520,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and mouseTime >= 0.2:
                    programState = 'level 2'
                    lastPlayed = 'level 2'
                    mapTime = 0
                    maps = 2
                    gun[0] = 'Pistol'
                    gun[1] = 'Pistol'
                    lives = [3, 3]
                    playerPos = [[50,608], [1100,608]]
                    mapReset()
                    
            elif mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 640 and mousePos[1] <= 740:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,640,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and mouseTime >= 0.2:
                    programState = 'level 3'
                    lastPlayed = 'level 3'
                    mapTime = 0
                    maps = 3
                    gun[0] = 'Pistol'
                    gun[1] = 'Pistol'
                    lives = [3, 3]
                    playerPos = [[300,608], [850,608]]
                    mapReset()
            
            # Back button
            elif mousePos[0] >= 20 and mousePos[0] <= 170 and mousePos[1] >= 890 and mousePos[1] <= 950:
                pygame.draw.rect(mainSurface, (255, 170, 0), [20,890,150,60], 2)
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    programState = 'start'
        
        # Custom level
        elif programState == 'customGame':
            # The platforms
            if mapSelection == 1:
                mainSurface.blit(map1Image, (0,0))
                mainSurface.blit(map1Platform, (100,525))
                mainSurface.blit(map1Platform, (1000,525))
                mainSurface.blit(map1MainPlatform, (350,325))
            elif mapSelection == 2:
                mainSurface.blit(map2Image, (0,0))
                mainSurface.blit(map2Platform, (150,475))
                mainSurface.blit(map2Platform, (850,475))
            else:
                mainSurface.blit(map3Image, (0,0))
            
            # Time
            if 0 <= mapTime <= 1:
                renderedText = pygame.font.SysFont("Roboto", 100).render("3", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 1 <= mapTime <= 2:
                renderedText = pygame.font.SysFont("Roboto", 100).render("2", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 2 <= mapTime <= 3:
                renderedText = pygame.font.SysFont("Roboto", 100).render("1", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 3 <= mapTime <= 4:
                renderedText = pygame.font.SysFont("Roboto", 100).render("GO!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (570,460))
            
            # Lives
            for x in range(2):
                if lives[x] == 3:
                    for i in range(50, 200, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                elif lives[x] == 2:
                    for i in range(50, 150, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                else:
                    if x == 0:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (50, 800))
                    else:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (1100, 800))

            
            # Spawning the players
            for i in range(2):
                player(playerPos[i], playerRect[i], playerPatchNumber[i], playerSpeed[i], gravities[i], \
                playerFrameRate, playerMove[i], playerJump[i], playerShoot[i], bulletPos[i], bulletDirection[i], playerDirection[i], i)
                playerPatchNumber[i] = patchNumbers
                playerShoot[i] = bulletState
                gravities[i] = acceleration
            
            # If the player falls out of the map
            if maps == 2 or maps == 3:
                if playerPos[0][1] >= 1000:
                    lives[0] = 0
                elif playerPos[1][1] >= 1000:
                    lives[1] = 0
            
            # Win/Lose condition
            if lives[0] <= 0:
                programState = 'lose'
            elif lives[1] <= 0:
                programState = 'win'
                    
        # Level 1
        elif programState == 'level 1':
            # The platforms
            mainSurface.blit(map1Image, (0,0))
            mainSurface.blit(map1Platform, (100,525))
            mainSurface.blit(map1Platform, (1000,525))
            mainSurface.blit(map1MainPlatform, (350,325))
            
            # Time
            if 0 <= mapTime <= 1:
                renderedText = pygame.font.SysFont("Roboto", 100).render("3", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 1 <= mapTime <= 2:
                renderedText = pygame.font.SysFont("Roboto", 100).render("2", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 2 <= mapTime <= 3:
                renderedText = pygame.font.SysFont("Roboto", 100).render("1", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 3 <= mapTime <= 4:
                renderedText = pygame.font.SysFont("Roboto", 100).render("GO!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (570,460))
            
            # Lives
            for x in range(2):
                if lives[x] == 3:
                    for i in range(50, 200, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                elif lives[x] == 2:
                    for i in range(50, 150, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                else:
                    if x == 0:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (50, 800))
                    else:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (1100, 800))

            
            # A.I shooting
            if mapTime >= 3.5:
                if characterRect[0].colliderect((playerPos[1][0]+110, playerPos[1][1]+63, surfaceSize[0], 2)) and playerDirection[1] == 'Right':
                    playerShoot[1] = True
                elif characterRect[0].colliderect((0, playerPos[1][1]+63, playerPos[1][0]+40, 2)) and playerDirection[1] == 'Left':
                    playerShoot[1] = True
                    
                if moveTime >= 0.5:
                    movement = random.randint(1,3)
                    if movement == 1:
                        playerMove[1] = True
                    elif movement == 2:
                        playerDirection[1] = 'Left'
                        playerMove[1] = True
                    elif movement == 3:
                        playerDirection[1] = 'Right'
                        playerMove[1] = True
                    else:
                        playerMove[1] = False
                        playerJump[1] = False
                    moveTime = 0
                
                if playerPos[1][0] >= 1160:
                    playerDirection[1] = 'Left'
                elif playerPos[1][0] <= 50:
                    playerDirection[1] = 'Right'

            # Spawning the players
            for i in range(2):
                player(playerPos[i], playerRect[i], playerPatchNumber[i], playerSpeed[i], gravities[i], \
                playerFrameRate, playerMove[i], playerJump[i], playerShoot[i], bulletPos[i], bulletDirection[i], playerDirection[i], i)
                playerPatchNumber[i] = patchNumbers
                playerShoot[i] = bulletState
                gravities[i] = acceleration
            
            # Win/lose condition
            if lives[0] <= 0:
                programState = 'lose'
            elif lives[1] <= 0:
                programState = 'win'
        
        # Level 2
        elif programState == 'level 2':
            # The platforms
            mainSurface.blit(map2Image, (0,0))
            mainSurface.blit(map2Platform, (150,475))
            mainSurface.blit(map2Platform, (850,475))
            
            # Time
            if 0 <= mapTime <= 1:
                renderedText = pygame.font.SysFont("Roboto", 100).render("3", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 1 <= mapTime <= 2:
                renderedText = pygame.font.SysFont("Roboto", 100).render("2", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 2 <= mapTime <= 3:
                renderedText = pygame.font.SysFont("Roboto", 100).render("1", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 3 <= mapTime <= 4:
                renderedText = pygame.font.SysFont("Roboto", 100).render("GO!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (570,460))
            
            # Lives
            for x in range(2):
                if lives[x] == 3:
                    for i in range(50, 200, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                elif lives[x] == 2:
                    for i in range(50, 150, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                else:
                    if x == 0:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (50, 800))
                    else:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (1100, 800))

            if mapTime >= 3.5:
                # A.I shooting
                if characterRect[0].colliderect((playerPos[1][0]+110, playerPos[1][1]+63, surfaceSize[0], 2)) and playerDirection[1] == 'Right'\
                   and reloadTime[1] >= 0.5 and playerShoot[1] == False:
                    
                    playerShoot[1] = True
                    bulletPos[1][1] = playerPos[1][1] + 63
                    bulletPos[1][0] = playerPos[1][0] + 80
                    if playerDirection[1] == 'Right':
                        bulletDirection[1] = 'Right'
                    else:
                        bulletDirection[1] = 'Left'
                    reloadTime[1] = 0
                elif characterRect[0].colliderect((0, playerPos[1][1]+63, playerPos[1][0]+40, 2)) and playerDirection[1] == 'Left'\
                     and reloadTime[1] >= 0.5 and playerShoot[1] == False:
                    
                    playerShoot[1] = True
                    bulletPos[1][1] = playerPos[1][1] + 63
                    bulletPos[1][0] = playerPos[1][0] + 80
                    if playerDirection[1] == 'Right':
                        bulletDirection[1] = 'Right'
                    else:
                        bulletDirection[1] = 'Left'
                    reloadTime[1] = 0
                
                # A.I movement
                if moveTime >= 0.5:
                    movement = random.randint(1,4)
                    if movement == 1:
                        playerMove[1] = True
                    elif movement == 2 and jumpTime[1] >= 0.3:
                        playerJump[1] = True
                        playerRect[1][0] = 0*scale
                    elif movement == 3:
                        playerDirection[1] = 'Left'
                        playerMove[1] = True
                    elif movement == 4:
                        playerDirection[1] = 'Right'
                        playerMove[1] = True
                    else:
                        playerMove[1] = False
                        playerJump[1] = False
                    moveTime = 0
                
                if playerPos[1][0] >= 1160:
                    playerDirection[1] = 'Left'
                elif playerPos[1][0] <= 850:
                    playerDirection[1] = 'Right'
                
            # Spawning the players
            for i in range(2):
                player(playerPos[i], playerRect[i], playerPatchNumber[i], playerSpeed[i], gravities[i], \
                playerFrameRate, playerMove[i], playerJump[i], playerShoot[i], bulletPos[i], bulletDirection[i], playerDirection[i], i)
                playerPatchNumber[i] = patchNumbers
                playerShoot[i] = bulletState
                gravities[i] = acceleration
            
            # If the player falls out of the map
            if playerPos[0][1] >= 1000:
                lives[0] = 0
            elif playerPos[1][1] >= 1000:
                lives[1] = 0
            
            # Win/lose condition
            if lives[0] <= 0:
                programState = 'lose'
            elif lives[1] <= 0:
                programState = 'win'
        
        # Level 3
        elif programState == 'level 3':
            # The platforms
            mainSurface.blit(map3Image, (0,0))
            
            # Time
            if 0 <= mapTime <= 1:
                renderedText = pygame.font.SysFont("Roboto", 100).render("3", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 1 <= mapTime <= 2:
                renderedText = pygame.font.SysFont("Roboto", 100).render("2", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 2 <= mapTime <= 3:
                renderedText = pygame.font.SysFont("Roboto", 100).render("1", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (630,460))
            elif 3 <= mapTime <= 4:
                renderedText = pygame.font.SysFont("Roboto", 100).render("GO!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (570,460))
            
            # Lives
            for x in range(2):
                if lives[x] == 3:
                    for i in range(50, 200, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                elif lives[x] == 2:
                    for i in range(50, 150, 50):
                        if x == 0:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i, 800))
                        else:
                            mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (i+1050, 800))
                else:
                    if x == 0:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (50, 800))
                    else:
                        mainSurface.blit(pygame.transform.scale(pygame.image.load("images/heart.png"), (50, 50)), (1100, 800))

            if mapTime >= 3.5:
                # A.I shooting
                if characterRect[0].colliderect((0, playerPos[1][1]+63, surfaceSize[0], 2)) and reloadTime[1] >= 0.2 and playerShoot[1] == False:
                    if characterRect[0].colliderect((playerPos[1][0]+110, playerPos[1][1]+63, surfaceSize[0], 2)):
                        playerDirection[1] = 'Right'
                        playerShoot[1] = True
                        bulletPos[1][1] = playerPos[1][1] + 63
                        bulletPos[1][0] = playerPos[1][0] + 80
                        if playerDirection[1] == 'Right':
                            bulletDirection[1] = 'Right'
                        else:
                            bulletDirection[1] = 'Left'
                        reloadTime[1] = 0
                    elif characterRect[0].colliderect((0, playerPos[1][1]+63, playerPos[1][0]+40, 2)):
                        playerDirection[1] = 'Left'
                        playerShoot[1] = True
                        bulletPos[1][1] = playerPos[1][1] + 63
                        bulletPos[1][0] = playerPos[1][0] + 80
                        if playerDirection[1] == 'Right':
                            bulletDirection[1] = 'Right'
                        else:
                            bulletDirection[1] = 'Left'
                        reloadTime[1] = 0
                
                # A.I movement
                if moveTime >= 0.2:
                    movement = random.randint(1,4)
                    if movement == 1:
                        playerMove[1] = True
                    elif movement == 2 and jumpTime[1] >= 0.3:
                        playerJump[1] = True
                        playerRect[1][0] = 0*scale
                    elif movement == 3:
                        playerMove[1] = True
                        playerDirection[1] = 'Left'
                    elif movement == 4:
                        playerMove[1] = True
                        playerDirection[1] = 'Right'
                    elif movement == 5:
                        playerJump[1] = True
                        playerMove[1] = True
                        playerRect[1][0] = 0*scale
                        moveTime = 0
                    moveTime = 0
                
                if playerPos[1][0] >= 900:
                    playerDirection[1] = 'Left'
                elif playerPos[1][0] <= 250:
                    playerDirection[1] = 'Right'

            # Spawning the players
            for i in range(2):
                player(playerPos[i], playerRect[i], playerPatchNumber[i], playerSpeed[i], gravities[i], \
                playerFrameRate, playerMove[i], playerJump[i], playerShoot[i], bulletPos[i], bulletDirection[i], playerDirection[i], i)
                playerPatchNumber[i] = patchNumbers
                playerShoot[i] = bulletState
                gravities[i] = acceleration
            
            # If the player falls out of the map
            if playerPos[0][1] >= 1000:
                lives[0] = 0
            elif playerPos[1][1] >= 1000:
                lives[1] = 0
            
            # Win/lose condition
            if lives[0] <= 0:
                programState = 'lose'
            elif lives[1] <= 0:
                programState = 'win'
        
        # If the player is shooting
        for i in range(2):
            if playerShoot[i] == True:
                pygame.draw.rect(mainSurface, (255,255,0), (bulletPos[i][0], bulletPos[i][1], 20, 4))
                # If using a pistol
                if gun[i] == 'Pistol':
                    if bulletDirection[i] == 'Right':
                        bulletPos[i][0] += 30
                    elif bulletDirection[i] == 'Left':
                        bulletPos[i][0] -= 30
                # If using a sniper
                elif gun[i] == 'Sniper':
                    if bulletDirection[i] == 'Right':
                        bulletPos[i][0] += 60
                    elif bulletDirection[i] == 'Left':
                        bulletPos[i][0] -= 60
                # If using a shotgun
                elif gun[i] == 'Shotgun':
                    pygame.draw.rect(mainSurface, (255,255,0), (bulletPos[i][0], bulletPos[i][1], 20, 4))
                    pygame.draw.rect(mainSurface, (255,255,0), (bulletPos[i+2][0], bulletPos[i+2][1], 20, 4))
                    pygame.draw.rect(mainSurface, (255,255,0), (bulletPos[i+4][0], bulletPos[i+4][1], 20, 4))
                    if bulletDirection[i] == 'Right':
                        bulletPos[i][0] += 30
                        bulletPos[i][1] += 2
                        bulletPos[i+2][0] += 30
                        bulletPos[i+2][1] += 0
                        bulletPos[i+4][0] += 30
                        bulletPos[i+4][1] -= 2
                    elif bulletDirection[i] == 'Left':
                        bulletPos[i][0] -= 30
                        bulletPos[i][1] += 2
                        bulletPos[i+2][0] -= 30
                        bulletPos[i+2][1] += 0
                        bulletPos[i+4][0] -= 30
                        bulletPos[i+4][1] -= 2
                # Resetting the position of the bullet
                if gun[i] == 'Pistol' or gun[i] == 'Sniper':
                    if bulletPos[i][0] >= surfaceSize[0] or bulletPos[i][0] <= 0:
                        bulletPos[i][0] = playerPos[i][0]+80
                        bulletPos[i][1] = playerPos[i][1]+63
                        playerShoot[i] = False
                
                if gun[i] == 'Shotgun':
                    if bulletPos[i][0] >= (playerPos[i][0]+400) or bulletPos[i][0] <= (playerPos[i][0]-400):
                        bulletPos[i][0] = playerPos[i][0]+80
                        bulletPos[i][1] = playerPos[i][1]+63
                        bulletPos[i+2][0] = playerPos[i][0]+80
                        bulletPos[i+2][1] = playerPos[i][1]+63
                        bulletPos[i+4][0] = playerPos[i][0]+80
                        bulletPos[i+4][1] = playerPos[i][1]+63
                        playerShoot[i] = False
                        
            elif programState == 'customGame' or programState == 'level 1' or programState == 'level 2' or programState == 'level 3':
                if gun[i] == 'Sniper':
                    if playerDirection[i] == 'Right':
                        pygame.draw.rect(mainSurface, (255,0,0), (playerPos[i][0]+110, playerPos[i][1]+63, surfaceSize[0], 2))
                    elif playerDirection[i] == 'Left':
                        pygame.draw.rect(mainSurface, (255,0,0), (0, playerPos[i][1]+63, playerPos[i][0]+40, 2))
        
        # Win screen
        if programState == 'win':
            # Filling the screen
            mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Background.webp"), (surfaceSize[0], surfaceSize[1])), (0, 0))
            
            if lastPlayed == 'custom':
                renderedText = title.render("Player 1 won!!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (400,200))
            else:
                renderedText = title.render("You won!!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (500,200))
                mapTime = round(mapTime, 2)
                renderedText = pygame.font.SysFont("Roboto", 50).render(f"Time: {mapTime}s", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (580,300))
            
                # Highscore display
                if lastPlayed == 'level 1':
                    if mapTime <= bestTime[0]:
                        bestTime[0] = mapTime
                    renderedText = pygame.font.SysFont("Roboto", 50).render(f"Best time: {bestTime[0]}s", 1, pygame.Color(255, 255, 255))
                    mainSurface.blit(renderedText, (540,350))
                elif lastPlayed == 'level 2':
                    if mapTime <= bestTime[1]:
                        bestTime[1] = mapTime
                    renderedText = pygame.font.SysFont("Roboto", 50).render(f"Best time: {bestTime[1]}s", 1, pygame.Color(255, 255, 255))
                    mainSurface.blit(renderedText, (540,350))
                elif lastPlayed == 'level 3':
                    if mapTime <= bestTime[2]:
                        bestTime[2] = mapTime
                    renderedText = pygame.font.SysFont("Roboto", 50).render(f"Best time: {bestTime[2]}s", 1, pygame.Color(255, 255, 255))
                    mainSurface.blit(renderedText, (540,350))
            
            # Words display
            renderedText = pygame.font.SysFont("Roboto", 60).render("Play again?", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (540,430))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Main menu", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (550,580))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Quit", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (600,730))
            
            # Writing the highscores
            file = open('Highscore.txt', 'w')
            for i in range(3):
                file.write(f"{str(bestTime[i])}\n")
            file.close()
            
            # Buttons
            for i in range(400, 850, 150):
                pygame.draw.rect(mainSurface, [255, 255, 255], [450,i,400,100], 2)
                            
            # Changing the color if the mouse touches the button
            if mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 400 and mousePos[1] <= 500:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,400,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    mapTime = 0
                    if lastPlayed == 'level 1':
                        programState = lastPlayed
                        maps = 1
                        lives = [3, 3]
                        playerPos[0] = [50,608]
                        playerPos[1] = [1100,608]
                        mapReset()

                    elif lastPlayed == 'level 2':
                        programState = lastPlayed
                        maps = 2
                        lives = [3, 3]
                        playerPos[0] = [50,608]
                        playerPos[1] = [1100,608]
                        mapReset()

                    elif lastPlayed == 'level 3':
                        programState = lastPlayed
                        maps = 3
                        lives = [3, 3]
                        playerPos[0] = [300,608]
                        playerPos[1] = [850,608]
                        mapReset()

                    elif lastPlayed == 'custom':
                        programState = lastPlayed
            
            # Back to main menu button
            elif mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 550 and mousePos[1] <= 650:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,550,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    programState = 'start'
            
            # Quit button
            elif mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 700 and mousePos[1] <= 800:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,700,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    break
        
        # Lose screen
        if programState == 'lose':
            # Filling the screen
            mainSurface.blit(pygame.transform.scale(pygame.image.load("Images/Background.webp"), (surfaceSize[0], surfaceSize[1])), (0, 0))
            
            # Words display
            if lastPlayed == 'custom':
                renderedText = title.render("Player 2 won!!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (400,200))
            else:
                renderedText = title.render("You lost!!", 1, pygame.Color(255, 255, 255))
                mainSurface.blit(renderedText, (500,200))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Play again?", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (540,430))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Main menu", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (550,580))
            renderedText = pygame.font.SysFont("Roboto", 60).render("Quit", 1, pygame.Color(255, 255, 255))
            mainSurface.blit(renderedText, (600,730))
            
            # Buttons
            for i in range(400, 850, 150):
                pygame.draw.rect(mainSurface, [255, 255, 255], [450,i,400,100], 2)
                            
            # Changing the color if the mouse touches the button
            if mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 400 and mousePos[1] <= 500:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,400,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    mapTime = 0
                    if lastPlayed == 'level 1':
                        programState = lastPlayed
                        maps = 1
                        lives = [3, 3]
                        playerPos[0] = [50,608]
                        playerPos[1] = [1100,608]
                        mapReset()

                    elif lastPlayed == 'level 2':
                        programState = lastPlayed
                        maps = 2
                        lives = [3, 3]
                        playerPos[0] = [50,608]
                        playerPos[1] = [1100,608]
                        mapReset()

                    elif lastPlayed == 'level 3':
                        programState = lastPlayed
                        maps = 3
                        lives = [3, 3]
                        playerPos[0] = [300,608]
                        playerPos[1] = [850,608]
                        mapReset()

                    elif lastPlayed == 'custom':
                        programState = lastPlayed
            
            # Back to main menu button
            elif mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 550 and mousePos[1] <= 650:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,550,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    programState = 'start'
            
            # Quit button
            elif mousePos[0] >= 450 and mousePos[0] <= 850 and mousePos[1] >= 700 and mousePos[1] <= 800:
                pygame.draw.rect(mainSurface, (255, 170, 0), [450,700,400,100], 2)
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    break
        
        # Character hitbox
        characterRect = [pygame.Rect((playerPos[0][0]+35,playerPos[0][1]+20,48*scale-80,39*scale-20)), \
                        pygame.Rect((playerPos[1][0]+35,playerPos[1][1]+20,48*scale-80,39*scale-20))]
        # Bullet hitbox
        bulletRect = [pygame.Rect(bulletPos[0][0], bulletPos[0][1], 20, 4), pygame.Rect(bulletPos[1][0], bulletPos[1][1], 20, 4), pygame.Rect(bulletPos[2][0], bulletPos[2][1], 20, 4), \
                      pygame.Rect(bulletPos[3][0], bulletPos[3][1], 20, 4), pygame.Rect(bulletPos[4][0], bulletPos[4][1], 20, 4), pygame.Rect(bulletPos[5][0], bulletPos[5][1], 20, 4)]
        
        # Bullet collision
        # Pistol or sniper
        if gun[0] == 'Pistol' or gun[0] == 'Sniper':
            if bulletRect[0].colliderect(characterRect[1]) and playerShoot[0] == True:
                bulletPos[0][0] = playerPos[0][0]+80
                playerShoot[0] = False
                if gun[0] == 'Pistol':
                    lives[1] -= 1
                elif gun[0] == 'Sniper':
                    lives[1] -= 3
        if gun[1] == 'Pistol' or gun[1] == 'Sniper':
            if bulletRect[1].colliderect(characterRect[0]) and playerShoot[1] == True:
                bulletPos[1][0] = playerPos[1][0]+80
                playerShoot[1] = False
                if gun[1] == 'Pistol':
                    lives[0] -= 1
                elif gun[1] == 'Sniper':
                    lives[0] -= 3
        
        # Shotgun
        if gun[0] == 'Shotgun':
            if bulletRect[0].colliderect(characterRect[1]) and playerShoot[0] == True:
                bulletPos[0][0] = playerPos[0][0]+80
                lives[1] -= 2
                playerShoot[0] = False
            if bulletRect[2].colliderect(characterRect[1]) and playerShoot[0] == True:
                bulletPos[2][0] = playerPos[0][0]+80
                lives[1] -= 2
                playerShoot[0] = False
            if bulletRect[4].colliderect(characterRect[1]) and playerShoot[0] == True:
                bulletPos[4][0] = playerPos[0][0]+80
                lives[1] -= 2
                playerShoot[0] = False
        if gun[1] == 'Shotgun':
            if bulletRect[1].colliderect(characterRect[0]) and playerShoot[1] == True:
                bulletPos[1][0] = playerPos[1][0]+80
                lives[0] -= 2
                playerShoot[1] = False
            if bulletRect[3].colliderect(characterRect[0]) and playerShoot[1] == True:
                bulletPos[3][0] = playerPos[1][0]+80
                lives[0] -= 2
                playerShoot[1] = False
            if bulletRect[5].colliderect(characterRect[0]) and playerShoot[1] == True:
                bulletPos[5][0] = playerPos[1][0]+80
                lives[0] -= 2
                playerShoot[1] = False

        
        
        # Collision for the first map
        if maps == 1:
            # Collision
            for i in range(2):
                # Collision with the ground
                if characterRect[i].colliderect(pygame.Rect(0, 800, surfaceSize[0], 200)):        #A collision happens!
                    playerJump[i] = False
                    playerPos[i][1] = 683
                    gravities[i] = 0
                    collision(characterRect[i], (0, 0, 0, 0), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                # Collision with platforms
                elif characterRect[i].colliderect(pygame.Rect(map1[0])):
                    collision(characterRect[i], map1[0], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map1[1])):
                    collision(characterRect[i], map1[1], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map1[2])):
                    collision(characterRect[i], map1[2], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(0, 725, surfaceSize[0], 200)):
                    collision(characterRect[i], (0, 725, surfaceSize[0], 200), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                # Collision with the side
                elif characterRect[i].colliderect(pygame.Rect(-50, 0, 50, surfaceSize[1])):
                    collision(characterRect[i], (-50, 0, 50, surfaceSize[1]), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(surfaceSize[0], 0, 50, surfaceSize[1])):
                    collision(characterRect[i], (surfaceSize[0], 0, 50, surfaceSize[1]), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                else:
                    if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a] or \
                        pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
                        playerSpeed[i] = 4
                    collision(characterRect[i], (0, 0, 0, 0), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                playerPos[i] = characterPosition
                gravities[i] = characterGravity
                playerJump[i] = characterJump
                playerDirection[i] = characterDirection
                playerSpeed[i] = characterSpeed
        
        # Collision for the second map
        elif maps == 2:
            # Collision
            for i in range(2):
                # Collision with the ground
                if characterRect[i].colliderect(pygame.Rect(0, 715, 420, 10)) or characterRect[i].colliderect(pygame.Rect(880, 715, 525, 10)):        #A collision happens!
                    playerJump[i] = False
                    gravities[i] = 0
                    collision(characterRect[i], (0, 0, 0, 0), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                # Collision with platforms
                if characterRect[i].colliderect(pygame.Rect(map2[0])):
                    collision(characterRect[i], map2[0], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map2[1])):
                    collision(characterRect[i], map2[1], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(0, 715, 525, 500)):
                    collision(characterRect[i], (0, 715, 525, 10), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(775, 715, 525, 500)):
                    collision(characterRect[i], (775, 715, 525, 10), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                # Collision with the side
                elif characterRect[i].colliderect(pygame.Rect(-50, 0, 50, surfaceSize[1])):
                    collision(characterRect[i], (-50, 0, 50, surfaceSize[1]), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(surfaceSize[0], 0, 50, surfaceSize[1])):
                    collision(characterRect[i], (surfaceSize[0], 0, 50, surfaceSize[1]), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                else:
                    if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a] or \
                        pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
                        playerSpeed[i] = 4
                    collision(characterRect[i], (0, 0, 0, 0), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                playerPos[i] = characterPosition
                gravities[i] = characterGravity
                playerJump[i] = characterJump
                playerDirection[i] = characterDirection
                playerSpeed[i] = characterSpeed
                        
        # Collision for the third map
        elif maps == 3:
            # Collision
            for i in range(2):
                # Collision with platforms
                if characterRect[i].colliderect(pygame.Rect(map3[0])):
                    collision(characterRect[i], map3[0], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map3[1])):
                    collision(characterRect[i], map3[1], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map3[2])):
                    collision(characterRect[i], map3[2], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map3[3])):
                    collision(characterRect[i], map3[3], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map3[4])):
                    collision(characterRect[i], map3[4], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(map3[5])):
                    collision(characterRect[i], map3[5], playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                # Collision with the side
                elif characterRect[i].colliderect(pygame.Rect(-70, 0, 50, surfaceSize[1])):
                    collision(characterRect[i], (-70, 0, 50, surfaceSize[1]), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                elif characterRect[i].colliderect(pygame.Rect(surfaceSize[0]+10, 0, 50, surfaceSize[1])):
                    collision(characterRect[i], (surfaceSize[0]+10, 0, 50, surfaceSize[1]), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])
                else:
                    if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a] or \
                        pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_LEFT]:
                        playerSpeed[i] = 4
                    collision(characterRect[i], (0, 0, 0, 0), playerPos[i], gravities[i], playerJump[i], playerDirection[i], playerSpeed[i])

                playerPos[i] = characterPosition
                gravities[i] = characterGravity
                playerJump[i] = characterJump
                playerDirection[i] = characterDirection
                playerSpeed[i] = characterSpeed
                
        pygame.display.flip()
        
        frameCount += 1
        clock.tick(frameRate) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.
# Running the main loop
main()