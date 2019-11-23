from promptWindow import *

class loginScreen():
    def __init__(self, screen):  # creates login screen configuration
        self.screen = screen
        self.logframe = Frame(screen)

    
    #Login prompts

    def successfulLogin(self): #user and password match existing profilec
        self.logframe.pack_forget()
        #Welcome(screen) move to parent!

    def wrongUser(self): #user does not exist
        promptWindow("Error", "User does not exist, please try again or register as a new user")

    def wrongPassword(self): #password typed incorrectly
        promptWindow("Error", "Incorrect password, please try again")
    

    def loginuser(self, usrstr, pwrstr, unames, pwords, un, pw):
        #user name and password are right
        if usrstr.get() in unames:
            for i in range(len(unames)):
                if unames[i] == usrstr.get() and pwords[i] == pwrstr.get():
                    self.successfulLogin()
                    return 1

                # incorrect password
                elif unames[i] == usrstr.get():
                    un.delete(0, END)
                    pw.delete(0, END)
                    self.wrongPassword()
                    return 0

        #incorrect user name or user does not exist
        else:
            un.delete(0, END)
            pw.delete(0, END)
            self.wrongUser()
            return 0
        
