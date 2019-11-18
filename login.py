from tkinter import *
from promptWindow import *
from Welcome import*

class loginScreen():
    def __init__(self, screen):  # creates login screen configuration
        self.screen = screen
        logframe = Frame(screen)
        logframe.pack()
        #logframe.grid(row =0,column=0)

        usrstr = StringVar()
        pwrstr = StringVar()

        #heading
        Label(logframe, text="PaceMaker Portal", bg="#bbd4dd", width="500", height="3",font=("Cambria", 20)).pack(side=TOP, fill=X)

        #username
        Label(logframe, text="Username:").pack()
        un = Entry(logframe, textvariable=usrstr)
        un.pack()  # whatever is typed will be saved into username
        Label(logframe, text="").pack()

        #password
        Label(logframe, text="Password: ").pack()
        pw = Entry(logframe, textvariable=pwrstr,show='*')
        pw.pack()  # whatever is typed will be saved into username
        Label(logframe, text="").pack()


        def createregister():
            logframe.pack_forget()
            Register(screen)

        #Login prompts

        def successfulLogin(self): #user and password match existing profilec
            logframe.pack_forget()
            Welcome(screen)

        def wrongUser(self): #user does not exist
            promptWindow("Error", "User does not exist, please try again or register as a new user")

        def wrongPassword(self): #password typed incorrectly
            promptWindow("Error", "Incorrect password, please try again")

        unames = []
        pwords = []

        #storing data in textfile into array so it can be compared
        try:  # Open the CSV we store the user/pass combos in
            srcFile = open("data.csv", "r")
            srcData = csv.DictReader(srcFile, fieldnames=['username', 'password'])

            # Append to array of unames and passwords
            for row in srcData:
                unames.append(row['username'])
                pwords.append(row['password'])

        except:  # If file does not exist, create it
            srcFile = open("data.csv", "w")
        # Close the file so we can re-open it in write mode later
        srcFile.close()

        print(unames)
        print(pwords)

        def loginuser(user,passw, u_entry ,p_entry):
            #user name and password are right
            if user in unames:
                for i in range(len(unames)):
                    if unames[i] == user and pwords[i] == passw:
                        successfulLogin(self)

                    # incorrect password
                    elif unames[i] == user:
                        u_entry.delete(0, END)
                        p_entry.delete(0, END)
                        wrongPassword(self)

            #incorrect user name or user does not exist
            else:
                u_entry.delete(0, END)
                p_entry.delete(0, END)
                wrongUser(self)

        #login
        Button(logframe, text="Login", height="2", width="15", command=lambda:loginuser(usrstr.get(),pwrstr.get(), un, pw)).pack()
        Label(logframe, text="").pack()

        #register
        # reg = Register()
        Button(logframe, text="Register", height="2", width="15", command=createregister).pack()  # command=register

        screen.mainloop()

from register import*
