import pygame, sys, math, random

pygame.init()
WINDOWSIZE = WINDOWWIDTH, WINDOWHEIGHT = 1000, 600
SCREEN = pygame.display.set_mode(WINDOWSIZE)
pygame.display.set_caption("Aim Pong")
comicSansMs = pygame.font.SysFont("comicsansms", 45)

#Constantes de coleur
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SKYBLUE = (119, 181, 254)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def mainLoop():
    global SCREEN
    mouseX = 0
    mouseY = 0
    mouseClick = False
    mainRunning = True

    while mainRunning == True:
        mouseClick = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainRunning = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mainRunning = False
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                mouseClick = True

        menuChoice = menu(mouseX, mouseY, mouseClick)          

        if menuChoice == 3:
            mainRunning = False
        elif menuChoice == 2:
            gameLoop(False)
        elif menuChoice == 1:
            gameLoop(True)

def menu(mouseX, mouseY,mouseClick):
    global BLACK, BLUE, DARKBLUE, SKYBLUE, comicSansMs
    
    soloButonColor = BLUE
    doubleButtonColor = BLUE
    exitButtonColor = BLUE
    
    soloPlayer = button(4, 8, 1)
    doublePlayer = button(4, 8, 2)
    progExit = button(4, 8, 3)

    rendSoloPlayer = comicSansMs.render("Solo Player", True, BLACK)
    rendDoublePlayer = comicSansMs.render("2 Players", True, BLACK)
    rendProgExit = comicSansMs.render("Quit Game", True, BLACK)

    if soloPlayer.collidepoint(mouseX, mouseY):
        soloButonColor = SKYBLUE
        if mouseClick == True:
            return 1
    elif doublePlayer.collidepoint(mouseX, mouseY):
        doubleButtonColor = SKYBLUE
        if mouseClick == True:
            return 2
    elif progExit.collidepoint(mouseX, mouseY):
        exitButtonColor = SKYBLUE
        if mouseClick == True:
            return 3

    SCREEN.fill(BLACK)

    pygame.draw.rect(SCREEN, soloButonColor, soloPlayer)
    pygame.draw.rect(SCREEN, doubleButtonColor, doublePlayer)
    pygame.draw.rect(SCREEN, exitButtonColor, progExit)

    SCREEN.blit(rendSoloPlayer, (soloPlayer.x, soloPlayer.y - 5))
    SCREEN.blit(rendDoublePlayer, (doublePlayer.x, doublePlayer.y - 5))
    SCREEN.blit(rendProgExit, (progExit.x, progExit.y - 5))
    
    pygame.display.flip()
    
def button(x, y, buttonOrder):
    global WINDOWWIDTH, WINDOWHEIGHT

    position = posX, posY = (WINDOWWIDTH  - (WINDOWWIDTH / x)) / 2, (WINDOWHEIGHT / y) * buttonOrder + ((WINDOWHEIGHT / y) * (buttonOrder - 1)) + ((WINDOWHEIGHT / y) / 2)
    buttonSize = buttonW, buttonH = WINDOWWIDTH / x, (WINDOWHEIGHT / y)
    button = pygame.rect.Rect(posX, posY, buttonW, buttonH)

    return button

def gameLoop(bot):
    global WINDOWWIDTH, WINDOWHEIGHT

    gameRunning = True
    clock = pygame.time.Clock()
    racketSize = racketWidth, racketHeight = 6, 80
    ballSize = ballWidth, ballHeight = 16, 16
    entities = {'rightRacket': pygame.rect.Rect((WINDOWWIDTH - 20) - racketWidth, (WINDOWHEIGHT / 2) - (racketHeight / 2), racketWidth, racketHeight),
                'leftRacket': pygame.rect.Rect(20, (WINDOWHEIGHT / 2) - (racketHeight / 2), racketWidth, racketHeight),
                'ball': pygame.rect.Rect((WINDOWWIDTH / 2) - (ballWidth / 2), (WINDOWHEIGHT / 2) - (ballHeight / 2), ballWidth, ballHeight),
                'rightAim': (-18, 0),
                'leftAim': (18, 0),
                'ballMoment': (18, 0)}
    events = {'quit': False,
              'escape': False,
              'w': False,
              's': False,
              'a': False,
              'd': False,
              'up': False,
              'down': False,
              'right': False,
              'left': False}

    score = (0, 0)
    gameReset(entities)
    time = pygame.time.get_ticks()

    while gameRunning == True:
        clock.tick(60)
        events = eventManager(events, bot)   

        if events is not None:
            if events['quit'] == True or events['escape'] == True:
                gameRunning = False

        if bot == True:
            AI(entities, time)
            
        gameUpdate(entities, events)
        score = gameLogic(entities, score)
        drawGame(entities, score)
    
def drawGame(entities, score):
    global WINDOWWIDTH, WINDOWHEIGHT, SCREEN, GREEN, BLACK
    rightAimX, rightAimY = entities['rightAim']
    leftAimX, leftAimY = entities['leftAim']
    tempScoreL, tempScoreR = score
    
    SCREEN.fill(BLACK)

    #Dessin du Terrain
    pygame.draw.line(SCREEN, WHITE, (20, 0), (20, WINDOWHEIGHT), 4)
    pygame.draw.line(SCREEN, WHITE, (WINDOWWIDTH - 22, 0), (WINDOWWIDTH - 22, WINDOWHEIGHT), 4)
    pygame.draw.line(SCREEN, WHITE, ((WINDOWWIDTH / 2) - 2, 0), ((WINDOWWIDTH / 2) - 2, WINDOWHEIGHT), 4)
    pygame.draw.line(SCREEN, WHITE, (20, 0), (WINDOWWIDTH - 22, 0), 3)
    pygame.draw.line(SCREEN, WHITE, (20, WINDOWHEIGHT - 3), (WINDOWWIDTH - 22, WINDOWHEIGHT - 3), 4)
    pygame.draw.circle(SCREEN, WHITE, (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2)), 100, 4)
    
    #Dessin des Entitiés
    pygame.draw.rect(SCREEN, GREEN, entities['rightRacket'])
    pygame.draw.rect(SCREEN, GREEN, entities['leftRacket'])
    pygame.draw.line(SCREEN, RED, (entities['rightRacket'].x, entities['rightRacket'].y + (entities['rightRacket'].height / 2)), ((entities['rightRacket'].x + (rightAimX * 2)), entities['rightRacket'].y + (entities['rightRacket'].height / 2) + (rightAimY * 2)), 2)
    pygame.draw.line(SCREEN, RED, (entities['leftRacket'].x + entities['leftRacket'].width - 2, entities['leftRacket'].y + (entities['leftRacket'].height / 2)),((entities['leftRacket'].x + entities['leftRacket'].width - 2) + (leftAimX * 2), entities['leftRacket'].y + (entities['leftRacket'].height / 2) + (leftAimY * 2)), 2)
    pygame.draw.ellipse(SCREEN, GREEN, entities['ball'])


    #Dessin Tableau des Scores
    rendPlayer1 = comicSansMs.render(str(tempScoreL), True, WHITE)
    rendPlayer2 = comicSansMs.render(str(tempScoreR), True, WHITE)

    SCREEN.blit(rendPlayer1, (WINDOWWIDTH / 4 - 10, 0))
    SCREEN.blit(rendPlayer2, ((WINDOWWIDTH / 4) * 3 - 10, 0))
    
    pygame.display.flip()

def eventManager(events, bot):
    if events is not None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events['quit'] = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    events['escape'] = True
                if bot != True:
                    if event.key == pygame.K_w:
                        events['w'] = True
                    elif event.key == pygame.K_s:
                        events['s'] = True
                    elif event.key == pygame.K_a:
                        events['a'] = True
                    elif event.key == pygame.K_d:
                        events['d'] = True
                if event.key == pygame.K_UP:
                    events['up'] = True
                elif event.key == pygame.K_DOWN:
                    events['down'] = True
                elif event.key == pygame.K_RIGHT:
                    events['right'] = True
                elif event.key == pygame.K_LEFT:
                    events['left'] = True
            elif event.type == pygame.KEYUP:
                if bot != True:
                    if event.key == pygame.K_ESCAPE:
                        events['escape'] = False
                    elif event.key == pygame.K_w:
                        events['w'] = False
                    elif event.key == pygame.K_s:
                        events['s'] = False
                    elif event.key == pygame.K_a:
                        events['a'] = False
                    elif event.key == pygame.K_d:
                        events['d'] = False
                if event.key == pygame.K_UP:
                    events['up'] = False
                elif event.key == pygame.K_DOWN:
                    events['down'] = False
                elif event.key == pygame.K_RIGHT:
                    events['right'] = False
                elif event.key == pygame.K_LEFT:
                    events['left'] = False

        return events
    

def gameUpdate(entities, keyStatus):
    global WINDOWSWIDHT, WINDOWHEIGHT
    
    if keyStatus is not None:
        if entities['rightRacket'].y >= 0:
            entities['rightRacket'].y = entities['rightRacket'].y - (6 * keyStatus['up'])
        if entities['rightRacket'].y <= WINDOWHEIGHT - entities['rightRacket'].height:
            entities['rightRacket'].y = entities['rightRacket'].y + (6 * keyStatus['down'])
        if entities['leftRacket'].y >= 0:
            entities['leftRacket'].y = entities['leftRacket'].y - (6 * keyStatus['w'])
        if entities['leftRacket'].y <= WINDOWHEIGHT - entities['leftRacket'].height:
            entities['leftRacket'].y = entities['leftRacket'].y + (6 * keyStatus['s'])

        rightAimX, rightAimY = entities['rightAim']
        if rightAimY >= -10:
            rightAimY = rightAimY - keyStatus['right']
        if rightAimY <= 10:
            rightAimY = rightAimY + keyStatus['left']
        rightAimX = 18 - math.sqrt(pow(rightAimY, 2))
        if rightAimX >= 0:
            rightAimX = rightAimX * (-1)
        entities['rightAim'] = rightAimX, rightAimY

        leftAimX, leftAimY = entities['leftAim']
        if leftAimY >= -10:
            leftAimY = leftAimY - (0.15 * keyStatus['d'])
        if leftAimY <= 10:
            leftAimY = leftAimY + (0.15 * keyStatus['a'])
        leftAimX = 18 - math.sqrt(pow(leftAimY, 2))
        if leftAimX <= 0:
            leftAimX = leftAimX * (-1)
        entities['leftAim'] = leftAimX, leftAimY

        ball1MomentX, ball1MomentY = entities['ballMoment']
        if (ball1MomentX / 2.5) < 1 and (ball1MomentX / 2.5) > - 1:
            entities['ball'].x = entities['ball'].x + 1
        else:
            entities['ball'].x = entities['ball'].x + (ball1MomentX / 2)
            
        entities['ball'].y = entities['ball'].y + (ball1MomentY / 2)
        

def gameLogic(entities, score):
    tempScoreL, tempScoreR = score
    hitSound = pygame.mixer.Sound("hitSound.wav")
    pointSound = pygame.mixer.Sound("pointSound.wav")
    hitSound.set_volume(0.5)
    pointSound.set_volume(0.5)
    if entities['ball'].y <= 0:
        ballMomentX, ballMomentY = entities['ballMoment']
        ballMomentY = math.sqrt(pow(ballMomentY,2))
        entities['ballMoment'] = ballMomentX, ballMomentY
    if  entities['ball'].y >= WINDOWHEIGHT - entities['ball'].height:
        ballMomentX, ballMomentY = entities['ballMoment']
        ballMomentY = 0 - math.sqrt(pow(ballMomentY,2))
        entities['ballMoment'] = ballMomentX, ballMomentY
    if entities['ball'].colliderect(entities['rightRacket']):
        hitSound.play()
        entities['ballMoment'] = entities['rightAim']
    if entities['ball'].colliderect(entities['leftRacket']):
        hitSound.play()
        entities['ballMoment'] = entities['leftAim']
    if entities['ball'].x >= WINDOWWIDTH:
        pointSound.play()
        tempScoreL = tempScoreL + 1
        gameReset(entities)
    if entities['ball'].x <= 0:
        pointSound.play()
        tempScoreR = tempScoreR + 1
        gameReset(entities)

    score = tempScoreL, tempScoreR
    return score
            
def gameReset(entities):
    global WINDOWWIDTH, WINDOWHEIGHT

    tempMomentX, tempMomentY = entities['ballMoment']

    entities['rightAim'] = (-18, 0)
    entities['leftAim'] =  (18, 0)
    entities['ball'].x = (WINDOWWIDTH / 2) - (entities['ball'].width / 2)
    entities['ball'].y = (WINDOWHEIGHT / 2) - (entities['ball'].height / 2)
    entities['rightRacket'].y = (WINDOWHEIGHT / 2) - (entities['ball'].height / 2)
    entities['leftRacket'].y = (WINDOWHEIGHT / 2) - (entities['ball'].height / 2)

    tempMomentY = (random.randrange(34) - 17)
    if random.randrange(2) == 0:
        tempMomentX = 18 - tempMomentY
    else:
        tempMomentX = (18 - tempMomentY) * -1

    entities['ballMoment']  = (tempMomentX / 2), (tempMomentY / 2)

def AI(entities, timer):
    ballMomentumX, ballMomentumY = entities['ballMoment'] 
    bMX, bMY = 0, 0
    bHitX, bHitY = 0, 0
    offset = 0
    if timer < pygame.time.get_ticks() - 500:
        if ballMomentumX < 0:
            temp = (entities['ball'].x - bHitX) // ballMomentumX
            bHitY = math.sqrt(pow((ballMomentumY * temp) - entities['ball'].y + (entities['ball'].height / 2), 2))
            bMX = ballMomentumX
            bMY = ballMomentumY
            offset = random.randrange(90) - 45
            bHitY = offset + bHitY
            tempAimX, tempAimY = entities['leftAim']
            tempAimX = random.randrange(1, 35) - 10
            tempAimY = tempAimX - 18
            entities['leftAim'] = tempAimX, tempAimY
            timer = pygame.time.get_ticks()

        if entities['leftRacket'].y + (entities['leftRacket'].height / 2) > bHitY - 9 and entities['leftRacket'].y + (entities['leftRacket'].height / 2) > bHitY + 9:
            if entities['leftRacket'].y >= 0:
                entities['leftRacket'].y = entities['leftRacket'].y - 6
        elif entities['leftRacket'].y + (entities['leftRacket'].height / 2) < bHitY - 9 and entities['leftRacket'].y + (entities['leftRacket'].height / 2) < bHitY + 9:
            if entities['leftRacket'].y <= WINDOWHEIGHT - entities['leftRacket'].height:
                entities['leftRacket'].y = entities['leftRacket'].y + 6


            

mainLoop()
pygame.quit()
