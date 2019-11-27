from login import *
from register import *
from Welcome import *


#import all files
class Begin():
	def __init__(self):
		print("begin text")
		Parent()

class Parent():
	def __init__(self):
		self.screen = Tk()
		self.screen.geometry("350x350")  # set the configuration of GUI window
		self.screen.title("pAce of Hearts")
		self.login = loginScreen(self.screen)
		self.register = Register(self.screen)

		self.loginpage()

		self.unames = []
		self.pwords = []

		#for login entries
		self.usrstr = StringVar()
		self.pwrstr = StringVar()

		#for register entried
		self.userstr = StringVar()
		self.pw1str = StringVar()
		self.pw2str = StringVar()

#__________________Login Buttons_________________#
		#heading
		Label(self.login.logframe, text="PaceMaker Portal", bg="#bbd4dd", width="500", height="3",font=("Cambria", 20)).pack(side=TOP, fill=X)

		#username
		Label(self.login.logframe, text="Username:").pack()
		self.un = Entry(self.login.logframe, textvariable=self.usrstr)
		self.un.pack()  # whatever is typed will be saved into username
		Label(self.login.logframe, text="").pack()

		#password
		Label(self.login.logframe, text="Password: ").pack()
		self.pw = Entry(self.login.logframe, textvariable=self.pwrstr,show='*')
		self.pw.pack()  # whatever is typed will be saved into username
		Label(self.login.logframe, text="").pack()
		#self.buttons()

		Button(self.login.logframe, text="Login", height="2", width="15", command=self.loginuser).pack()
		Label(self.login.logframe, text="").pack()
		#register
		# reg = Register()
		Button(self.login.logframe, text="Register", height="2", width="15", command=self.registerpage).pack()  # command=register

		Button(self.login.logframe,text=" ",height="2",width="55",relief="flat",command=self.__admin).pack()

#_______________Register Buttons_______________#

		Label(self.register.reg, text = "Please Register Below:").pack(side = TOP, fill=Y)
		self.register.reg.pack(side="top", fill="both", expand = True)
		Label(self.register.reg, text = " ").pack()

		Label(self.register.reg, text="Enter Full Name:").pack()
		newuser = Entry(self.register.reg, textvariable=self.userstr)
		newuser.pack()
		Label(self.register.reg, text="").pack()

		Label(self.register.reg, text="Choose a password:").pack()
		password = Entry(self.register.reg, textvariable=self.pw1str, show ='*')
		password.pack()
		Label(self.register.reg, text="").pack()

		Label(self.register.reg, text="Confirm password:").pack()
		confirm = Entry(self.register.reg, textvariable=self.pw2str, show ='*')
		confirm.pack()

		submitB = Button(self.register.reg, text = "Submit", command=self.check)
		submitB.pack()
		Label(self.register.reg, text="").pack()
		
		cancelB = Button(self.register.reg, text = "Cancel and Return to Login", command=self.loginpage)
		cancelB.pack()
		self.register.reg.pack_forget()
		self.screen.mainloop()

	def __admin(self):
		self.login.logframe.pack_forget()
		self.welcome=Welcome(self.screen)

	def loginuser(self):
		self.getfromfile()
		if self.login.loginuser(self.usrstr, self.pwrstr, self.unames, self.pwords, self.un, self.pw)==1:
			self.welcome = Welcome(self.screen)

	def check(self):
		if self.register.checkUsername(self.userstr)==1 & self.register.checkPasswords(self.pw1str, self.pw2str)==1:
			if self.register.adduser(self.userstr.get(),self.pw1str.get(), self.unames, self.pwords)==1:
				self.unames.append(self.userstr.get())
				self.pwords.append(self.pw1str.get())

				srcFile = open("data.csv", "a+")
				srcWrite = csv.DictWriter(srcFile, fieldnames=['username', 'password'])
				srcWrite.writerow({'username' : self.userstr.get(), 'password' : self.pw1str.get()})
				srcFile.close()
				self.loginpage()

	def getfromfile(self):
		#storing data in textfile into array so it can be compared
		try:  # Open the CSV we store the user/pass combos in
			srcFile = open("data.csv", "r")
			srcData = csv.DictReader(srcFile, fieldnames=['username', 'password'])

			# Append to array of unames and passwords
			for row in srcData:
				self.unames.append(row['username'])
				self.pwords.append(row['password'])

		except:  # If file does not exist, create it
			srcFile = open("data.csv", "w")
			# Close the file so we can re-open it in write mode later
			srcFile.close()

	def loginpage(self):
		self.register.reg.pack_forget() 
		self.login.logframe.pack()

	def registerpage(self):
		self.login.logframe.pack_forget() 
		self.register.reg.pack()	

# screen = Tk()
# Welcome(screen)