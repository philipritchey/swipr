import tkinter as tk
from PIL import ImageTk, Image
import time
import os

w = tk.Tk()
ready = True

def show_img(uin = None):
    global w
    global panel

    w.title(str(uin))
    try:
        img = ImageTk.PhotoImage(Image.open(os.path.join('image',uin+'.jpeg')))
    except FileNotFoundError:
        img = ImageTk.PhotoImage(Image.open(os.path.join('image','notfound.png')))
    panel.image = img
    width = img.width()
    height = img.height()
    x,y=0,0
    w.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    panel.configure(image = img)
    w.update_idletasks()
    w.update()
    time.sleep(1)


def ready():
    global w
    global panel

    w.title('Ready')
    img = ImageTk.PhotoImage(Image.open(os.path.join('image','ready.png')))
    panel.image = img
    width = img.width()
    height = img.height()
    x,y=0,0
    w.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    panel.configure(image = img)
    w.update_idletasks()
    w.update()

def main():
    global w
    global panel

    panel = tk.Label(w)
    panel.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.YES)

    uin = "1";
    while uin > "0":
        ready()
        uin = input('uin: ')
        show_img(uin)



if __name__ == '__main__':
    main()

