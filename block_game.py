import tkinter
import random

FNT = ("Time New Roman")

key = ""

keyoff = False
idx = 0
tmr = 0
stage = 0
score = 0
bar_x = 0
bar_y = 540
ball_x = 0
ball_y = 0
ball_xp = 0
ball_yp = 0
is_clr = True

block = []
for i in range(5):
    block.append([1]*10)
for i in range(10):
    block.append([0]*10)

def key_down(e):
    global key
    key = e.keysym

def key_up(e):
    global keyoff
    keyoff = True

def draw_block():
    global is_clr
    is_clr = True
    cvs.delete("BG")
    for y in range(15):
        for x in range(10):
            gx = x*80
            gy = y*40
            if block[y][x] == 1:
                cvs.create_rectangle(gx+1, gy+4, gx+79,gy+32, fill = block.color(x,y), width = 0, tag = "BG")
                is_clr = False
    cvs.create_text(200, 20, text = "STAGE" + str(stage), fill = "white", font = FNT, tag = "BG")
    cvs.create_text(600, 20, text = "SCORE" + str(score), fill = "white", dont = FNT, tag = "BG")

def block_color(x,y): #format()で16新数に変換可
    col = "#{0:x}{1:x}{2:x}".format(15-x-int(y/3), x+1, y*3+3)
    return col

def draw_bar():
    cvs.delete("BAR")
    cvs.create_rectangle(bar_x-80, bar_y-12, bar_x+80, bar_y+12, fill="silver", width = 0,tag = "BAR")
    cvs.create_rectangle(bar_x-78, bsr_y-12, bar_x+78, bar_y+12, fill = "white", width = 0, tag = "BAR")

def move_bar():
    global bar_x
    if key == "Left" and bar_x > 80:
        bar_x = bar_x-40
    if key == "Right" and bar_x < 720:
        bar_x = bar_x + 40
    
def draw_ball():
    cvs.delete("BALL")
    cvs.create_oval(ball_x-20, ball_y-20, ball_x+20, ball_y+20, fill = "gold",outline = "orange", width = 2, tag = "BALL")
    cvs.create_oval()