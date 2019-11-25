from promptWindow import *
import csv


class Register():
	def __init__(self, screen):
		self.screen = screen
		self.reg = Frame(screen)


	def checkUsername(self, userstr):
		if (len(userstr.get())==0):
			noUsername(self)
			return 0
		else: 
			return 1

	def checkPasswords(self, pw1str, pw2str):
		if (pw1str.get() != pw2str.get()):
			differentPassword(self)
			return 0

		elif (len(pw1str.get())<5 or len(pw2str.get())<5):
			self.shortPassword(self)
			return 0
		else:
			#self.adduser(self.userstr.get(),self.pw1str.get())
			return 1


	#Registration prompts
	def differentPassword(self): #passwords don't match when registering
		promptWindow("Error", "Passwords do not match, please try again")

	def repeatUser(self): #user already exists
		promptWindow("Error", "An account with this username already exists")

	def successfulRegistration(self):
		promptWindow("Success", "Registration Successful. \n Redirecting to Login")

	def maxUsers(self): #double check about this#
		promptWindow("Error", "Maximum of 10 users are already registered")

	def shortPassword(self):  # must be minimum of five characters
		promptWindow("Error", "Password must be at least 5 characters")
	    #can add for wrong combination or we can just let them do whatever
	def noUsername(self):  # must be minimum of five characters
		promptWindow("Error", "No username was entered")

    #To add a new user to data file

	def adduser(self,user,passw, unames, pwords):
		if user in unames:
			self.repeatUser()
			return 0
		else:
			if len(unames) >= 10:
				self.maxUsers()
				return 0
			else:
				self.successfulRegistration()
				return 1
				
