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

#===COMPLETED TODO ITEMS==#
# IDEA: for the edit_XXXX's, instead of making a dedicated method for each mode,							COMPLETED
  # Make one that takes care of all of them, and input a string of 1's and 0's which marks which entries	COMPLETED
  # we care about, as is page 28 of the PACEMAKER document													COMPLETED
  # Issues: how do we determine mode? maybe check against a dictionary 										COMPLETED
  # PREREQ's: 1.) modify data storage string format (needs to include all 25 options for each mode,			COMPLETED
  # with NA's anywhere it's not applicable)																	COMPLETED
  # 2.) edit __check_In_Range - PSEUDO CODE WRITTEN															COMPLETED
  # 3.) edit __get_Vals - PSEUDO CODE WRITTEN																COMPLETED
  # 4.) replace edit_XXX's with 1 function - PSEUDO CODE WRITTEN											COMPLETED
  # 5.) add all buttons in __create_Welcome_Window															COMPLETED
# Create 'update' method to update screen when values change 												COMPLETED
  # This method would be called 'refreshScreen'																COMPLETED
# Main GUI, make it more user friendly																		COMPLETED
  # Replace 'Pacing Modes' label with 'Select a Pacing Mode'												COMPLETED
  # When pressing reset, ask the user to confirm 															COMPLETED
  # Prompt 'Do you want to save' when you change modes without saving										COMPLETED
  # Prompt 'Do you want to save' before saving (in case of a misclick)										COMPLETED
  # Logout button 																							COMPLETED
    # Prompt 'Are you sure?'																				COMPLETED
  # Exit button																								COMPLETED
    # Prompt 'Are you sure?'																				COMPLETED
  # Include units for all parameters 																		COMPLETED
  # Create more descriptive error messages																	COMPLETED
    # Having some issues in __check_In_Range function. Come back to this.									COMPLETED
    # If you save a value, it should be obvious that it was saved 											COMPLETED
  # Show past 2 actions (save/reset)																		COMPLETED
    # Maybe have a window at the bottom, or have a 'log' file that saves all past actions 					COMPLETED
  # Remove A/V sensitivity for relevant modes (not using)													COMPLETED
  # Remove Unreg. Voltage for A/V (only need one)															COMPLETED
  # Remove Hysteresis and PVARP 																			COMPLETED
  # Remove rate smoothing in AAI & VVI 																		COMPLETED
  # Extend pulse width to 10ms																				COMPLETED
  # Add an up/down for rate smoothing 																		COMPLETED
  # Bring back ARP (missing in AAI)																			COMPLETED
  # Remove rate smoothing in AAI and VVI 																	COMPLETED

#===TODO===#
# Simulink Compatibility
  # For activity threshold send v-low = 1 and increment by 1  (v high = 7)									simulink stuff
  # For anything that has OFF, send 0																		simulink stuff
  # Not using hysteresis, so remove for modes that we implement 											COMPLETED
  # Serial comms b/w DCM and board
    # Transmit parameter and mode data
    # Conduct error checking
  # Implement egram
  # Take care of enum for simulink																		 !!!IMPORTANT!!!

#===IMPORT===#
from tkinter import*
from tkinter import font
from rw import*
from promptWindow import promptWindow5
from copy import deepcopy

class Welcome():
	def __init__(self,screen): #Constructor, sets up inital values
		self.modeDict = {								#Dictionary to map modes to their code which tells the program which parameters are meaningful (1=meaningful)
			"Off":"00000000000000000000000000000000",
			"AAT":"11000001010101001100000000000000", 	# Not using
			"VVT":"11000000101010110000000000000000", 	# Not using
			"AOO":"11000001000100000000000000000000",
			"AAI":"11000001000100001000000000000000",
			"VOO":"11000000100010000000000000000000",
			"VVI":"11000000100010010000000000000000",
			"VDD":"11011100101010110010111111100000", 	# Not using
			"DOO":"11010001100110000000000000000000",
			"DDI":"11010001111111111100000000000000", 	# Not using
			"DDD":"11011111111111111111111111100000", 	# Not using
			"AOOR":"11100001000100000000110000001111",
			"AAIR":"11100001000100001000110000001111",
			"VOOR":"11100000100010000000110000001111",
			"VVIR":"11100000100010010000110000001111",
			"VDDR":"11111100101010110010111111111111", 	# Not using
			"DOOR":"11110001100110000000110000001111",
			"DDIR":"11110001111111111100110000001111", 	# Not using
			"DDDR":"11111111111111111111111111111111"  	# Not using
		}
		self.mode = "Off"

		# Ranges for each of the parameters
		self.lowerRateLimitRange = list(range(30,50,5))+list(range(50,90,1))+list(range(90,176,5)) 		#0
		self.upperRateLimitRange = list(range(50,176,5))												#1
		self.maxSensorRateRange = list(range(50,176,5))													#2
		self.fixedAVDelayRange = list(range(50,301,10))													#3
		self.dyanmicAVDelayRange = list(('OFF','ON'))													#4
		self.minDynamicAVDelayRange = list(range(30,101,10))											#5
		self.sensedAVDelayOffsetRange = list(('OFF',-10,-20,-30,-40,-50,-60,-70,-80,-90,-100))			#6
		self.avPulseAmpRegRange = list((0,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0)) #7,8
		self.avPulseAmpUnregRange = list((0,1.25,2.5,3.75,5))																																#9,10
		self.avPulseWidthRange = list((0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5.0,5.1,5.2,5.3,5.4,5.5,5.6,5.7,5.8,5.9,6.0,6.1,6.2,6.3,6.4,6.5,6.6,6.7,6.8,6.9,7.0,7.1,7.2,7.3,7.4,7.5,7.6,7.7,7.8,7.9,8.0,8.1,8.2,8.3,8.4,8.5,8.6,8.7,8.8,8.9,9.0,9.1,9.2,9.3,9.4,9.5,9.6,9.7,9.8,9.9,10.0))	#11,12
		self.aSensitivityRange = list((0.25,0.5,0.75))+list((1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10))																			#13
		self.vSensitivityRange = list((0.25,0.5,0.75))+list((1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10))																			#14
		self.VRPRange = list(range(150,510,10))															#15
		self.ARPRange = list(range(150,510,10))															#16
		self.pvarpRange = list(range(150,501,10))														#17
		self.pvarpExtensionRange = list(('OFF'))+list(range(50,401,50))									#18
		self.hysRange = ['OFF']+list(range(30,50,5))+list(range(50,90,1))+list(range(90,176,5))			#19
		self.rateSmoothingRange = list(('OFF',3,6,9,12,15,18,21,25))									#20,21
		self.atrFallBackModeRange = list(('OFF','ON'))													#25
		self.atrDurationCyclesRange = list(range(10,11,1))												#22
		self.atrDurationLowerRange = list(range(20,81,20))												#23
		self.atrDurationUpperRange = list(range(100,2001,100))											#24
		self.atrFallBackTimeRange = list(range(1,6,1))													#26
		self.ventricularBlankingRange = list(range(30,61,10))											#27
		self.activityThresholdRange = list(('V-LOW','LOW','MED-LOW','MED','MED-HIGH','HIGH','V-HIGH'))	#28
		self.reactionTimeRange = list(range(10,51,10))													#29
		self.responseFactorRange = list(range(1,17,1))													#30
		self.recoveryTimeRange = list(range(2,17,1))													#31
		self.rangesParam = list((self.lowerRateLimitRange,self.upperRateLimitRange,self.maxSensorRateRange,self.fixedAVDelayRange,self.dyanmicAVDelayRange,self.minDynamicAVDelayRange,
			self.sensedAVDelayOffsetRange,self.avPulseAmpRegRange,self.avPulseAmpRegRange,self.avPulseAmpUnregRange,self.avPulseAmpUnregRange,self.avPulseWidthRange,self.avPulseWidthRange,
			self.aSensitivityRange,self.vSensitivityRange,self.VRPRange,self.ARPRange,self.pvarpRange,self.pvarpExtensionRange,self.hysRange,self.rateSmoothingRange,self.rateSmoothingRange,self.atrDurationCyclesRange,
			self.atrDurationLowerRange,self.atrDurationUpperRange,self.atrFallBackModeRange,self.atrFallBackTimeRange,self.ventricularBlankingRange,self.activityThresholdRange,
			self.reactionTimeRange,self.responseFactorRange,self.recoveryTimeRange)) 					# Combining all ranges into a list

		self.parameterNamesParam = ["Lower Rate Limit","Upper Rate Limit","Maximum Sensor Rate","Fixed AV Delay","Dynamic AV Delay","Minimum Dynamic AV Delay",
		"Sensed AV Delay Offset","Atrial Pulse Amplitude Regulated","Ventricular Pulse Amplitude Regulated","Atrial Pulse Amplitude Unregulated",
		"Ventricular Pulse Amplitude Unregulated","Atrial Pulse Width","Ventricular Pulse Width","Atrial Sensitivity","Ventricular Sensitivity",
		"Ventricular Regulatory Pulse","Atrial Regulatory Pulse","PVARP","PVARP Extension","Hysteresis","Rate Smoothing Up","Rate Smoothing Down","Atrial Fallback Mode",
		"Atrial Duration Cycles","Atrial Duration Lower Range","Atrial Duration Upper Range","Ventricular Blanking","Atrial Fall Back Time","Activity Threshold",
		"Reaction Time","Response Factor","Recovery Time"]

		#===Core variable parameters===#
		self.progParam = []
		self.progParamTMinus1 = []
		self.logContents = []
		self.commsStatusInd = StringVar()
		self.boardStatusInd = StringVar()
		self.refreshTimeVar = StringVar()
		self.refreshTime = 0

		#===Auxiliary Variable parameters===#
		self.numParams = 32
		self.activityThresholdIndex = 28
		self.labelParams = [None]*self.numParams
		self.spinboxParams = [None]*self.numParams
		self.commsStatus = 1 # 0 means good status
		self.boardStatus = 1 # 0 means good board
		self.offsetX = 0
		self.offsetY = 0

		#===Window Parameters===# - should probably replace with #define
		self.butFill = BOTH
		self.butWidth = "10"
		self.butAnchor = "e"
		self.spinboxBD = 2
		self.spinboxWidth = 15
		self.paddingWidthVert = 2
		self.paddingWidthHorz = 4
		self.headingsHeight = 2
		self.spinboxJustify = "center"
		self.popupLocation = "+150+300"
		self.topFrameColour = "cornflower blue"
		self.textColourLight = "ghost white"
		self.buttonTextColour = "black"
		self.backGroundColour = "white"

		#===Fonts===#
		self.fontHeading = font.Font(family="BebasNeue-Regular",size=18)
		self.fontButton = font.Font(family="Helvetica Neue",size=11)
		self.fontLabel = font.Font(family="Helvetica Neue",size=12)
		self.fontSpinbox = font.Font(family="Helvetica Neue",size=12)
		self.fontMeta = font.Font(family="Helvetica Neue",size=14)
		self.fontText = font.Font(family="Helvetica Neue",size=12)

		self.root = screen

		self.__get_User_Data()
		self.__start_Status_Check_Loop(self.refreshTime)
		self.__create_Welcome_Window()

		self.root.mainloop() #All statements must occur before this line as .mainloop() traps it for all eternity. (.mainloop ~ while(1);)

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
	
	def __set_Meta_Status(self): # Sets the board & comms status, using the getter functions for comms and board
		self.commsStatusInd.set(self.__get_Comms_Status())
		self.boardStatusInd.set(self.__get_Board_Status())

	def __start_Status_Check_Loop(self,secondsToCheck): # Runs repeatedly to check the comms and board status by using the .after() function
		self.refreshTimeVar.set(str(secondsToCheck))

		if(secondsToCheck <= 0):
			self.__set_Meta_Status()
			secondsToCheck = 10
		else:
			secondsToCheck = secondsToCheck-1

		self.root.after(1000,self.__start_Status_Check_Loop,secondsToCheck)

	def __get_User_Data_Pacemaker(self): # Gets programmable parameters from pacemaker
		# serial = Serial()

		# progParamUnParsed = serial.download_Parameters(self.mode)

		if(progParamUnParsed == -1):
			print("failure")
			return

		indexParsed = 0
		indexUnparsed = 0

		for param in self.modeDict[self.mode]:
			if (param == 1):
				self.progParam.append(progParamUnParsed[indexUnParsed])
				indexUnparsed+=1
				indexParsed+=1
			else:
				self.progParam.append("NA")
				indexParsed+=1

	def __set_User_Data_Pacemaker(self): # Sets programmable parameters to pacemaker
		progParamParsed = [] # Parsed parameter array

		index = 0

		for param in self.modeDict[self.mode]: # Parsing the parameter array to remove all 'NA's
			print(str(index)+","+str(param))
			if(param == '1'):
				if(index == 28): # Checking for Activity Threshold first because it's special.
					progParamParsed.append(str(self.__activityThreshold_Enum()))
					print("Appended "+str(self.__activityThreshold_Enum()))
				elif(self.progParam[self.__mode_Enum()][index]=='OFF'):
					progParamParsed.append('0')
					print("Appended 0 for OFF")
				else:
					progParamParsed.append(str(self.progParam[self.__mode_Enum()][index]))
					print("Appended "+str(self.progParam[self.__mode_Enum()][index]))
			index+=1

		print(progParamParsed)

		# serial = Serial() # Instantiating a serial object

		# if(serial.upload_Parameters(self.mode,progParamParsed) == 0): # Writing to the board, feedback depending on return value
		# 	print("success")
		# else:
		# 	print("failure")

	def __get_User_Data(self): # Gets programmable parameters from rw class
		file=RW()
		self.progParam=file.get_ProgParam(0)

	def __set_User_Data_File(self): # Sets user data by sending self.progParam to rw class
		file = RW()
		file.set_ProgParam(self.progParam)

	def __get_Default_Values(self,mode): # Gets default nominal values from rw class instead of primary user values. Has the option of reading default for all parameters, or just for 1 mode
		file=RW()						 # if code = -1, set all values to default, if not, only set 1 modes' values to default
		if(mode==-1):
			self.progParam=file.get_ProgParam(1)
		else:
			self.progParamTMinus1=deepcopy(self.progParam)
			self.progParam[mode]=file.get_ProgParam(1)[mode]

			index = 0

			for get in self.modeDict[self.mode]:
				if(get == '1'):
					print("Old: "+self.progParamTMinus1[self.__mode_Enum()][index])
					print("New: "+self.progParam[self.__mode_Enum()][index])
					if(self.progParam[self.__mode_Enum()][index] != self.progParamTMinus1[self.__mode_Enum()][index]):
						self.__write_To_Log("MODE: "+self.mode+". RESET Parameter: "+self.parameterNamesParam[index]+" to default ("+self.progParamTMinus1[self.__mode_Enum()][index]+"->"+self.progParam[self.__mode_Enum()][index]+")")
					else:
						self.__write_To_Log("MODE: "+self.mode+". Parameter: "+self.parameterNamesParam[index]+" ("+self.progParam[self.__mode_Enum()][index]+")")
				index+=1

	def __confirm_Reset_Default_Values(self):
		confirmReset = Tk()
		confirmReset.geometry(self.popupLocation)
		confirmReset.title("Reset to default values?")

		def __confirmed(window):
			window.destroy()
			self.__set_Default_Values()
			self.__flashSpinboxParams()

		Label(confirmReset,text="Are you sure you want to reset to nominal values?").pack()
		Button(confirmReset,text="Yes, reset to nominal values.",command=lambda:__confirmed(confirmReset)).pack(fill=X)
		Button(confirmReset,text="No, return to editor.",command=confirmReset.destroy).pack(fill=X)

	def __set_Default_Values(self): # Sets default nominal values for one mode by using the rw class
		self.__get_Default_Values(self.__mode_Enum())
		self.__set_User_Data_File()
		self.__set_User_Data_Pacemaker()
		self.__refresh_Screen()
		self.__write_To_Log("Loaded default parameters for mode "+str(self.mode))
	
	def __save_Param(self): # Saves the data currently in spinboxes by reading all data, checking if its in range then finally calling the __set_User_Data_File() function 
		if(self.__check_In_Range()==0): # If the data is bad, it displays an error and reset the spinboxes to what they were at before
			confirmSave = Tk()
			confirmSave.geometry(self.popupLocation)
			confirmSave.title("Run "+self.mode+"?")

			def __confirmed(window):
				window.destroy()
				self.__get_Vals()
				self.__set_User_Data_File()
				self.__set_User_Data_Pacemaker()
				self.__flashSpinboxParams(0)
	
			Label(confirmSave,text="Are you sure you want to run "+self.mode+"?").pack()
			Button(confirmSave,text="Yes, run "+self.mode+".",command=lambda:__confirmed(confirmSave)).pack(fill=X)
			Button(confirmSave,text="No, return to editor.",command=confirmSave.destroy).pack(fill=X)
		else:
			self.__refresh_Screen()

	def __refresh_Screen(self):
		self.__show_MODE(self.mode)
		# This comment serves no purpose beside letting me minimize the function

	def __get_Vals(self): # Saves relevant spinbox data into self.progParam depending on what pacing mode the user is editing
		index = 0

		self.progParamTMinus1=deepcopy(self.progParam)

		print(self.progParamTMinus1[self.__mode_Enum()][0])

		for get in self.modeDict[self.mode]:
			if(get == '1'):
				self.progParam[self.__mode_Enum()][index] = self.spinboxParams[index].get()
				print("Old: "+self.progParamTMinus1[self.__mode_Enum()][index])
				print("New: "+self.progParam[self.__mode_Enum()][index])
				if(self.progParam[self.__mode_Enum()][index] != self.progParamTMinus1[self.__mode_Enum()][index]):
					self.__write_To_Log("MODE: "+self.mode+". UPDATED Parameter: "+self.parameterNamesParam[index]+" ("+self.progParamTMinus1[self.__mode_Enum()][index]+"->"+self.progParam[self.__mode_Enum()][index]+")")
				else:
					self.__write_To_Log("MODE: "+self.mode+". Parameter: "+self.parameterNamesParam[index]+" ("+self.progParam[self.__mode_Enum()][index]+")")
			index+=1

		self.__write_To_Log("Selected mode "+self.mode+" to run")

	def __check_In_Range(self): # Checks if the current data stored in the spinboxes is valid. NOTE: Checks spinboxes and NOT self.progParam as we don't want to potentially overwrite good data with bad data
		index = 0

		print("Checking for valid values in mode: "+self.mode)
		for check in self.modeDict[self.mode]:
			if(check == '1'):
				print("check int for "+self.parameterNamesParam[index])
				try:
					if((int(self.spinboxParams[index].get()) in self.rangesParam[index]) == 0):
						promptWindow5("Data out of Range","Entered value:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
						return 1
				except:
					print("check float for "+self.parameterNamesParam[index])
					try:
						if((float(self.spinboxParams[index].get()) in self.rangesParam[index]) == 0):
							promptWindow5("Data out of Range","Entered value:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
							return 1
					except:
						print("check string for "+self.parameterNamesParam[index])
						try:
							if((self.spinboxParams[index].get() in self.rangesParam[index]) == 0):
								promptWindow5("Data out of Range","Entered values:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
								return 1
						except:
							promptWindow5("Data out of Range","Entered value:",self.parameterNamesParam[index],self.spinboxParams[index].get(),"Allowed values:",self.rangesParam[index])
							return 1
			index+=1

		return 0

	def __check_If_Same(self): # returns 0 if spinbox values match stored. returns 1 else
		index = 0
		print("Checking for unsaved values in "+self.mode)
		for check in self.modeDict[self.mode]:
			if(check == '1'):
				if(self.progParam[self.__mode_Enum()][index] != self.spinboxParams[index].get()):
					return 1

			# 	print("Checking index "+str(index)+", Comparing to: "+self.progParam[self.__mode_Enum()][index])
			# 	print("Spinbox value: "+self.spinboxParams[index].get())
				# print(self.progParam[self.__mode_Enum()][index] == self.spinboxParams[index].get())
			index+=1

		return 0

	def __flashSpinboxParams(self,step=0):
		if(step == 0):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray9"
				self.progParamFrameItemsR["bg"] = "gray9"
				self.spinboxParams[i]["bg"] = "gray9"
				self.labelParams[i]["bg"] = "gray9"
			self.root.after(10,self.__flashSpinboxParams,1)
		elif(step == 1):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray19"
				self.progParamFrameItemsR["bg"] = "gray19"
				self.spinboxParams[i]["bg"] = "gray19"
				self.labelParams[i]["bg"] = "gray19"
			self.root.after(20,self.__flashSpinboxParams,2)
		elif(step == 2):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray29"
				self.progParamFrameItemsR["bg"] = "gray29"
				self.spinboxParams[i]["bg"] = "gray29"
				self.labelParams[i]["bg"] = "gray29"
			self.root.after(30,self.__flashSpinboxParams,3)
		elif(step == 3):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray39"
				self.progParamFrameItemsR["bg"] = "gray39"
				self.spinboxParams[i]["bg"] = "gray39"
				self.labelParams[i]["bg"] = "gray39"
			self.root.after(40,self.__flashSpinboxParams,4)
		elif(step == 4):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray49"
				self.progParamFrameItemsR["bg"] = "gray49"
				self.spinboxParams[i]["bg"] = "gray49"
				self.labelParams[i]["bg"] = "gray49"
			self.root.after(50,self.__flashSpinboxParams,5)
		elif(step == 5):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray59"
				self.progParamFrameItemsR["bg"] = "gray59"
				self.spinboxParams[i]["bg"] = "gray59"
				self.labelParams[i]["bg"] = "gray59"
			self.root.after(60,self.__flashSpinboxParams,6)
		elif(step == 6):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray69"
				self.progParamFrameItemsR["bg"] = "gray69"
				self.spinboxParams[i]["bg"] = "gray69"
				self.labelParams[i]["bg"] = "gray69"
			self.root.after(70,self.__flashSpinboxParams,7)
		elif(step == 7):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray79"
				self.progParamFrameItemsR["bg"] = "gray79"
				self.spinboxParams[i]["bg"] = "gray79"
				self.labelParams[i]["bg"] = "gray79"
			self.root.after(80,self.__flashSpinboxParams,8)
		elif(step == 8):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray89"
				self.progParamFrameItemsR["bg"] = "gray89"
				self.spinboxParams[i]["bg"] = "gray89"
				self.labelParams[i]["bg"] = "gray89"
			self.root.after(90,self.__flashSpinboxParams,9)
		elif(step == 9):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = "gray99"
				self.progParamFrameItemsR["bg"] = "gray99"
				self.spinboxParams[i]["bg"] = "gray99"
				self.labelParams[i]["bg"] = "gray99"
			self.root.after(100,self.__flashSpinboxParams,10)
		elif(step == 10):
			for i in range(31):
				self.progParamFrameItemsL["bg"] = self.backGroundColour
				self.progParamFrameItemsR["bg"] = self.backGroundColour
				self.spinboxParams[i]["bg"] = self.backGroundColour
				self.labelParams[i]["bg"] = self.backGroundColour
			self.root.after(110,self.__flashSpinboxParams,11)
		return

	def __write_To_Log(self,text):
		log = RW()
		log.append_To_Log(text)

	def __welcome_Prompts(self):
		welcomeWindow = Tk()
		welcomeWindow.geometry(self.popupLocation)
		welcomeWindow.title("Welcome")

		def __confirmed(window):
			window.destroy()

		Label(welcomeWindow,text="Start by selecting a mode on the left hand explorer").pack()
		Label(welcomeWindow,text="Next, edit the parameters as required, followed by Saving and Running the selected mode").pack()
		Label(welcomeWindow,text="If you make an error, you can view past actions by clicking the 'Log' button at the bottom right").pack()
		Label(welcomeWindow,text="You can also load default values if you wish by clicking 'Reset parameters to Nominal' at the bottom").pack()
		Button(welcomeWindow,text="Okay",command=lambda:__confirmed(welcomeWindow)).pack(fill=X)

	def __show_Log(self):
		self.mainFrame.pack_forget()
		self.logFrame.pack(side=TOP,fill=BOTH,expand=True)
		# self.logInfoFrame.pack(side = TOP,fill=X,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		# self.Info1.pack(side=LEFT) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		# self.logTextFrame.pack(side=TOP,fill=X,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		# self.logFrameScrollbar.pack(side=RIGHT,fill=Y,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		# self.but1_Logout.pack(side=RIGHT)

		logs = RW()
		self.logContents = logs.get_Logs()

		#===Need to run this before using insert/delete functions===#
		self.logText.config(state=NORMAL)
		#===Delete old text===#
		self.logText.delete("0.0",END)

		#===Print new text===#
		for line in self.logContents:
			# print(line)
			self.logText.insert(END,line)
			self.logText.insert(END,"\n")

		self.logText.pack() # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		#===Need to run this to prevent user edits===#
		self.logText.config(state=DISABLED)

		# self.logInfoActionsFrame.pack(side=BOTTOM,fill=X,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		# self.logReturnButton.pack(side=RIGHT) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
	
	def __show_Main_Frame(self):
		self.logFrame.pack_forget()
		self.mainFrame.pack(side=TOP,fill=BOTH,expand=True)

	def __mode_Enum(self):
		if(self.mode == "Off"):
			return -1
		if(self.mode == "AAT"):
			return 0
		if(self.mode == "VVT"):
			return 1
		if(self.mode == "AOO"):
			return 2
		if(self.mode == "AAI"):
			return 3
		if(self.mode == "VOO"):
			return 4
		if(self.mode == "VVI"):
			return 5
		if(self.mode == "VDD"):
			return 6
		if(self.mode == "DOO"):
			return 7
		if(self.mode == "DDI"):
			return 8
		if(self.mode == "DDD"):
			return 9
		if(self.mode == "AOOR"):
			return 10
		if(self.mode == "AAIR"):
			return 11
		if(self.mode == "VOOR"):
			return 12
		if(self.mode == "VVIR"):
			return 13
		if(self.mode == "VDDR"):
			return 14
		if(self.mode == "DOOR"):
			return 15
		if(self.mode == "DDIR"):
			return 16
		if(self.mode == "DDDR"):
			return 17

	def __activityThreshold_Enum(self):
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'V-LOW'):
			return 1
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'LOW'):
			return 2
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'MED-LOW'):
			return 3
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'MED'):
			return 4
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'MED-HIGH'):
			return 5
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'HIGH'):
			return 6
		if(self.progParam[self.__mode_Enum()][self.activityThresholdIndex] == 'V-HIGH'):
			return 7
		print(self.progParam[self.__mode_Enum()][self.activityThresholdIndex])
		print("Activity Threshold could not be enumerated")
		return -1

	def __show_MODE(self,mode): # Displays the correct labels, spinboxes, and activates/deactivates the save/reset buttons
		# If values different from stored, confirm if they want to switch
		self.mode = mode

		index = 0

		for show in self.modeDict[self.mode]:
			self.labelParams[index].pack_forget()
			self.spinboxParams[index].pack_forget()
			index+=1

		index = 0

		for show in self.modeDict[self.mode]:
			if(int(show)):
				self.labelParams[index].pack(side=TOP,anchor="e",fill=Y,expand=False)
				self.spinboxParams[index].pack(side=TOP,anchor="w",fill=Y,expand=False)
			index+=1

		index = 0

		for show in self.modeDict[self.mode]:
			if(int(show)):
				self.spinboxParams[index].delete(0,"end")
				self.spinboxParams[index].insert(0,self.progParam[self.__mode_Enum()][index])
			index+=1

		# if(self.__mode_Enum() == -1):
		# 	self.but_Save.config(state=DISABLED)
		# 	self.but_Reset.config(state=DISABLED)
		# else:
		self.but_Save.config(state=NORMAL)
		self.but_Reset.config(state=NORMAL)
		self.but_ViewLog.config(state=NORMAL)

		self.but_Off.config(relief='raised')
		self.but_AOO.config(relief='raised')
		self.but_VOO.config(relief='raised')
		self.but_AAI.config(relief='raised')
		self.but_VVI.config(relief='raised')
		self.but_DOO.config(relief='raised')
		self.but_AOOR.config(relief='raised')
		self.but_AAIR.config(relief='raised')
		self.but_VOOR.config(relief='raised')
		self.but_VVIR.config(relief='raised')
		self.but_DOOR.config(relief='raised')
		
		if(self.__mode_Enum() == -1):
			self.but_Off.config(relief='sunken')
		elif(self.__mode_Enum() == 2):
			self.but_AOO.config(relief='sunken')
		elif(self.__mode_Enum() == 3):
			self.but_AAI.config(relief='sunken')
		elif(self.__mode_Enum() == 4):
			self.but_VOO.config(relief='sunken')
		elif(self.__mode_Enum() == 5):
			self.but_VVI.config(relief='sunken')
		elif(self.__mode_Enum() == 7):
			self.but_DOO.config(relief='sunken')
		elif(self.__mode_Enum() == 10):
			self.but_AOOR.config(relief='sunken')
		elif(self.__mode_Enum() == 11):
			self.but_AAIR.config(relief='sunken')
		elif(self.__mode_Enum() == 12):
			self.but_VOOR.config(relief='sunken')
		elif(self.__mode_Enum() == 13):
			self.but_VVIR.config(relief='sunken')
		elif(self.__mode_Enum() == 15):
			self.but_DOOR.config(relief='sunken')

	def __edit_MODE(self,mode): # Checks if unsaved errors exist. If so, prompt user to go back and save or ignore. Calls __show_MODE(,) to actually view the mode
		if(self.__check_If_Same() == 1):
			# Confirm w/ user
			confirmDoNotSave = Tk()
			confirmDoNotSave.geometry(self.popupLocation)
			confirmDoNotSave.title("Are you sure?")

			def __confirmed(window):
				window.destroy()
				self.__show_MODE(mode);

			Label(confirmDoNotSave,text="There are unsaved changes. Do you want to go back and save?").pack()
			Button(confirmDoNotSave,text="Yes, go back and save changes.",command=confirmDoNotSave.destroy).pack(fill=X)
			Button(confirmDoNotSave,text="No, switch modes and delete changes.",command=lambda:__confirmed(confirmDoNotSave)).pack(fill=X)
		else:
			self.__show_MODE(mode)

	def __dragWindow(self,event):
	    x = self.metaDataFrame.winfo_pointerx() - self.offsetX
	    y = self.metaDataFrame.winfo_pointery() - self.offsetY
	    self.root.geometry('+{x}+{y}'.format(x=x,y=y))

	def __clickWindow(self,event):
	    self.offsetX = event.x
	    self.offsetY = event.y

	def __logout(self):
		if(self.__check_If_Same() == 1):
			# Confirm w/ user
			confirm = Tk()
			confirm.geometry(self.popupLocation)
			confirm.title("Logout?")

			def __confirmed(window):
				window.destroy()
				self.root.destroy()
				from parent import Parent
				Parent()

			Label(confirm,text="There are unsaved changes. Are you sure you want to logout?").pack()
			Button(confirm,text="Yes",command=lambda:__confirmed(confirm)).pack(fill=X)
			Button(confirm,text="No",command=confirm.destroy).pack(fill=X)
		else:
			confirm = Tk()
			confirm.geometry(self.popupLocation)
			confirm.title("Are you sure you want to logout?")

			def __confirmed(window):
				window.destroy()
				self.root.destroy()
				from parent import Parent
				Parent()

			Label(confirm,text="Are you sure you want to logout?").pack()
			Button(confirm,text="Yes",command=lambda:__confirmed(confirm)).pack(fill=X)
			Button(confirm,text="No",command=confirm.destroy).pack(fill=X)

	def __exit(self):
		if(self.__check_If_Same() == 1):
			# Confirm w/ user
			confirm = Tk()
			confirm.geometry(self.popupLocation)
			confirm.title("Exit?")

			def __confirmed(window):
				window.destroy()
				self.root.destroy()

			Label(confirm,text="There are unsaved changes. Are you sure you want to exit?").pack()
			Button(confirm,text="Yes",command=lambda:__confirmed(confirm)).pack(fill=X)
			Button(confirm,text="No",command=confirm.destroy).pack(fill=X)
		else:
			confirm = Tk()
			confirm.geometry(self.popupLocation)
			confirm.title("Are you sure you want to exit?")

			def __confirmed(window):
				window.destroy()
				self.root.destroy()

			Label(confirm,text="Are you sure you want to exit?").pack()
			Button(confirm,text="Yes",command=lambda:__confirmed(confirm)).pack(fill=X)
			Button(confirm,text="No",command=confirm.destroy).pack(fill=X)

	def __create_Welcome_Window(self): # Creates the main GUI using .pack()
		# #==Remove title bar===#
		# self.root.overrideredirect(True)
		
		# #===Implement draggability===#
		# self.root.bind('<Button-1>',self.__clickWindow)
		# self.root.bind('<B1-Motion>',self.__dragWindow)
		
		#===Frame Setup===#
		self.root.title("Digital Communications Module")
		self.root.geometry("850x600+100+100")
		
		# There are 2 high level frames, 'Main frame' and 'log frame'
			# Interact with parameters in the main frame
			# See the log file in the log frame

		#===Main Frame Setup===#
		self.mainFrame = Frame(self.root)
		self.mainFrame.pack(side=TOP,fill=BOTH,expand=True)

		#===Top Status bar + Logout + Exit + Icon===#
		self.metaDataFrame = Frame(self.mainFrame,bg=self.topFrameColour,bd=4)
		self.metaDataFrame.pack(side = TOP,fill=X,expand=False)
		
		self.Ind11 = Label(self.metaDataFrame, text="Communication Status: ",bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.Ind11.pack(side=LEFT)
		self.Ind12 = Label(self.metaDataFrame, textvariable=self.commsStatusInd,bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.Ind12.pack(side = LEFT)
		self.Ind21 = Label(self.metaDataFrame, text="   Board Status: ",bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.Ind21.pack(side=LEFT)
		self.Ind22 = Label(self.metaDataFrame, textvariable=self.boardStatusInd,bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.Ind22.pack(side = LEFT)
		self.UpdateIndicatorLabel = Label(self.metaDataFrame,text="   Refreshing in: ",bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.UpdateIndicatorLabel.pack(side=LEFT)
		self.UpdateIndicatorVar = Label(self.metaDataFrame,textvariable=self.refreshTimeVar,bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.UpdateIndicatorVar.pack(side=LEFT)
		self.but_Exit = Button(self.metaDataFrame,text="Exit",state=NORMAL,command=self.__exit,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but_Exit.pack(side=RIGHT)
		self.but_Logout = Button(self.metaDataFrame,text="Logout",state=NORMAL,command=self.__logout,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but_Logout.pack(side=RIGHT)

		#===Bottom frames===#
		self.otherFrame = Frame(self.mainFrame,bg="yellow")
		self.otherFrame.pack(side = BOTTOM,fill=BOTH,expand=True)

		#===Pacing mode selection explorer===#
		self.pacingModesFrame = Frame(self.otherFrame,bg=self.backGroundColour)
		self.pacingModesFrame.pack(side = LEFT,fill=Y,expand=False)

		self.pacingModesLabel = Label(self.pacingModesFrame,text="Select a Pacing Mode",justify=LEFT,width="20",height=self.headingsHeight,bg=self.backGroundColour,fg="black",font=self.fontHeading)
		self.pacingModesLabel.pack(side=TOP)
		self.but_Off = Button(self.pacingModesFrame,text="Off",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("Off"))
		self.but_Off.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_AOO = Button(self.pacingModesFrame,text="AOO",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("AOO"))
		self.but_AOO.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_VOO = Button(self.pacingModesFrame,text="VOO",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("VOO"))
		self.but_VOO.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_AAI = Button(self.pacingModesFrame,text="AAI",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("AAI"))
		self.but_AAI.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_VVI = Button(self.pacingModesFrame,text="VVI",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("VVI"))
		self.but_VVI.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_DOO = Button(self.pacingModesFrame,text="DOO",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("DOO"))
		self.but_DOO.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_AOOR = Button(self.pacingModesFrame,text="AOOR",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("AOOR"))
		self.but_AOOR.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_AAIR = Button(self.pacingModesFrame,text="AAIR",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("AAIR"))
		self.but_AAIR.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_VOOR = Button(self.pacingModesFrame,text="VOOR",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("VOOR"))
		self.but_VOOR.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_VVIR = Button(self.pacingModesFrame,text="VVIR",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("VVIR"))
		self.but_VVIR.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)
		self.but_DOOR = Button(self.pacingModesFrame,text="DOOR",bg=self.backGroundColour,fg=self.buttonTextColour,width=self.butWidth,font=self.fontButton,command=lambda:self.__edit_MODE("DOOR"))
		self.but_DOOR.pack(side=TOP,fill=self.butFill,anchor=self.butAnchor)

		#===Parameter explorer===#
		self.progParamFrame = Frame(self.otherFrame,bg="black")
		self.progParamFrame.pack(side = RIGHT,fill=BOTH,expand=True)

		#===Description===#
		self.progParamFrameTop = Frame(self.progParamFrame,bg=self.backGroundColour)
		self.progParamFrameTop.pack(side=TOP,fill=X,expand=False)
		self.progParamFrameLabel = Label(self.progParamFrameTop,text="Edit Parameters",justify=LEFT,height=self.headingsHeight,bg=self.backGroundColour,fg="black",font=self.fontHeading)
		self.progParamFrameLabel.pack()

		#===Parameter explorer top side padding===#
		self.progParamFrameTopPadding = Frame(self.progParamFrame,bg="gainsboro",width=self.paddingWidthHorz)
		self.progParamFrameTopPadding.pack(side=TOP,fill=X,expand=False)

		#===Parameter explorer left side padding===#
		self.progParamFrameLeftPadding1 = Frame(self.progParamFrame,bg="gainsboro",width=self.paddingWidthVert)
		self.progParamFrameLeftPadding1.pack(side=LEFT,fill=Y,expand=False)
		self.progParamFrameLeftPadding2 = Frame(self.progParamFrame,bg=self.backGroundColour,width="50")
		self.progParamFrameLeftPadding2.pack(side=LEFT,fill=Y,expand=False)

		#===View Log Action===#
		self.progParamFrameLogActions = Frame(self.progParamFrame,bg=self.backGroundColour)
		self.progParamFrameLogActions.pack(side=BOTTOM,fill=X,expand=False)
		self.but_ViewLog = Button(self.progParamFrameLogActions,text="View past Actions (Log)",state=NORMAL,command=self.__show_Log,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but_ViewLog.pack(side=RIGHT)

		#===Save & Reset Actions===#
		self.progParamFrameActions = Frame(self.progParamFrame,bg=self.backGroundColour)
		self.progParamFrameActions.pack(side=BOTTOM,fill=X,expand=False)
		self.but_Reset = Button(self.progParamFrameActions,text="Reset parameters to nominal",state=NORMAL,command=self.__confirm_Reset_Default_Values,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but_Reset.pack(side=RIGHT)
		self.but_Save = Button(self.progParamFrameActions,text="Save parameters and Run current mode",state=NORMAL,command=self.__save_Param,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but_Save.pack(side=RIGHT)

		#===Parameter labels===#
		self.progParamFrameItemsL = Frame(self.progParamFrame,bg=self.backGroundColour)
		self.progParamFrameItemsL.pack(side=LEFT,fill=Y,expand=False)
		self.labelParams[0] = Label(self.progParamFrameItemsL,text="Lower Rate Limit (ppm): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[1] = Label(self.progParamFrameItemsL,text="Upper Rate Limit (ppm): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[2] = Label(self.progParamFrameItemsL,text="Maximum Sensor Rate (ppm): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[3] = Label(self.progParamFrameItemsL,text="Fixed AV Delay (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[4] = Label(self.progParamFrameItemsL,text="Dynamic AV Delay (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[5] = Label(self.progParamFrameItemsL,text="Minimum Dynamic AV Delay (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[6] = Label(self.progParamFrameItemsL,text="Sensed AV Delay Offset (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[7] = Label(self.progParamFrameItemsL,text="Atrial Pulse Amplitude Reg. (V): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[8] = Label(self.progParamFrameItemsL,text="Ventricular Pulse Amplitude Reg. (V): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[9] = Label(self.progParamFrameItemsL,text="Atrial Pulse Amplitude Unreg. (V): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[10] = Label(self.progParamFrameItemsL,text="Ventricular Pulse Amplitude Unreg. (V): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[11] = Label(self.progParamFrameItemsL,text="Atrial Pulse Width (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[12] = Label(self.progParamFrameItemsL,text="Ventricular Pulse Width (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[13] = Label(self.progParamFrameItemsL,text="Atrial Sensitivity (mV): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[14] = Label(self.progParamFrameItemsL,text="Ventricular Sensitivity (mV): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[15] = Label(self.progParamFrameItemsL,text="Ventricular Refractory Period (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[16] = Label(self.progParamFrameItemsL,text="Atrial Refractory Period (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[17] = Label(self.progParamFrameItemsL,text="PVARP (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[18] = Label(self.progParamFrameItemsL,text="PVARP Extension (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[19] = Label(self.progParamFrameItemsL,text="Hysteresis (ppm): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[20] = Label(self.progParamFrameItemsL,text="Rate Smoothing Up (%): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[21] = Label(self.progParamFrameItemsL,text="Rate Smoothing Down (%): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[22] = Label(self.progParamFrameItemsL,text="ATR Duration Cycles (N/A): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[23] = Label(self.progParamFrameItemsL,text="ATR Duration Lower Range: ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[24] = Label(self.progParamFrameItemsL,text="ATR Duration Upper Range: ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[25] = Label(self.progParamFrameItemsL,text="ATR Mode: ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[26] = Label(self.progParamFrameItemsL,text="ATR Fallback Time (min): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[27] = Label(self.progParamFrameItemsL,text="Ventricular Blanking (ms): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[28] = Label(self.progParamFrameItemsL,text="Activity Threshold: ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		
		self.labelParams[29] = Label(self.progParamFrameItemsL,text="Reaction Time (s): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[30] = Label(self.progParamFrameItemsL,text="Response Factor: ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)
		self.labelParams[31] = Label(self.progParamFrameItemsL,text="Recovery Time (min): ",justify=LEFT,bg=self.backGroundColour,font=self.fontLabel)

		#===Parameter Spinboxes===#
		self.progParamFrameItemsR = Frame(self.progParamFrame,bg=self.backGroundColour)
		self.progParamFrameItemsR.pack(side=LEFT,fill=BOTH,expand=True)
		self.spinboxParams[0] = Spinbox(self.progParamFrameItemsR,values=self.lowerRateLimitRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[1] = Spinbox(self.progParamFrameItemsR,values=self.upperRateLimitRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[2] = Spinbox(self.progParamFrameItemsR,values=self.maxSensorRateRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[3] = Spinbox(self.progParamFrameItemsR,values=self.fixedAVDelayRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		
		self.spinboxParams[4] = Spinbox(self.progParamFrameItemsR,values=self.dyanmicAVDelayRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[5] = Spinbox(self.progParamFrameItemsR,values=self.minDynamicAVDelayRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[6] = Spinbox(self.progParamFrameItemsR,values=self.sensedAVDelayOffsetRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[7] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpRegRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		
		self.spinboxParams[8] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpRegRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[9] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpUnregRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[10] = Spinbox(self.progParamFrameItemsR,values=self.avPulseAmpUnregRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[11] = Spinbox(self.progParamFrameItemsR,values=self.avPulseWidthRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		
		self.spinboxParams[12] = Spinbox(self.progParamFrameItemsR,values=self.avPulseWidthRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[13] = Spinbox(self.progParamFrameItemsR,values=self.aSensitivityRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[14] = Spinbox(self.progParamFrameItemsR,values=self.vSensitivityRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[15] = Spinbox(self.progParamFrameItemsR,values=self.VRPRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		
		self.spinboxParams[16] = Spinbox(self.progParamFrameItemsR,values=self.ARPRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[17] = Spinbox(self.progParamFrameItemsR,values=self.pvarpRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[18] = Spinbox(self.progParamFrameItemsR,values=self.pvarpExtensionRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[19] = Spinbox(self.progParamFrameItemsR,values=self.hysRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		
		self.spinboxParams[20] = Spinbox(self.progParamFrameItemsR,values=self.rateSmoothingRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[21] = Spinbox(self.progParamFrameItemsR,values=self.rateSmoothingRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[22] = Spinbox(self.progParamFrameItemsR,values=self.atrDurationCyclesRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[23] = Spinbox(self.progParamFrameItemsR,values=self.atrDurationLowerRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[24] = Spinbox(self.progParamFrameItemsR,values=self.atrDurationUpperRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		
		self.spinboxParams[25] = Spinbox(self.progParamFrameItemsR,values=self.atrFallBackModeRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[26] = Spinbox(self.progParamFrameItemsR,values=self.atrFallBackTimeRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[27] = Spinbox(self.progParamFrameItemsR,values=self.ventricularBlankingRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[28] = Spinbox(self.progParamFrameItemsR,values=self.activityThresholdRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)

		self.spinboxParams[29] = Spinbox(self.progParamFrameItemsR,values=self.reactionTimeRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[30] = Spinbox(self.progParamFrameItemsR,values=self.responseFactorRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)
		self.spinboxParams[31] = Spinbox(self.progParamFrameItemsR,values=self.recoveryTimeRange,bd=self.spinboxBD,width=self.spinboxWidth,justify=self.spinboxJustify,font=self.fontSpinbox)

		self.but_Off.config(relief='sunken')

		#===Log Frame Setup===#
		self.logFrame = Frame(self.root,bg=self.backGroundColour)
		self.logFrame.pack(side=TOP,fill=BOTH,expand=True) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		
		#===Top info bar===#
		self.logInfoFrame = Frame(self.logFrame,bg=self.topFrameColour,bd=4)
		self.logInfoFrame.pack(side = TOP,fill=X,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		self.Info1 = Label(self.logInfoFrame, text="Viewing up to 250 actions in order from most recent to oldest: ",bg=self.topFrameColour,fg=self.textColourLight,font=self.fontMeta)
		self.Info1.pack(side=LEFT) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		self.but1_Exit = Button(self.logInfoFrame,text="Exit",state=NORMAL,command=self.__exit,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but1_Exit.pack(side=RIGHT) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		self.but1_Logout = Button(self.logInfoFrame,text="Logout",state=NORMAL,command=self.__logout,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.but1_Logout.pack(side=RIGHT) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!

		#===Middle Text area===#
		self.logTextFrame = Frame(self.logFrame,bg=self.backGroundColour)
		self.logTextFrame.pack(side=TOP,fill=X,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!

		self.logText = Text(self.logTextFrame,font=self.fontText,bg=self.backGroundColour)
		# self.logText.pack() # DO NOT PACK. PACKING OCCURS IN __show_Log()!!

		self.logFrameScrollbar = Scrollbar(self.logTextFrame,command=self.logText.yview)
		self.logFrameScrollbar.pack(side=RIGHT,fill=Y,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!

		self.logText['yscrollcommand'] = self.logFrameScrollbar.set

		#===Bottom actions bar==#
		self.logInfoActionsFrame = Frame(self.logFrame,bg=self.backGroundColour)
		self.logInfoActionsFrame.pack(side=BOTTOM,fill=X,expand=False) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!
		self.logReturnButton = Button(self.logInfoActionsFrame,text="Return to Main Screen",state=NORMAL,command=self.__show_Main_Frame,bg=self.backGroundColour,fg=self.buttonTextColour,font=self.fontButton)
		self.logReturnButton.pack(side=RIGHT) # DO NOT PACK. PACKING OCCURS IN __show_Log()!!

		self.logFrame.pack_forget()

		self.__welcome_Prompts()
