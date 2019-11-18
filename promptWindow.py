from tkinter import *


def promptWindow(title,message):
    promptScreen = Tk()
    promptScreen.title(title)

    Label(promptScreen, text=message).pack()
    Button(promptScreen,text="Okay", command=promptScreen.destroy).pack()