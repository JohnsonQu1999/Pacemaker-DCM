from tkinter import *


def promptWindow(title,message):
	promptScreen = Tk()
	promptScreen.title(title)

	Label(promptScreen, text=message).pack()
	Button(promptScreen,text="Okay", command=promptScreen.destroy).pack()

def promptWindow2(title,message1,message2):
	promptScreen = Tk()
	promptScreen.title(title)

	Label(promptScreen, text=message1).pack()
	Label(promptScreen, text=message2).pack()
	Button(promptScreen,text="Okay", command=promptScreen.destroy).pack()

def promptWindow3(title,message1,message2,message3):
	promptScreen = Tk()
	promptScreen.title(title)

	Label(promptScreen, text=message1).pack()
	Label(promptScreen, text=message2).pack()
	Label(promptScreen, text=message3).pack()
	Button(promptScreen,text="Okay", command=promptScreen.destroy).pack()

def promptWindow4(title,message1,message2,message3,message4):
	promptScreen = Tk()
	promptScreen.title(title)

	Label(promptScreen, text=message1).pack()
	Label(promptScreen, text=message2).pack()
	Label(promptScreen, text=message3).pack()
	Label(promptScreen, text=message4).pack()
	Button(promptScreen,text="Okay", command=promptScreen.destroy).pack()

	# Material order January 1st
	# Design review first week of January
	# Packaging review first week of January - needs to be 100% done by end of December
	# Optimization review
	# Start machining first week back
