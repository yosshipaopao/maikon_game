import math
import random
import numpy
import pygame
from pygame.locals import *
from PIL import Image
from busio import SPI
from board import SCK, MOSI, MISO, D8, D18, D23, D24, D2, D3,D20,D21,D19,D26
from digitalio import DigitalInOut, Direction,Pull
from analogio import AnalogIn
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display.ili9341 import ILI9341
import RPi.GPIO as GPIO

GPIO.cleanup()
CS_PIN    = DigitalInOut(D8)
LED_PIN   = DigitalInOut(D18)
RESET_PIN = DigitalInOut(D23)
DC_PIN    = DigitalInOut(D24)
LED_PIN.direction = Direction.OUTPUT

SWITCH_PIN = DigitalInOut(D3)
SWITCH_PIN.direction = Direction.INPUT

UDP_SHUTDOWN_SH_PORT=50001

spi = SPI(clock=SCK, MOSI=MOSI, MISO=MISO)
display = ILI9341(
    spi,
    cs = CS_PIN,
    dc = DC_PIN,
    rst = RESET_PIN,
    width = 240,
    height = 320,
    rotation = 90,
    
    baudrate=24000000)

GPIO.setmode(GPIO.BCM)
CTRL_T=DigitalInOut(D20)
CTRL_L=DigitalInOut(D21)

#GPIO.setup(20, GPIO.IN)
#GPIO.setup(21, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(26, GPIO.IN)

#いろいろ
stage = 0
block =[[]]
SIZE=Rect(0, 0, 320, 240)



def set_blocklist(stage):
    global block
    if stage == 1:
        
        block = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,1,0,1,0,1],
            [1,1,1,0,1,1,0,1,1,1],
            [1,1,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]
        """
        # for debug
        block = [
            [0,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
        ]"""
    elif stage == 2:
        block = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,1,0,1,0,1],
            [1,1,1,0,1,1,0,1,1,1],
            [1,1,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]
        """
        # for debug
        block = [
            [0,0,0,0,1,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
        ]
        """
    return block
class Block(pygame.sprite.Sprite):
    def __init__(self, image, x,y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = SIZE.top + x
        self.rect.top = SIZE.top + y + 10
class Info():
    def __init__(self, x, y):
        self.sysfont = pygame.font.SysFont("Terminal", 25)
        self.score = 0
        self.stage=1
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        score = self.sysfont.render("SCORE:"+str(self.score), True, (0,0,0))
        screen.blit(score, (self.x, self.y))
        stage = self.sysfont.render("STAGE:"+str(self.stage), True, (0,0,0))
        screen.blit(stage, (self.x, self.y+20))
    def add_score(self, x):
        self.score += x
    def add_stage(self):
        self.stage += 1
class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = SIZE.bottom -20
        self.rect.centerx=90
    def start(self):
        self.rect.centerx=90
    def update(self):
        self.rect.centerx = min(180,self.rect.centerx)
        self.rect.centerx= max(0,self.rect.centerx)
        self.rect.clamp_ip(SIZE)
    def move(self,x):
        self.rect.centerx+=x
class Ball(pygame.sprite.Sprite):
    def __init__(self, image, player, blocks,info, speed, angle_left, angle_right):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.dx = self.dy = 0
        self.player = player
        self.info=info
        self.blocks = blocks
        self.update = self.start
        self.speed = speed
        self.angle_left = angle_left
        self.angle_right = angle_right
    def start(self):
        self.rect.centerx = self.player.rect.centerx
        self.rect.bottom = self.player.rect.top
        radian=random.uniform(60,120)
        angle = math.radians(radian)
        self.dx = self.speed * math.cos(angle)
        self.dy = -self.speed * math.sin(angle)
        self.update = self.move
    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
        if self.rect.left < SIZE.left:
            self.rect.left = SIZE.left
            self.dx = -self.dx
        if self.rect.right > SIZE.right-120:
            self.rect.right = SIZE.right-120
            self.dx = -self.dx
        if self.rect.top < SIZE.top:
            self.rect.top = SIZE.top
            self.dy = -self.dy
        if self.rect.colliderect(self.player.rect) and self.dy > 0:
            (x1, y1) = (self.player.rect.left - self.rect.width, self.angle_left)
            (x2, y2) = (self.player.rect.right, self.angle_right)
            x = self.rect.left
            y = (float(y2-y1)/(x2-x1)) * (x - x1) + y1
            angle = math.radians(y)
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)
        if self.rect.top > SIZE.bottom:#失敗時
                self.update = self.start
        
        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:
            oldrect = self.rect
            for block in blocks_collided:
                # ボールが左から衝突
                if oldrect.left < block.rect.left < oldrect.right < block.rect.right:
                    self.rect.right = block.rect.left
                    self.dx = -self.dx
                # ボールが右から衝突
                if block.rect.left < oldrect.left < block.rect.right < oldrect.right:
                    self.rect.left = block.rect.right
                    self.dx = -self.dx
                # ボールが上から衝突
                if oldrect.top < block.rect.top < oldrect.bottom < block.rect.bottom:
                    self.rect.bottom = block.rect.top
                    self.dy = -self.dy
                # ボールが下から衝突
                if block.rect.top < oldrect.top < block.rect.bottom < oldrect.bottom:
                    self.rect.top = block.rect.bottom
                    self.dy = -self.dy
                self.info.add_score(1)
def main():
    LED_PIN.value=True
    STATUS=0
    TIMER=0
    pygame.init()
    screen = pygame.display.set_mode(SIZE.size)
    BG_IMG = pygame.image.load("background.png")
    BLOCK_IMG =pygame.image.load("brick.png")
    TITLE_IMG = pygame.image.load("title.png")
    PLAYER_IMG= pygame.image.load("player.png")
    BALL_IMG= pygame.image.load("ball.png")
    FONT=pygame.font.SysFont("Terminal", 25)
    group = pygame.sprite.RenderUpdates()
    blocks = pygame.sprite.Group()
    Player.containers=group
    Ball.containers=group
    Block.containers = group, blocks
    

    
    player=Player(PLAYER_IMG)
    info = Info(215,20)
    ball=Ball(BALL_IMG,player,blocks,info,5, 135, 45)

    clock = pygame.time.Clock()
    A_BTN_CNT=0
    B_BTN_CNT=0

    while 1:
        clock.tick(20)#fps
        screen.blit(BG_IMG, (0, 0))
        A_BTN=GPIO.input(19)==1
        B_BTN=GPIO.input(26)==1
        if A_BTN:
            A_BTN_CNT+=1
        else:
            A_BTN_CNT=0
        
        if B_BTN:
            B_BTN_CNT+=1
        else:
            B_BTN_CNT=0
        

        if STATUS==0:
            screen.blit(TITLE_IMG,(30,30))
            tutorial=FONT.render("[A]to start",True,(0,0,0))
            screen.blit(tutorial,(30,150))
            #変更ポイント
            if A_BTN_CNT>5:
                STATUS=1
                TIMER=0
        
        elif STATUS==1:
            if TIMER==0:
                player.start()
                ball.start()
                for y,v in enumerate(set_blocklist(info.stage)):
                    for x,w in enumerate(v):
                        if w:
                            Block(BLOCK_IMG, x*20, y*8)
            TIMER+=1
            if TIMER<15:
                tutorial=FONT.render("START:"+str(15-TIMER),True,(0,0,0))
                screen.blit(tutorial,(30,100))
            else:#ゲーム is here
                # 変更ポイント
                if B_BTN:
                    player.move(-5)
                #変更ポイント
                if A_BTN:
                    player.move(5)

                info.draw(screen)
                
                group.update()
                group.draw(screen)
                if len(blocks)==0:
                    info.add_stage()
                    STATUS=3
                    TIMER=0
        elif STATUS==3:
            TIMER+=1
            if TIMER<15:
                tutorial=FONT.render("STAGE CLEAR",True,(0,0,0))
                screen.blit(tutorial,(30,50))
            else:
                tutorial=FONT.render("[A] to next",True,(0,0,0))
                screen.blit(tutorial,(30,50))
                tutorial=FONT.render("[B] to title",True,(0,0,0))
                screen.blit(tutorial,(30,100))
                if A_BTN_CNT>5:
                    STATUS=1
                    TIMER=0
                if B_BTN_CNT>5:
                    info.score=0
                    info.stage=1
                    STATUS=0
        
        print(GPIO.input(19),GPIO.input(26))
        ## ここからおまじない
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit()
            
        ### こちらがディスプレイ表示用
        pixArray = pygame.surfarray.pixels3d(screen)
        array = numpy.fliplr(numpy.rot90(numpy.uint8(pixArray),-1))
        #array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(array)
        #img.save("screen.png")
        display.image(img)
        del pixArray
        del array
        ### ここまで
if __name__ == "__main__":
    main()