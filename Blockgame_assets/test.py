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
        self.rect.top = SIZE.top + y



def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE.size)
    bg = pygame.image.load("background.png")
    block =pygame.image.load("brick.png")
    
    group = pygame.sprite.RenderUpdates()
    blocks = pygame.sprite.Group()
    Block.containers = group, blocks
    
    for y,v in enumerate(set_blocklist(1)):
            for x,w in enumerate(v):
                if w:
                    Block(block, x*20, y*8)
    
    clock = pygame.time.Clock()
    while 1:
        clock.tick(20)
        screen.blit(bg, (0, 0))
        
        group.update()
        group.draw(screen)
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        pixArray = pygame.PixelArray(screen)
        array = numpy.uint8(pixArray)
        #print(array.size)
        del pixArray
if __name__ == "__main__":
    main()