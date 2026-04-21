from tkinter import *
from tkinter.ttk import Progressbar
import sys
from PIL import Image, ImageTk

root = Tk()
root.resizable(0,0)

width = 530
height = 430

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root.overrideredirect(1)
root.config(background= 'yellow')

exit_btn = Button(root,text = 'X',command = lambda: exit_wind(),font = ("yu gothic ui",13,'bold'), fg = 'black')
exit_btn.place(x = 0,y=0)

welcome_label = Label(root,text = 'Find an opponent...',font =("yu gothic ui",19,"bold"),bg = "yellow")
welcome_label.place(x = 140,y=15)

path = "C:\\Users\\user\\Downloads\\img23.png"
pil_image = Image.open(path)
resized_pil_image = pil_image.resize((200, 200))
image = ImageTk.PhotoImage(resized_pil_image)

bg_label = Label(root, image=image, bg='yellow', bd=0)
bg_label.image = image
bg_label.place(x=148, y=100)

progress_label = Label(root,text = "Please Wait...",font = ("yu gothic ui",13,"bold") ,bg = "yellow")
progress_label.place(x = 190 , y = 320)

progress = Progressbar(root,orient = HORIZONTAL,length = 500,mode = "determinate")
progress.place(x = 15, y =350)




def exit_wind():
    sys.exit(root.destroy())


i = 0

def load():
    global i

    if i <= 10:
        txt = 'Please Wait...' + (str(10*i) + '%')
        progress_label.config(text = txt)
        progress_label.after(1000,load)
        progress['value'] = 10*i
        i += 1

load()
root.mainloop()