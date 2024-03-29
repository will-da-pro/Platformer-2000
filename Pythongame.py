import pygame
import time
import sys
from pygame import *
import playsound
import winsound
playerX = 0
playerY = 0
winHeight = 1000
winWidth = 1700
halfWinHeight = winHeight/2
halfWinWidth = winWidth/2
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
display = (winWidth,winHeight)

depth = 32
timer = pygame.time.Clock()
flags = 0
stage = 1
stageDelta = stage
gameRunning = True
pygame.init()

pygame.display.set_icon(pygame.image.load('assets/icon.png'))
pygame.display.set_caption('Platformer 2000')
screen = pygame.display.set_mode(display, flags, depth)
monospace = pygame.font.SysFont("monospace", 20)
def main(stage):
    stageDelta = stage
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sound.mp3")
    pygame.mixer.music.play()
    playerObj = playerClass(100, 550)
    buttonObjStart = buttonClass(green, 700, 50, 250, 100, "Click to play")
    buttonObjMenu = buttonClass(red, 2, 2, 250, 100, "Menu")
    platformGroup = pygame.sprite.Group()
    playerGroup = pygame.sprite.Group()
    backGround = Surface((winWidth, winHeight))
    backGround.convert()

    backGround.fill(Color("#69FFFF"))
    playing = False
    upKey = downKey = rightKey = leftKey = False

    platformList = []
    x = y = 0                                                                                                                    
    level = ["GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
             "P                                                                                                                         P                                                                                      P",
             "P                                                                                                                         P                                                                                      P",
             "P                                                                                                                         P                                                                                      P",
             "P                                                                                                                         P                                                                                      P",
             "P                                         GGG                                                                             P                                                                                      P",
             "P                                                                                                                 GGG     PGGGG                                                                                  P",
             "P                                                         GGGGGG                  GGG     G   GGGG                        P                                                                                      P",
             "P            GGGG           GGGGGG                                                                    GG                  P               GGGGGG                                                                 P", 
             "P        GGGG                                                             GGGG                                            P                                                                                      P",
             "P                                             GGGGGG                                                                      P                                                                                      P",
             "P                                                                                                                         P                                                                                      P",
             "PGGGGG                                                                                                                    P                                                                                      P",
             "PPPPPPG                                                                                                                   P                                                                                      P",
             "PPPPPPPG                                                                                                                  P                                                                                      P",
             "PPPPPPPPG                                                                                                                 P                                                                                      P",
             "PPPPPPPPPG                                                                                                                P                                                                                      P",]
    for row in level:
        for col in row:
            if col == "P":
                P = blockClass(x,y)
                platformGroup.add(P)
                platformList.append(P)
            if col == "G":
                G = blockClassGrass(x,y)
                platformGroup.add(G)
                platformList.append(G)

            x += 50
        y += 50
        x = 0
    totalLevelWidth = len(level[0])*50
    totalLevelHeight = len(level[0])*50
    cameraObj = cameraClass(complexCamera, totalLevelWidth, totalLevelHeight)
	
    playerGroup.add(playerObj)


                
    while gameRunning:
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                    
                    upKey = True
                if event.key == K_DOWN or event.key == K_s:
                    downKey = True
                if event.key == K_LEFT or event.key == K_a:
                    leftKey = True
                if event.key == K_RIGHT or event.key == K_d:
                    rightKey = True
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                    upKey = False
                if event.key == K_DOWN or event.key == K_s:
                    downKey = False
                if event.key == K_LEFT or event.key == K_a:
                    leftKey = False

                if event.key == K_RIGHT or event.key == K_d:
                    rightKey = False
        screen.blit(backGround,(0,0))


        if not playing:
            screen.blit(pygame.image.load('assets/startBack.png').convert_alpha(), (0, 0))
            buttonObjStart.draw(screen, 60, (0,0,0))
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttonObjStart.isOver(pos):
                        playing = True
                if event.type == pygame.MOUSEMOTION:
                    if buttonObjStart.isOver(pos):
                        buttonObjStart.color = (6, 96, 0)
                    else:
                        buttonObjStart.color = green
        if playing:
            

            cameraObj.update(playerObj)
            playerObj.update(upKey, downKey, rightKey, leftKey, platformList)
            for i in playerGroup:
                screen.blit(i.image, cameraObj.Apply(i))
            for x in platformGroup:
                screen.blit(x.image, cameraObj.Apply(x))
       
            text1 = monospace.render("(x, y)- "+ str(playerObj.rect.x/50)+ ", "+ str(playerObj.rect.y/50), 1, black)
            screen.blit(text1, (1400, 0))
            timer.tick(60)
            if playerObj.stageD == 2:
                backGround.fill(Color('#c2c5cc'))
        
##            buttonObjMenu.draw(screen, 60, (0, 0, 0))
##            for event in pygame.event.get():
##                pos = pygame.mouse.get_pos()
##                if event.type == pygame.MOUSEBUTTONDOWN:
##                    if buttonObjMenu.isOver(pos):
##                        pass
##                if event.type == pygame.MOUSEMOTION:
##                    if buttonObjMenu.isOver(pos):
##                        buttonObjMenu.color = (193, 0, 0)
##                    else:
##                        buttonObjMenu.color = red
        


        pygame.display.update()
class cameraClass(object):
    def __init__(self, cameraFunc, width, height):
        self.cameraFunc = cameraFunc
        self.state = Rect(0, 0, width, height)
    def Apply(self, target):
        return target.rect.move(self.state.topleft)
    def update(self, target):
        self.state = self.cameraFunc(self.state, target.rect)

def complexCamera(camera, targetRect):
    x, y, w, h = targetRect
    return Rect(halfWinWidth-x,halfWinHeight-y, w, h)
    
        
class entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class blockClass(entity):
    def __init__(self, x, y):
        entity.__init__(self)
        self.image = Surface((50, 50))
        self.image = (pygame.image.load('assets/stone.png').convert_alpha())
        self.image.convert()
        self.rect = Rect(x, y, 50, 50)
class blockClassGrass(entity):
    def __init__(self, x, y):
        entity.__init__(self)
        self.image = Surface((50, 50))
        self.image = (pygame.image.load('assets/stoneWithGrass.png').convert_alpha())
        self.image.convert()
        self.rect = Rect(x, y, 50, 50)
class buttonClass():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win, fontSize, outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', fontSize)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False    
class playerClass(entity):
    def __init__(self, x, y):
        entity.__init__(self)
        self.stageD = 1
        self.xvel = 0
        self.yvel = 0
        self.image = Surface((50, 100))
        self.image = (pygame.image.load('assets/player.png').convert_alpha())
        self.image.convert()
        self.rect = Rect(x, y, 50, 100)
        self.onGround = False
        
    def update(self, upKey, downKey, rightKey, leftKey, platforms):

        if upKey and self.onGround:
            self.yvel -= 17

        if rightKey:

            self.xvel += 0.5
        if leftKey:
            self.xvel -= 0.5
        if not(leftKey or rightKey):
            if self.xvel < 0:
                self.xvel += .5
            if self.xvel > 0:
                self.xvel -= .5
            if self.xvel == 0:
                self.xvel == 0
        if not(upKey):
            if self.yvel < 0:
                self.yvel += 0.5

            if self.yvel > 0:
                self.yvel -= 0.5
        
        if not self.onGround and self.yvel < 1000:
            self.yvel += 0.8
        if self.rect.y > 800:
            self.yvel = 0
            self.xvel = 0
            if (self.stageD == 1):
                self.rect.x = 150
                self.rect.y = 550
            if (self.stageD == 2):
                self.rect.x = 6250
                self.rect.y = 250
        if self.rect.x > 5750 and self.rect.x < 6100: 
            self.stageD = 2
            self.rect.x = 6250
            self.rect.y = 250

                
        self.rect.left += self.xvel
        self.collide(self.xvel, 0,  platforms)
        self.rect.top += self.yvel
        self.onGround = False
        self.collide(0, self.yvel, platforms)
        playerX = self.rect.x
        playerY = self.rect.y        
    def collide(self, xvelDelta, yvelDelta, platforms):
        for i in platforms:
            if pygame.sprite.collide_rect(self, i):
                if xvelDelta > 0:
                    self.xvel = 0
                    self.rect.right = i.rect.left
                if xvelDelta < 0:
                    self.rect.left = i.rect.right
                    self.xvel = 0
                if yvelDelta > 0:
                    self.rect.bottom = i.rect.top
                    self.yvel = 0
                    self.onGround = True
                if yvelDelta < 0:
                    self.yvel = 0
                    self.rect.top = i.rect.bottom
                
            

main(stage)
