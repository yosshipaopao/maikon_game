import math
import random
import numpy
import pygame
from pygame.locals import *
from PIL import Image
"""
from busio import SPI
from board import SCK, MOSI, MISO, D8, D18, D23, D24, D2, D3,D20,D21,D19,D26
from digitalio import DigitalInOut, Direction,Pull
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display.ili9341 import ILI9341

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
"""


#いろいろ
stage = 0
block =[[]]
SIZE=Rect(0, 0, 320, 240)

font_list = []
for x in pygame.font.get_fonts():
    font_list.append(x)

def set_blocklist(stage):
    global block
    if stage %2 == 0:
        block = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,1,0,1,0,1],
            [1,1,1,0,1,1,0,1,1,1],
            [1,1,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]
    elif stage %2== 1:
        block = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]
        #block=[[0]*10 for _ in range(5)]
        #block[0][5]=1
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
        self.sysfont = pygame.font.SysFont(font_list[round(random.uniform(0,len(font_list)))], 15)
        self.score = 0
        self.stage=1
        (self.x, self.y) = (x, y)
    def draw(self, screen):
        score = self.sysfont.render("SCORE:"+str(self.score), True, (0,0,0))
        screen.blit(score, (self.x, self.y))
        stage = self.sysfont.render("STAGE:"+str(self.stage), True, (0,0,0))
        screen.blit(stage, (self.x, self.y+20))
        demo = self.sysfont.render("DEMO PLAY", True, (0,0,0))
        screen.blit(demo, (self.x, self.y+160))
    def add_score(self, x):
        self.score += x
        self.score%=999
    def add_stage(self):
        self.stage += 1
        self.sysfont = pygame.font.SysFont(font_list[round(random.uniform(0,len(font_list)))], 15)
        self.stage%=99
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
        while abs(90-radian)<10:
            radian+=random.uniform(-30,30)
        angle = math.radians(radian)
        self.dx = self.speed * math.cos(angle)
        self.dy = -self.speed * math.sin(angle)
        self.update = self.move
    def move(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        if -1<self.dx<1:
            if self.dx > 0:
                self.dx += 0.1
            else:
                self.dx -= 0.1
        if self.rect.left < SIZE.left+1:
            self.rect.left = SIZE.left+1
            self.dx = -self.dx
        if self.rect.right > SIZE.right-120:
            self.rect.right = SIZE.right-120
            self.dx = -self.dx
        if self.rect.top < SIZE.top:
            self.rect.top = SIZE.top
            self.dy = -self.dy
        if self.rect.colliderect(self.player.rect) and self.dy > 0:
            angle=math.acos(self.dx/self.speed)
            angle+=random.random()/5
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
    #LED_PIN.value=True
    pygame.init()
    screen = pygame.display.set_mode(SIZE.size)
    BG_IMG = pygame.image.load("background.png")
    BLOCK_IMG =pygame.image.load("brick.png")
    PLAYER_IMG= pygame.image.load("player.png")
    BALL_IMG= pygame.image.load("ball.png")
    group = pygame.sprite.RenderUpdates()
    blocks = pygame.sprite.Group()
    Player.containers=group
    Ball.containers=group
    Block.containers = group, blocks
    
    player=Player(PLAYER_IMG)
    info = Info(215,20)
    ball=Ball(BALL_IMG,player,blocks,info,5, 135, 45)

    clock = pygame.time.Clock()
    
    for y,v in enumerate(set_blocklist(info.stage)):
            for x,w in enumerate(v):
                if w:
                    Block(BLOCK_IMG, x*20, y*8)
    player.start()
    ball.start()
    while 1:
        clock.tick(20)#fps
        screen.blit(BG_IMG, (0, 0))

        player.rect.centerx=ball.rect.centerx

        info.draw(screen)
        
        group.update()
        group.draw(screen)
        if len(blocks)==0:
            player.start()
            ball.start()
            info.add_stage()
            for y,v in enumerate(set_blocklist(info.stage)):
                for x,w in enumerate(v):
                    if w:
                        Block(BLOCK_IMG, x*20, y*8)
                
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
        #display.image(img)
        del pixArray
        del array
        ### ここまで
if __name__ == "__main__":
    main()