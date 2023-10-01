import sys
import numpy
import pygame
from pygame.locals import *

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
    elif stage == 2:
        block = [
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,1,0,1,0,1],
            [1,1,1,0,1,1,0,1,1,1],
            [1,1,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1]
        ]
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
    def update(self):
        self.rect.centerx = min(180,self.rect.centerx)
        self.rect.centerx= max(0,self.rect.centerx)
        self.rect.clamp_ip(SIZE)
    def move(self,x):
        self.rect.centerx+=x


def main():
    SCORE=0
    STAGE=1
    STATUS=0
    TIMER=0
    pygame.init()
    screen = pygame.display.set_mode(SIZE.size)
    BG_IMG = pygame.image.load("background.png")
    BLOCK_IMG =pygame.image.load("brick.png")
    TITLE_IMG = pygame.image.load("title.png")
    PLAYER_IMG= pygame.image.load("player.png")
    FONT=pygame.font.SysFont("Terminal", 25)
    group = pygame.sprite.RenderUpdates()
    blocks = pygame.sprite.Group()
    Player.containers=group
    Block.containers = group, blocks
    

    
    player=Player(PLAYER_IMG)
    info = Info(215,20)

    clock = pygame.time.Clock()
    while 1:
        pressed_key = pygame.key.get_pressed()
        clock.tick(20)
        screen.blit(BG_IMG, (0, 0))

        if STATUS==0:
            screen.blit(TITLE_IMG,(30,30))
            tutorial=FONT.render("[Space]to start",True,(0,0,0))
            screen.blit(tutorial,(30,150))
            if pressed_key[K_SPACE]:
                STATUS=1
                TIMER=0
                for y,v in enumerate(set_blocklist(1)):
                    for x,w in enumerate(v):
                        if w:
                            Block(BLOCK_IMG, x*20, y*8)
        elif STATUS==1:
            TIMER+=1
            if TIMER<15:
                tutorial=FONT.render("START:"+str(15-TIMER),True,(0,0,0))
                screen.blit(tutorial,(30,100))
            else:#ゲーム is here
                # 変更ポイント
                if pressed_key[K_LEFT]:
                    player.move(-1)
                #変更ポイント
                if pressed_key[K_RIGHT]:
                    player.move(1)

                info.draw(screen)
                #info.add_score(1)
                
                group.update()
                group.draw(screen)
            

        ## ここからおまじない
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
        ### こちらがディスプレイ表示用
        pixArray = pygame.PixelArray(screen)
        array = numpy.uint8(pixArray)
        #print(array.size)
        del pixArray
        ### ここまで
if __name__ == "__main__":
    main()