from tkinter import *
from tkinter import ttk

class DCM:

	def __init__(self):
		self.main_screen = Tk()   # create a GUI window 
		self.main_screen.geometry("300x250") # set the configuration of GUI window 
		

		self.createWelcome()
		#self.reg_screen()
		self.main_screen.mainloop()

	def createWelcome(self):
		self.main_screen.title("Welcome") # set the title of GUI window
		self.f = Frame(self.main_screen)
		self.f.pack()

		# create a Form label 
		L1 = Label(self.f,text="Choose Login Or Register", bg="blue", width="300", height="2", font=("Calibri", 13))
		L1.pack() 
		Label(self.f,text="").pack() 
		 
		# create Login Button 
		LoginBtn = Button(self.f,text="Login", height="2", width="30")
		LoginBtn.pack() 
		Label(self.f,text="").pack() 
		 
		# create a register button
		RegisterBtn = Button(self.f,text="Register", height="2", width="30", command=lambda:self.reg_screen())
		RegisterBtn.pack()
		#RegisterBtn.config()


	def reg_screen(self):
		regscreen = Tk()
		regscreen.title("Register")
		self.main_screen.destroy()
		regscreen.mainloop()


go = DCM()



