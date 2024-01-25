import pygame, sys, random
#instead of calling pygame.math i can call Vector2
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.newBlock = False
        
        self.headUp = pygame.image.load('snake/head_up.png').convert_alpha()
        self.headDown = pygame.image.load('snake/head_down.png').convert_alpha()
        self.headLeft = pygame.image.load('snake/head_left.png').convert_alpha()
        self.headRight = pygame.image.load('snake/head_right.png').convert_alpha()

        self.bodyBl = pygame.image.load('snake/body_bottomleft.png').convert_alpha()
        self.bodyBr = pygame.image.load('snake/body_bottomright.png').convert_alpha()
        self.bodyTl = pygame.image.load('snake/body_topleft.png').convert_alpha()
        self.bodyTr = pygame.image.load('snake/body_topright.png').convert_alpha()

        self.bodyV = pygame.image.load('snake/body_vertical.png').convert_alpha()
        self.bodyH = pygame.image.load('snake/body_horizontal.png').convert_alpha()

        self.tailUp = pygame.image.load('snake/tail_up.png').convert_alpha()
        self.tailDown = pygame.image.load('snake/tail_down.png').convert_alpha()
        self.tailRight = pygame.image.load('snake/tail_right.png').convert_alpha()
        self.tailLeft = pygame.image.load('snake/tail_left.png').convert_alpha()
        

    def drawSnake(self):
        self.updateHead()
        self.updateTail()

        for index, block in enumerate(self.body):
            xPos = int(block.x*cellSize)
            yPos = int(block.y*cellSize)
            snakeRect = pygame.Rect(xPos,yPos,cellSize,cellSize)

            if index == 0:
                screen.blit(self.head, snakeRect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snakeRect)
            else:
                previousBlock = self.body[index + 1] - block
                nextBlock = self.body[index - 1] - block
                if previousBlock.x == nextBlock.x:
                    screen.blit(self.bodyV, snakeRect)
                elif previousBlock.y == nextBlock.y:
                    screen.blit(self.bodyH, snakeRect)
                else:
                    if previousBlock.x == -1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == -1:
                        screen.blit(self.bodyTl, snakeRect)
                    elif previousBlock.x == -1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == -1:
                        screen.blit(self.bodyBl, snakeRect)
                    elif previousBlock.x == 1 and nextBlock.y == -1 or previousBlock.y == -1 and nextBlock.x == 1:
                        screen.blit(self.bodyTr, snakeRect)
                    elif previousBlock.x == 1 and nextBlock.y == 1 or previousBlock.y == 1 and nextBlock.x == 1:
                        screen.blit(self.bodyBr, snakeRect)
    
    def updateHead(self):
        headRelation = self.body[1] - self.body[0]
        if headRelation == Vector2(1,0): self.head = self.headLeft
        elif headRelation == Vector2(-1,0): self.head = self.headRight
        elif headRelation == Vector2(0,1): self.head = self.headUp
        elif headRelation == Vector2(0,-1): self.head = self.headDown

    def updateTail(self):
        tailRelation = self.body[-2] - self.body[-1]
        if tailRelation == Vector2(1,0): self.tail = self.tailLeft
        elif tailRelation == Vector2(-1,0): self.tail = self.tailRight
        elif tailRelation == Vector2(0,1): self.tail = self.tailUp
        elif tailRelation == Vector2(0,-1): self.tail = self.tailDown

    def moveSnake(self):
        if self.newBlock == True:
            bodyCopy = self.body[:]
            bodyCopy.insert(0,bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]
            self.newBlock = False
        else:
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0,bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True 

class FRUIT:
    def __init__ (self):
        self.randomize()

    def drawFruit(self):
        #create a rectangle
        #to code a rect you need pygame.Rect(x,y,w,h)
        fruitRect = pygame.Rect(int(self.pos.x*cellSize),int(self.pos.y*cellSize),cellSize,cellSize)
        screen.blit(apple,fruitRect)

        #draw it
        #to draw a rect you need pygame.draw.rect(surface, color,rect)
        #HERERERERERE
        #pygame.draw.rect(screen,(126,166,114),fruitRect)
    
    def randomize(self):
        self.x = random.randint(0, cellNum - 1)
        self.y = random.randint(0, cellNum - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkFail()

    def drawElements(self):
        self.drawGrass()
        self.fruit.drawFruit()
        self.snake.drawSnake()
        self.drawScore()

        #bug 
        

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.addBlock()

    def checkFail(self):
        #if snake hit walls
        if not 0 <= self.snake.body[0].x < cellNum or not 0 <= self.snake.body[0].y < cellNum:
            self.gameOver()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        pygame.quit()
        sys.exit()

    def drawGrass(self):
        grassColor = (167,209,61)

        for row in range(cellNum):
            if row % 2 == 0:
                for col in range(cellNum):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col * cellSize, row*cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)

                else:
                  if row % 2 == 0:
                    for col in range(cellNum):
                        if col % 2 == 0:
                            grassRect = pygame.Rect(col * cellSize, row*cellSize, cellSize, cellSize)
                            pygame.draw.rect(screen, grassColor, grassRect) 

    def drawScore(self):
        scoreText = str (len(self.snake.body) - 3)
        scoreSurface = gameFont.render(scoreText,True,(55,74,12))
        scoreX = int(cellSize * cellNum - 60)
        scoreY = int(cellSize * cellNum - 40)
        scoreRect = scoreSurface.get_rect(center = (scoreX, scoreY))
        screen.blit(scoreSurface, scoreRect)

#starts the pygame 
pygame.init()

cellSize = 40
cellNum = 20
#makes the actual screen
screen = pygame.display.set_mode((cellNum*cellSize,cellNum*cellSize)) 

#limits how many times the loop will run
clock = pygame.time.Clock()

#import image
apple = pygame.image.load('snake/apple.png').convert_alpha()

gameFont = pygame.font.Font(None, 25)
#create a rectangle you need pygame.Rect(x,y,w,h) or inclose a shape with it using name of surface.get_rect()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
mainGame = MAIN()

# main game loop
while True:

    # make sure that code can close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # moves snake right
        if event.type == SCREEN_UPDATE:
            mainGame.update()

        # moves snake depending on user input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainGame.snake.direction.y != 1:
                    mainGame.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if mainGame.snake.direction.y != -1:
                    mainGame.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if mainGame.snake.direction.x != 1:
                    mainGame.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if mainGame.snake.direction.x != -1:
                    mainGame.snake.direction = Vector2(1,0)

    #Two ways to make color, either use pygame.Color('name of color') or use rgb
    screen.fill((175,215,70))
    mainGame.drawElements()
    
    #draw all elements
    pygame.display.update()

    #frame rate
    clock.tick(70) 