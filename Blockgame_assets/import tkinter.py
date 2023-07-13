import tkinter
root = tkinter.Tk()
root.title = ("test")
canvas = tkinter.Canvas(width = 320, height = 240, bg = "white")
canvas.pack()
img = tkinter.PhotoImage(file = "brick.png")
canvas.create_image(1,1,image = img)
root.mainloop()