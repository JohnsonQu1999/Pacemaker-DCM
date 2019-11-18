from tkinter import *
from promptWindow import promptWindow
import csv


class Register():
	def __init__(self, screen):
		self.screen = screen
		userstr = StringVar()
		pw1str = StringVar()
		pw2str = StringVar()
		reg = Frame(screen)

		Label(reg, text = "Please Register Below:").pack(side = TOP, fill=Y)
		reg.pack(side="top", fill="both", expand = True)
		Label(reg, text = " ").pack()

		Label(reg, text="Enter Full Name:").pack()
		newuser = Entry(reg, textvariable=userstr)
		newuser.pack()
		Label(reg, text="").pack()

		Label(reg, text="Choose a password:").pack()
		password = Entry(reg, textvariable=pw1str, show ='*')
		password.pack()
		Label(reg, text="").pack()

		Label(reg, text="Confirm password:").pack()
		confirm = Entry(reg, textvariable=pw2str, show ='*')
		confirm.pack()

		submitB = Button(reg, text = "Submit", command=lambda:checkUsername(userstr.get()))
		submitB.pack()
		Label(reg, text="").pack()

		def returntolog():
			reg.pack_forget()
			loginScreen(screen)

		cancelB = Button(reg, text = "Cancel and Return to Login", command=returntolog)
		cancelB.pack()

		def checkUsername(user):
			if (len(user)==0):
				noUsername(self)
			else: 
				checkPasswords(userstr.get(),pw1str.get(), pw2str.get())

		def checkPasswords(user,p1, p2):
			if (p1 != p2):
				differentPassword(self)

			elif (len(p1)<5 or len(p2)<5):
				shortPassword(self)
			else:
				adduser(user,p1)


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


		unames = []
		pwords = []
		try: #Open the CSV we store the user/pass combos in
			srcFile = open("data.csv", "r")
			srcData = csv.DictReader(srcFile, fieldnames=['username', 'password'])

			#Append to array of unames and passwords
			for row in srcData:
				unames.append(row['username'])
				pwords.append(row['password'])

		except: #If file does not exist, create it
			srcFile = open("data.csv", "w")
			#Close the file so we can re-open it in write mode later
		srcFile.close()

        #To add a new user to data file

		def adduser(user,passw):
			if user in unames:
				repeatUser(self)
			else:
				if len(unames) >= 10:
					maxUsers(self)
				else:
					unames.append(user)
					pwords.append(passw)

					srcFile = open("data.csv", "a+")
					srcWrite = csv.DictWriter(srcFile, fieldnames=['username', 'password'])
					srcWrite.writerow({'username' : user, 'password' : passw})
					srcFile.close()

					successfulRegistration(self)
					returntolog()
					
from login import*
