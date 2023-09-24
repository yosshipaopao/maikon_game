import tkinter
import random

FNT = ("Terminal", 10, "normal")



key = ""

keyoff = False
idx = 0
tmr = 0
stage = 0
score = 0
bar_x = 0
bar_y =200
ball_x = 0
ball_y = 0
ball_xp = 0
ball_yp = 0
is_clr = True
maxstage = 2
block = []

def set_blocklist():
    global block
    if stage == 1:
        block = [
            [0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,1,0,1,0,1],
            [1,1,1,0,1,1,0,1,1,1],
            [1,1,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
            #10*27
        ]
    elif stage == 2:
        block = [
            [0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,1,1,0,1,0,1],
            [1,1,1,0,1,1,0,1,1,1],
            [1,1,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
            #10*27
        ]

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
    for y in range(24):
        for x in range(10):
            gx = x*20
            gy = y*8
            if block[y][x] == 1:
                cvs.create_image(gx+11, gy+0, image = blick, tag = "BG")
                is_clr = False
    cvs.create_text(230, 20, text = "STAGE: " + str(stage), fill = "white", font = FNT, tag = "BG")
    cvs.create_text(250, 40, text = "SCORE: " + str(score), fill = "white", font = FNT, tag = "BG")

                
def draw_bar():
    cvs.coords("BAR", bar_x, bar_y)

def move_bar():
    global bar_x
    if key == "Left" and bar_x > 25:
        bar_x = bar_x-5
    if key == "Right" and bar_x < 180:
        bar_x = bar_x+5

def draw_ball():
    cvs.coords("BALL", ball_x, ball_y)

def move_ball():
    global idx, tmr, score, ball_x, ball_y, ball_xp, ball_yp
    ball_x = ball_x + ball_xp
    if ball_x < 3:
        ball_x = 3
        ball_xp = -ball_xp
    if ball_x > 197:
        ball_x = 197
        ball_xp = -ball_xp
    x = int( ball_x/20)
    y = int(ball_y/8)
    if ball_y <= 190:
        if block[y][x] == 1:
            block[y][x] = 0
            ball_xp = -ball_xp
            score = score+10

    ball_y = ball_y + ball_yp
    if ball_y >= 240:
        idx = 2
        tmr = 0
        return
    if ball_y < 3:
        ball_y = 3
        ball_yp = -ball_yp
    x = int(ball_x/20)
    y = int(ball_y/8)
    if ball_y <= 190:
        if block[y][x] == 1:
            block[y][x] = 0
            ball_yp = -ball_yp
            score = score+10

    if bar_y-3 <= ball_y and ball_y <= bar_y+3:
        if bar_x-16 <= ball_x and ball_x <= bar_x+16:
            ball_yp = -3
            score = score+1
        elif bar_x-28 <= ball_x and ball_x <= bar_x-16:
            ball_yp = -3
            if key == "Left":
                ball_xp = random.randint(-4,-3)
            else:
                ball_xp = random.randint(-4,-2)
            score = score+1
        elif bar_x+16 <= ball_x and ball_x <= bar_x+28:
            ball_yp = -3
            if key == "Right":
                ball_xp = random.randint(3,4)
            else:
                ball_xp = random.randint(1,4)
            score = score+1

def main_proc():
    global key,keyoff
    global idx, tmr, stage, score
    global bar_x, ball_x, ball_y, ball_xp, ball_yp
    if idx == 0:
        if tmr == 0:
            tmr = tmr+1
            stage = 1
            score = 0
            cvs.delete("BAR","BALL","BG")
            cvs.create_image(100, 100, image = title, tag = "TXT")
            cvs. create_text(100,140, text = "[Space]to start", fill = "white", font = FNT, tag = "TXT")
            ball_x = 20
            ball_y = 120
            ball_xp = 5
            ball_yp = 5
            bar_x = 100
        if key == "space":
            cvs.delete("TXT")
            set_blocklist()
            tmr = 0
            idx = 1

    elif idx == 1:
        tmr = tmr+1
        if tmr == 1:
            ball_x = 20
            ball_y = 120
            ball_xp = 3
            ball_yp = 3
            bar_x = 100
            cvs.delete("BALL","BAR")
            cvs.create_image(bar_x, bar_y, image = bar, tag = "BAR")
            cvs.create_image(ball_x, ball_y, image = ball, tag = "BALL")
            cvs.create_text(100, 100, text = "START", fill = "white", font = "FNT", tag = "TEXT")
        if tmr == 15:
            cvs.delete("TEXT")
        if tmr >= 15:
            move_ball()
            move_bar()
            draw_block()
            draw_ball()
            draw_bar()
            if is_clr == True:
                idx = 3
                tmr = 0
    elif idx == 2:
        tmr = tmr+1
        if tmr == 1:
            cvs.create_text(100, 120, text = "GAME OVER", fill = "white", font = FNT, tag = "TXT")
        if tmr == 15:
            cvs.create_text(50, 150, text = "[R]Replay", fill = "white", font = FNT, tag = "TXT")
            cvs.create_text(150, 150, text = "[B]Back to title", fill = "white", font = FNT, tag = "TXT")
        if key == "r":
            cvs.delete("TXT")
            idx = 1
            tmr = 0
        if key =="b":
            cvs.delete("TXT")
            idx = 0
            tmr = 0
    elif idx == 3:
        tmr = tmr+1
        if tmr == 1:
            cvs.create_text(100, 120, text = "STAGE CLEAR", fill = "white", font = FNT, tag = "TXT")
        if tmr == 15:
            cvs.create_text(50, 150, text = "[Space]to next", fill = "white", font = FNT, tag = "TXT")
            cvs.create_text(150, 150, text = "[B]Back to title", fill = "white", font = FNT, tag = "TXT")
        if key == "space":
            if stage == maxstage:
                cvs.delete("TXT")
                cvs.create_text(100, 200, text = "All stage creared", fill = "white", font = FNT, tag = "TXT")
            else:
                stage = stage+1
                cvs.delete("TXT")
                set_blocklist()
                idx = 1
                tmr = 0
        if key =="b":
            cvs.delete("TXT")
            idx = 0
            tmr = 0

    if keyoff == True:
        keyoff = False
        if key != "":
            key = ""

    root.after(50,main_proc)

root = tkinter.Tk()
root.title("Blick.")
root.resizable (False,False)
root.bind("<Key>", key_down)
root.bind("<KeyRelease>", key_up)
cvs = tkinter.Canvas(root, width = 320, height = 240, bg = "black")
cvs.pack()
bg = tkinter.PhotoImage(file = "background.png")
title = tkinter.PhotoImage(file = "title.png")
bar = tkinter.PhotoImage(file = "player.png")
ball = tkinter.PhotoImage(file = "ball.png")
blick = tkinter.PhotoImage(file = "brick.png")
#img_block = [
#    None,
#    tkinter.PhotoImage(file = "brick.png")
#]
cvs.create_image(162, 122, image = bg, tag = "BASE")
main_proc()
root.mainloop()