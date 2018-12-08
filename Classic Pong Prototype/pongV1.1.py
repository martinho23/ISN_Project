import sys, pygame, random, math
pygame.init()

size = width, height = 900, 600
screen = pygame.display.set_mode(size)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
racketDmove = 0
racketGmove = 0
botMove = 0
rightRacket = pygame.rect.Rect(865, 275, 6, 70)
leftRacket = pygame.rect.Rect(29, 275, 6, 70)
ball = pygame.rect.Rect(394, 295, 12, 12)
ballMomentum = ballMomentumX, ballMomentumY = 0, 0
bM = bMX, bMY = 0, 0
bHitX, bHitY = 25, 0
running = True
scoreP1 = 0
scoreP2 = 0
random.seed()

def playerUpdate(player, direction):
    if direction == 1 and player.y >= 0:
        player.y = player.y - 6
    elif direction == 2 and player.y <= height - player.height:
        player.y = player.y + 6


def screenUpdate():
    screen.fill(BLACK)

    pygame.draw.rect(screen, GREEN, rightRacket);
    pygame.draw.rect(screen, GREEN, leftRacket);
    pygame.draw.ellipse(screen, GREEN, ball);

    pygame.display.flip()

def eventManager():
    global racketDmove
    global racketGmove
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    running = False
                if event.key == pygame.K_UP:
                    racketDmove = 1
                if event.key == pygame.K_DOWN:
                    racketDmove = 2
                if event.key == pygame.K_w:
                    racketGmove = 1
                if event.key == pygame.K_s:
                    racketGmove = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    racketDmove = 0
                if event.key == pygame.K_DOWN:
                    racketDmove = 0
                if event.key == pygame.K_w:
                    racketGmove = 0
                if event.key == pygame.K_s:
                    racketGmove = 0

def gameLogic():
    global ball
    global ballMomentumX
    global ballMomentumY
    global rightRacket
    global leftRacket 
    global scoreP1
    global scoreP2

    ball.x = ball.x + ballMomentumX
    ball.y = ball.y + ballMomentumY

    if ball.y <= 0:
        ballMomentumY = random.randrange(2) + 4
    elif ball.y >= height - ball.height:
        ballMomentumY = random.randrange(2) - 5
    elif ball.colliderect(leftRacket):
        ballMomentumX = random.randrange(2) + 4
    elif ball.colliderect(rightRacket):
        ballMomentumX = random.randrange(2) - 5
    if ball.x < 25:
        scoreP1 = scoreP1 + 1
        pongReset()
        print("Player 1: " + str(scoreP1))
    if ball.x > 875:
        scoreP2 = scoreP2 + 1
        pongReset()
        print("Player 2: " + str(scoreP2))

def pongReset():
    global ball
    global ballMomentumX
    global ballMomentumY
    global rightRacket
    global leftRacket

    ballMomentumX = random.randrange(3) - 1
    ballMomentumY = random.randrange(3) - 1
    if ballMomentumX == 0:
        ballMomentumX = 1
    if ballMomentumY == 0:
        ballMomentumy = -1

    if ballMomentumX > 0:
        ballMomentumX = random.randrange(2) + 4
    else:
        ballMomentumX = random.randrange(2) - 5
    if ballMomentumY > 0:
        ballMomentumY = random.randrange(2) + 4
    else:
        ballMomentumY = random.randrange(2) - 5
    
    ball.x = 395
    ball.y = 295

    rightRacket.y = 275
    leftRacket.y = 275
    
def bot():
    global ballMomentumX
    global ballMomentumY
    global bMX
    global bMY
    global leftRacket
    global ball
    global botMove
    global bHitX, bHitY
    offset = 0
    if ballMomentumX < 0:
        if bMX != ballMomentumX or bMY != ballMomentumY:
            temp = (ball.x - bHitX) // ballMomentumX
            bHitY = math.sqrt(pow((ballMomentumY * temp) - ball.y + (ball.height / 2), 2))
            bMX = ballMomentumX
            bMY = ballMomentumY
            offset = random.randrange(90) - 45
            bHitY = offset + bHitY

        if leftRacket.y + (leftRacket.height / 2) > bHitY - 3 and leftRacket.y + (leftRacket.height / 2) > bHitY + 3 :
            botMove = 1
        elif leftRacket.y + (leftRacket.height / 2) < bHitY - 3 and leftRacket.y + (leftRacket.height / 2) < bHitY + 3:
            botMove = 2
        else:
            botMove = 0

def gameLoop(running, player1):
    global racketDmove
    global racketGmove
    global rightRacket
    global leftRacket

    clock = pygame.time.Clock()
    while running == True:
        clock.tick(60)
        if player1 == True:
            eventManager()
            playerUpdate(rightRacket, racketDmove)
            playerUpdate(leftRacket, botMove)
            bot()
            gameLogic()
            screenUpdate()
        else:
            eventManager()
            playerUpdate(rightRacket, racketDmove)
            playerUpdate(leftRacket, racketGmove)
            gameLogic()
            screenUpdate()

pongReset()
gameLoop(True, True)

pygame.quit()
