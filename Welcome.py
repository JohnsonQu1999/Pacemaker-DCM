#===ABSTRACTION LAYER===#
# Required inputs: 
# Behaviour:
#  - Draws main GUI with all parameters present - capable of utilizing and managing windows for display of text and graphics
#  - Creates interface for pacing modes
#  - Displays all programmable parameters for review and modification
#  - Capable of processing user positioning and input buttons
#  - Allows user to tell instance what mode they want to edit
#  - Allows user to tell instance what they want the parameters to be
#  - Allows user to tell instance they want to reset parameters to nominal values
#  - Visually indicates when the DCM and device are communicating
#  - Visually indicates when a different pacemaker device is approached than was previously interrogated

#===TODO===#
# IDEA: for the edit_XXXX's, instead of making a dedicated method for each mode,
  # Make one that takes care of all of them, and input a string of 1's and 0's which marks which entries
  # we care about, as is page 28 of the PACEMAKER document
  # Issues: how do we determine mode? maybe check against a dictionary
  # PREREQ's: 1.) modify data storage string format (needs to include all 25 options for each mode,
  # with NA's anywhere it's not applicable)
  # 2.) edit check_In_Range - PSEUDO CODE WRITTEN
  # 3.) edit get_Vals - PSEUDO CODE WRITTEN
  # 4.) replace edit_XXX's with 1 function - PSEUDO CODE WRITTEN
  # 5.) add all buttons in create_Welcome_Window
  # This method would be called 'refreshGUI'
# Create more descriptive error messages
# Serial comms b/w DCM and board
  # Transmit parameter and mode data
  # Conduct error checking
  # Implement egram

#===IMPORT===#
from tkinter import*
from tkinter import messagebox
from rw import*

class Welcome():
	def __init__(self,screen): #Constructor, sets up inital values
		self.modeDict = {
			"Off":"0000000000000000000000000",
			"AAT":"1100001010100110000000000",
			"VVT":"1100000101011000000000000",
			"AOO":"1100001010000000000000000",
			"AAI":"1100001010100110110000000",
			"VOO":"1100000101000000000000000",
			"VVI":"1100000101011000110000000",
			"VDD":"1101100101011001011110000",
			"DOO":"1101001111000000000000000",
			"DDI":"1101001111111110000000000",
			"DDD":"1101111111111111111110000",
			"AOOR":"1110001010000000000001111",
			"AAIR":"1110001010100110110001111",
			"VOOR":"1110000101000000000001111",
			"VVIR":"1110000101011000110001111",
			"VDDR":"1111100101011001011111111",
			"DOOR":"1111001111000000000001111",
			"DDIR":"1111001111111110000001111",
			"DDDR":"1111111111111111111111111"
		}
		self.mode = "DDD"

		self.lowerRateLimitRange = list(range(30,50,5))+list(range(50,90,1))+list(range(90,176,5))
		self.upperRateLimitRange = list(range(50,176,5))
		# self.maxSensorRateRange = list(range(50,176,5))
		# self.fixedAVDelayRange = list(range(50,301,10))
		# self.dyanmicAVDelayrange = list('OFF','ON')
		self.avPulseAmpRegRange = list(('OFF',0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0))
		self.avPulseWidthRange = list((0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9))
		# self.aSensitivityRange = 
		# self.vSensitivityrange = 
		self.VRPRange = list(range(150,510,10))
		self.ARPRange = list(range(150,510,10))
		# self.pvarpExetnsionRange = 
		# self.hysRange = 
		# self.rateSmoothingRange = 
		# self.atrDurationRange = 
		# self. atrFallBackModeRange =
		# self.atrFallBacktimeRange =
		# self.activityThresholdRange = 
		# self.reactionTimeRange = 
		# self.responseFactorRange =
		# self.recoveryTimeRange = 

		self.progParam = []
		self.commsStatus = 1 # 0 means good status
		self.boardStatus = 1 # 0 means good board
		self.spinboxBD = 2
		self.root = screen
		self.commsStatusInd = StringVar()
		self.commsStatusInd.set(self.__get_Comms_Status())
		self.boardStatusInd = StringVar()
		self.boardStatusInd.set(self.__get_Board_Status())

		self.__get_User_Data()
		self.__create_Welcome_Window() #All statements must occur before this as this contains the .mainloop() where it gets trapped for all eternity.

	def __get_Comms_Status(self): # Gets comms status. Currently psuedo code - will call upon an external class in the future
		if(self.commsStatus==0):
			return "GOOD"
		else:
			return "BAD"

	def __get_Board_Status(self): # Gets board status. Currently psuedo code - will call upon an external class in the future
		if(self.boardStatus==0):
			return "GOOD"
		else:
			return "BAD"

	def __get_User_Data(self): # Gets programmable parameters from rw class
		# print(10)
		file=RW()
		self.progParam=file.get_ProgParam(0)

		# try:
		# 	file=RW(self.fileName)
		# 	self.progParam=file.get_ProgParam()
		# except:
		# 	self.__get_Default_Values(-1)

		# print(self.progParam)

	def __set_User_Data(self): # Sets user data by sending self.progParam to rw class
		file = RW()
		file.set_ProgParam(self.progParam)

	def __get_Default_Values(self,code): # Gets default nominal values from rw class instead of primary user values. Has the option of reading default for all parameters, or just for 1 mode
		file=RW()
		if(code==-1):
			self.progParam=file.get_ProgParam(1)
		else:
			self.progParam[code]=file.get_ProgParam(1)[code]

	def __set_Default_Values(self): # Sets default nominal values for one mode by using the rw class
		self.__get_Default_Values(self.mode)
		self.__set_User_Data()
		if(self.mode==0):
			self.__edit_AOO()  # calling self_editAOO() is a workaround for updating spinbox values after writing them. 
		elif(self.mode==1):    # Should replace with a single 'update' method that updates the GUI screen depending on the mode we're in
			self.__edit_VOO()
		elif(self.mode==2):
			self.__edit_AAI()
		elif(self.mode==3):
			self.__edit_VVI()
	
	def __save_Param(self): # Saves the data currently in spinboxes by reading all data, checking if its in range then finally calling the __set_User_Data() function 
		if(self.__check_In_Range()==0): # If the data is bad, it displays an error and reset the spinboxes to what they were at before
			self.__get_Vals()
			self.__set_User_Data()
		else:
			messagebox.showerror("Error","Data out of range!")
			if(self.mode==0):
				self.__edit_AOO()
			elif(self.mode==1):
				self.__edit_VOO()
			elif(self.mode==2):
				self.__edit_AAI()
			elif(self.mode==3):
				self.__edit_VVI()

	def __check_In_Range(self): # Checks if the current data stored in the spinboxes is valid. NOTE: Checks spinboxes and NOT self.progParam as we don't want to potentially overwrite good data with bad data
		inRange = 0 # 0 = in range; anything else = out of range

		# Example code if we use a code to represent each mode
		# We could use a dictionary to map modes to their code
		# inRange = 0
		# for i in numParams:
		# 	if(!((code[i]==1)&&(self.spinboxParams[i].get() in paramRanges[i]))): #paramRanges is an array that contains the range of every parameter #spinboxParams is an array of spinbox widgets #by extension, we could have an array of label widgets
		# 		inRange += 1

		# print(int(self.spinbox_LowerRateLimit.get()))
		# print(self.lowerRateLimitRange)
		# print((int(self.spinbox_LowerRateLimit.get()) in self.lowerRateLimitRange))

		try:
			if(self.mode==0):
				if((int(self.spinbox_LowerRateLimit.get()) in self.lowerRateLimitRange) == 0):
					inRange = 1
				if((int(self.spinbox_UpperRateLimit.get()) in self.upperRateLimitRange) == 0):
					inRange = 1
				try:
					if((float(self.spinbox_atrPulseAmpReg.get()) in self.avPulseAmpRegRange) == 0):
						inRange = 1
				except:
					try:
						if((self.spinbox_atrPulseAmpReg.get() in self.avPulseAmpRegRange) == 0):
							inRange = 1
					except:
						inRange = 1
				if((float(self.spinbox_atrPulseWidth.get()) in self.avPulseWidthRange) == 0):
					inRange = 1
			elif(self.mode==1):
				if((int(self.spinbox_LowerRateLimit.get()) in self.lowerRateLimitRange) == 0):
					inRange = 1
				if((int(self.spinbox_UpperRateLimit.get()) in self.upperRateLimitRange) == 0):
					inRange = 1
				try:
					if((float(self.spinbox_ventPulseAmpReg.get()) in self.avPulseAmpRegRange) == 0):
						inRange = 1
				except:
					try:
						if((self.spinbox_ventPulseAmpReg.get() in self.avPulseAmpRegRange) == 0):
							inRange = 1
					except:
						inRange = 1
				if((float(self.spinbox_ventPulseWidth.get()) in self.avPulseWidthRange) == 0):
					inRange = 1
			elif(self.mode==2):
				if((int(self.spinbox_LowerRateLimit.get()) in self.lowerRateLimitRange) == 0):
					inRange = 1
				if((int(self.spinbox_UpperRateLimit.get()) in self.upperRateLimitRange) == 0):
					inRange = 1
				try:
					if((float(self.spinbox_atrPulseAmpReg.get()) in self.avPulseAmpRegRange) == 0):
						inRange = 1
				except:
					try:
						if((self.spinbox_atrPulseAmpReg.get() in self.avPulseAmpRegRange) == 0):
							inRange = 1
					except:
						inRange = 1
				if((float(self.spinbox_atrPulseWidth.get()) in self.avPulseWidthRange) == 0):
					inRange = 1
				if((int(self.spinbox_ARP.get()) in self.ARPRange) == 0):
					inRange = 1
			elif(self.mode==3):
				if((int(self.spinbox_LowerRateLimit.get()) in self.lowerRateLimitRange) == 0):
					inRange = 1
				if((int(self.spinbox_UpperRateLimit.get()) in self.upperRateLimitRange) == 0):
					inRange = 1
				try:
					if((float(self.spinbox_ventPulseAmpReg.get()) in self.avPulseAmpRegRange) == 0):
						inRange = 1
				except:
					try:
						if((self.spinbox_ventPulseAmpReg.get() in self.avPulseAmpRegRange) == 0):
							inRange = 1
					except:
						inRange = 1
				if((float(self.spinbox_ventPulseWidth.get()) in self.avPulseWidthRange) == 0):
					inRange = 1
				if((int(self.spinbox_VRP.get()) in self.VRPRange) == 0):
					inRange = 1
		except:
			inRange = 1

		return inRange

	def __get_Vals(self): # Saves relevant spinbox data into self.progParam depending on what pacing mode the user is editing

		# Example code if we use a code to represent each mode
		# We could use a dictionary to map modes to their code
		# for i in numParams:
		# 	if(code[i]==1)
		# 		self.progParam[mode][i]=spinboxParams[i].get()

		if(self.mode==0):
			self.progParam[0][0]=self.spinbox_LowerRateLimit.get()
			self.progParam[0][1]=self.spinbox_UpperRateLimit.get()
			self.progParam[0][2]=self.spinbox_atrPulseAmpReg.get()
			self.progParam[0][3]=self.spinbox_atrPulseWidth.get()
			# print(self.progParam[0])
		elif(self.mode==1):
			self.progParam[1][0]=self.spinbox_LowerRateLimit.get()
			self.progParam[1][1]=self.spinbox_UpperRateLimit.get()
			self.progParam[1][2]=self.spinbox_ventPulseAmpReg.get()
			self.progParam[1][3]=self.spinbox_ventPulseWidth.get()
			# print(self.progParam[1])
		elif(self.mode==2):
			self.progParam[2][0]=self.spinbox_LowerRateLimit.get()
			self.progParam[2][1]=self.spinbox_UpperRateLimit.get()
			self.progParam[2][2]=self.spinbox_atrPulseAmpReg.get()
			self.progParam[2][3]=self.spinbox_atrPulseWidth.get()
			self.progParam[2][4]=self.spinbox_ARP.get()
			# print(self.progParam[2])
		elif(self.mode==3):
			self.progParam[3][0]=self.spinbox_LowerRateLimit.get()
			self.progParam[3][1]=self.spinbox_UpperRateLimit.get()
			self.progParam[3][2]=self.spinbox_ventPulseAmpReg.get()
			self.progParam[3][3]=self.spinbox_ventPulseWidth.get()
			self.progParam[3][4]=self.spinbox_VRP.get()
			# print(self.progParam[3])

	def __edit_MODE(self):
		self.mode = self.mode

	def __edit_NONE(self): # Displays the correct labels & spinboxes, and activates/deactivates the save/reset to nominal buttons depending on the mode. The next functions are similar

		# Example code if we use a code to represent each mode
		# We could use a dictionary to map modes to their code
		# Need to modify each button's command= to send edit_Mode(mode)
		# That way we can lookup mode in the dictionary to get the corresponding string code
		# self.mode = mode
		# for i in numParams:
		# 	if(code[i]==1):
		# 		self.labelParams[i].pack(side=TOP,fill=X,expand=False)
		# 		self.spinboxParams[i].pack(side=TOP,fill=X,expand=False)
		# 	else:
		# 		self.labelParams[i].pack_forget()
		# 		self.spinboxParams[i].pack_forget()

		self.mode = -1

		self.progParamFrameItemsL.config(background='snow')
		self.progParamFrameItemsR.config(background='snow')

		self.label_LowerRateLimit.pack_forget()
		self.label_UpperRateLimit.pack_forget()
		self.label_atrPulseAmpReg.pack_forget()
		self.label_ventPulseAmpReg.pack_forget()
		self.label_atrPulseWidth.pack_forget()
		self.label_ventPulseWidth.pack_forget()
		self.label_ARP.pack_forget()
		self.label_VRP.pack_forget()

		self.spinbox_LowerRateLimit.pack_forget()
		self.spinbox_UpperRateLimit.pack_forget()
		self.spinbox_atrPulseAmpReg.pack_forget()
		self.spinbox_ventPulseAmpReg.pack_forget()
		self.spinbox_atrPulseWidth.pack_forget()
		self.spinbox_ventPulseWidth.pack_forget()
		self.spinbox_ARP.pack_forget()
		self.spinbox_VRP.pack_forget()

		self.but_NONE.config(relief='sunken')
		self.but_AOO.config(relief='raised')
		self.but_VOO.config(relief='raised')
		self.but_AAI.config(relief='raised')
		self.but_VVI.config(relief='raised')
		self.but_Save.config(state=DISABLED)
		self.but_Reset.config(state=DISABLED)

	def __edit_AOO(self):
		self.mode = 0

		self.progParamFrameItemsL.config(background='snow')
		self.progParamFrameItemsR.config(background='snow')

		self.label_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_atrPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.label_ventPulseAmpReg.pack_forget()
		self.label_atrPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.label_ventPulseWidth.pack_forget()
		self.label_ARP.pack_forget()
		self.label_VRP.pack_forget()

		self.spinbox_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_atrPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.spinbox_ventPulseAmpReg.pack_forget()
		self.spinbox_atrPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.spinbox_ventPulseWidth.pack_forget()
		self.spinbox_ARP.pack_forget()
		self.spinbox_VRP.pack_forget()

		# print(self.mode)
		self.spinbox_LowerRateLimit.delete(0,"end")
		self.spinbox_LowerRateLimit.insert(0,self.progParam[self.mode][0])
		self.spinbox_UpperRateLimit.delete(0,"end")
		self.spinbox_UpperRateLimit.insert(0,self.progParam[self.mode][1])
		self.spinbox_atrPulseAmpReg.delete(0,"end")
		self.spinbox_atrPulseAmpReg.insert(0,self.progParam[self.mode][2])
		self.spinbox_atrPulseWidth.delete(0,"end")
		self.spinbox_atrPulseWidth.insert(0,self.progParam[self.mode][3])

		self.but_NONE.config(relief='raised')
		self.but_AOO.config(relief='sunken')
		self.but_VOO.config(relief='raised')
		self.but_AAI.config(relief='raised')
		self.but_VVI.config(relief='raised')
		self.but_Save.config(state=DISABLED)
		self.but_Save.config(state=NORMAL)
		self.but_Reset.config(state=NORMAL)

	def __edit_VOO(self):
		self.mode = 1

		self.progParamFrameItemsL.config(background='snow')
		self.progParamFrameItemsR.config(background='snow')

		self.label_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_atrPulseAmpReg.pack_forget()
		self.label_ventPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.label_atrPulseWidth.pack_forget()
		self.label_ventPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.label_ARP.pack_forget()
		self.label_VRP.pack_forget()

		self.spinbox_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_atrPulseAmpReg.pack_forget()
		self.spinbox_ventPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.spinbox_atrPulseWidth.pack_forget()
		self.spinbox_ventPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.spinbox_ARP.pack_forget()
		self.spinbox_VRP.pack_forget()

		# print(self.mode)
		self.spinbox_LowerRateLimit.delete(0,"end")
		self.spinbox_LowerRateLimit.insert(0,self.progParam[self.mode][0])
		self.spinbox_UpperRateLimit.delete(0,"end")
		self.spinbox_UpperRateLimit.insert(0,self.progParam[self.mode][1])
		self.spinbox_ventPulseAmpReg.delete(0,"end")
		self.spinbox_ventPulseAmpReg.insert(0,self.progParam[self.mode][2])
		self.spinbox_ventPulseWidth.delete(0,"end")
		self.spinbox_ventPulseWidth.insert(0,self.progParam[self.mode][3])

		self.but_NONE.config(relief='raised')
		self.but_AOO.config(relief='raised')
		self.but_VOO.config(relief='sunken')
		self.but_AAI.config(relief='raised')
		self.but_VVI.config(relief='raised')
		self.but_Save.config(state=DISABLED)
		self.but_Save.config(state=NORMAL)
		self.but_Reset.config(state=NORMAL)

	def __edit_AAI(self):
		self.mode = 2

		self.progParamFrameItemsL.config(background='snow')
		self.progParamFrameItemsR.config(background='snow')
		
		self.label_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_atrPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.label_ventPulseAmpReg.pack_forget()
		self.label_atrPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.label_ventPulseWidth.pack_forget()
		self.label_ARP.pack(side=TOP,fill=X,expand=False)
		self.label_VRP.pack_forget()

		self.spinbox_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_atrPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.spinbox_ventPulseAmpReg.pack_forget()
		self.spinbox_atrPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.spinbox_ventPulseWidth.pack_forget()
		self.spinbox_ARP.pack(side=TOP,fill=X,expand=False)
		self.spinbox_VRP.pack_forget()

		# print(self.mode)
		self.spinbox_LowerRateLimit.delete(0,"end")
		self.spinbox_LowerRateLimit.insert(0,self.progParam[self.mode][0])
		self.spinbox_UpperRateLimit.delete(0,"end")
		self.spinbox_UpperRateLimit.insert(0,self.progParam[self.mode][1])
		self.spinbox_atrPulseAmpReg.delete(0,"end")
		self.spinbox_atrPulseAmpReg.insert(0,self.progParam[self.mode][2])
		self.spinbox_atrPulseWidth.delete(0,"end")
		self.spinbox_atrPulseWidth.insert(0,self.progParam[self.mode][3])
		self.spinbox_ARP.delete(0,"end")
		self.spinbox_ARP.insert(0,self.progParam[self.mode][4])

		self.but_NONE.config(relief='raised')
		self.but_AOO.config(relief='raised')
		self.but_VOO.config(relief='raised')
		self.but_AAI.config(relief='sunken')
		self.but_VVI.config(relief='raised')
		self.but_Save.config(state=DISABLED)
		self.but_Save.config(state=NORMAL)
		self.but_Reset.config(state=NORMAL)

	def __edit_VVI(self):
		self.mode = 3
		
		self.progParamFrameItemsL.config(background='snow')
		self.progParamFrameItemsR.config(background='snow')

		self.label_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.label_atrPulseAmpReg.pack_forget()
		self.label_ventPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.label_atrPulseWidth.pack_forget()
		self.label_ventPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.label_ARP.pack_forget()
		self.label_VRP.pack(side=TOP,fill=X,expand=False)

		self.spinbox_LowerRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_UpperRateLimit.pack(side=TOP,fill=X,expand=False)
		self.spinbox_atrPulseAmpReg.pack_forget()
		self.spinbox_ventPulseAmpReg.pack(side=TOP,fill=X,expand=False)
		self.spinbox_atrPulseWidth.pack_forget()
		self.spinbox_ventPulseWidth.pack(side=TOP,fill=X,expand=False)
		self.spinbox_ARP.pack_forget()
		self.spinbox_VRP.pack(side=TOP,fill=X,expand=False)

		# print(self.mode)
		self.spinbox_LowerRateLimit.delete(0,"end")
		self.spinbox_LowerRateLimit.insert(0,self.progParam[self.mode][0])
		self.spinbox_UpperRateLimit.delete(0,"end")
		self.spinbox_UpperRateLimit.insert(0,self.progParam[self.mode][1])
		self.spinbox_ventPulseAmpReg.delete(0,"end")
		self.spinbox_ventPulseAmpReg.insert(0,self.progParam[self.mode][2])
		self.spinbox_ventPulseWidth.delete(0,"end")
		self.spinbox_ventPulseWidth.insert(0,self.progParam[self.mode][3])
		self.spinbox_VRP.delete(0,"end")
		self.spinbox_VRP.insert(0,self.progParam[self.mode][4])

		self.but_NONE.config(relief='raised')
		self.but_AOO.config(relief='raised')
		self.but_VOO.config(relief='raised')
		self.but_AAI.config(relief='raised')
		self.but_VVI.config(relief='sunken')
		self.but_Save.config(state=DISABLED)
		self.but_Save.config(state=NORMAL)
		self.but_Reset.config(state=NORMAL)

	def __create_Welcome_Window(self): # Creates the main GUI using .pack()
		self.root.title("DCM")
		self.root.geometry("500x750+500+100")
		
		self.metaDataFrame = Frame(self.root,bg="grey50",bd=4)
		self.metaDataFrame.pack(side = TOP,fill=X,expand=False)
		self.Ind11 = Label(self.metaDataFrame, text="Communication Status: ",bg="grey50",fg="snow")
		self.Ind11.pack(side=LEFT)
		self.Ind12 = Label(self.metaDataFrame, textvariable=self.commsStatusInd,bg="grey50",fg="snow")
		self.Ind12.pack(side = LEFT)
		self.Ind21 = Label(self.metaDataFrame, text="Board Status: ",bg="grey50",fg="snow")
		self.Ind21.pack(side=LEFT)
		self.Ind22 = Label(self.metaDataFrame, textvariable=self.boardStatusInd,bg="grey50",fg="snow")
		self.Ind22.pack(side = LEFT)

		self.otherFrame = Frame(self.root,bg="yellow")
		self.otherFrame.pack(side = BOTTOM,fill=BOTH,expand=True)

		#===Pacing mode selection explorer===#
		self.pacingModesFrame = Frame(self.otherFrame,bg="gainsboro")
		self.pacingModesFrame.pack(side = LEFT,fill=Y,expand=False)
		self.pacingModesLabel = Label(self.pacingModesFrame,text="Pacing Modes",justify=LEFT,bg="gainsboro",fg="black")
		self.pacingModesLabel.pack(side=TOP)
		self.but_NONE = Button(self.pacingModesFrame,text="Off",bg="snow",fg="black",command=self.__edit_NONE)
		self.but_NONE.pack(side=TOP,fill=X)
		self.but_AOO = Button(self.pacingModesFrame,text="AOO",bg="snow",fg="black",command=self.__edit_AOO)
		self.but_AOO.pack(side=TOP,fill=X)
		self.but_VOO = Button(self.pacingModesFrame,text="VOO",bg="snow",fg="black",command=self.__edit_VOO)
		self.but_VOO.pack(side=TOP,fill=X)
		self.but_AAI = Button(self.pacingModesFrame,text="AAI",bg="snow",fg="black",command=self.__edit_AAI)
		self.but_AAI.pack(side=TOP,fill=X)
		self.but_VVI = Button(self.pacingModesFrame,text="VVI",bg="snow",fg="black",command=self.__edit_VVI)
		self.but_VVI.pack(side=TOP,fill=X)

		#===Parameter explorer===#
		self.progParamFrame = Frame(self.otherFrame,bg="black")
		self.progParamFrame.pack(side = RIGHT,fill=BOTH,expand=True)

		#===Description===#
		self.progParamFrameTop = Frame(self.progParamFrame,bg="gainsboro")
		self.progParamFrameTop.pack(side=TOP,fill=X,expand=False)
		self.progParamFrameLabel = Label(self.progParamFrameTop,text="Edit Parameters",justify=LEFT,bg="gainsboro",fg="black")
		self.progParamFrameLabel.pack()

		#===Save & Reset Actions===#
		self.progParamFrameActions = Frame(self.progParamFrame,bg="snow")
		self.progParamFrameActions.pack(side=BOTTOM,fill=X,expand=False)
		self.but_Save = Button(self.progParamFrameActions,text="Save Parameters",state=DISABLED,command=self.__save_Param,bg="snow",fg="black")
		self.but_Save.pack(side=LEFT)
		self.but_Reset = Button(self.progParamFrameActions,text="Reset parameters to nominal",state=DISABLED,command=self.__set_Default_Values,bg="snow",fg="black")
		self.but_Reset.pack(side=LEFT)

		#===Parameter labels===#
		self.progParamFrameItemsL = Frame(self.progParamFrame,bg="snow")
		self.progParamFrameItemsL.pack(side=LEFT,fill=Y,expand=False)
		self.label_LowerRateLimit = Label(self.progParamFrameItemsL,text="Lower Rate Limit: ",justify=LEFT,bg="snow")
		self.label_UpperRateLimit = Label(self.progParamFrameItemsL,text="Upper Rate Limit: ",justify=LEFT,bg="snow")
		self.label_atrPulseAmpReg = Label(self.progParamFrameItemsL,text="Atrial Pulse Amplitude Reg.: ",justify=LEFT,bg="snow")
		self.label_ventPulseAmpReg = Label(self.progParamFrameItemsL,text="Ventricular Pulse Amplitude Reg.: ",justify=LEFT,bg="snow")
		self.label_atrPulseWidth = Label(self.progParamFrameItemsL,text="Atrial Pulse Width: ",justify=LEFT,bg="snow")
		self.label_ventPulseWidth = Label(self.progParamFrameItemsL,text="Ventricular Pulse Width: ",justify=LEFT,bg="snow")
		self.label_ARP = Label(self.progParamFrameItemsL,text="Atrial Refractory Period: ",justify=LEFT,bg="snow")
		self.label_VRP = Label(self.progParamFrameItemsL,text="Ventricular Refractory Period: ",justify=LEFT,bg="snow")

		#===Parameter Spinboxes===#
		self.progParamFrameItemsR = Frame(self.progParamFrame,bg="snow")
		self.progParamFrameItemsR.pack(side=LEFT,fill=BOTH,expand=True)
		self.spinbox_LowerRateLimit = Spinbox(self.progParamFrameItemsR,values=self.lowerRateLimitRange,bd=self.spinboxBD)
		self.spinbox_UpperRateLimit = Spinbox(self.progParamFrameItemsR,values=self.upperRateLimitRange,bd=self.spinboxBD)
		self.spinbox_atrPulseAmpReg = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpRegRange,bd=self.spinboxBD)
		self.spinbox_ventPulseAmpReg = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpRegRange,bd=self.spinboxBD)
		self.spinbox_atrPulseWidth = Spinbox(self.progParamFrameItemsR,values=self.avPulseWidthRange,bd=self.spinboxBD)
		self.spinbox_ventPulseWidth = Spinbox(self.progParamFrameItemsR,values=self.avPulseWidthRange,bd=self.spinboxBD)
		self.spinbox_ARP = Spinbox(self.progParamFrameItemsR,values=self.ARPRange,bd=self.spinboxBD)
		self.spinbox_VRP = Spinbox(self.progParamFrameItemsR,values=self.VRPRange,bd=self.spinboxBD)
		
		self.root.mainloop()
