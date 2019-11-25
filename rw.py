#===ABSTRACTION LAYER===#
# Required inputs: mode (read default values or actual values), parameters to save
# Behaviour:
#  - When getting values, try to read from file.txt
#  - If unavailable, return default values
#  - When requested for default values, return them
#  - When parameters are passed, save them by writing to .txt file



# def put_In_Init():
# 	__read_File()
# 	setup_Interface()

#===File I/O Functions===#

class RW():
	def __init__(self):
		self.fileName="file.txt"
		self.defaultFileName="defaultUserData.txt"
		self.logFileName = "log.txt"
		self.maxLogLines = 100
		self.logLines = 0
		self.progParam = []
		
### For Parameters

	def __write_File(self):
		f=open(self.fileName,"w+")

		for i in range(len(self.progParam)):
			for j in range(len(self.progParam[i])):
				f.write(self.progParam[i][j])
				if(j!=len(self.progParam[i])-1):
					f.write(",")
			if(i!=len(self.progParam)-1):
				f.write(";")

		f.close()

	def __read_File(self,mode): # if mode=0, return actual vals; if mode=anything else, return default values
		if(mode==0):
			try:
				self.__read_Actual()
			except:
				self.__read_Default()
		else:
			self.__read_Default()

	def __read_Actual(self):
		f=open(self.fileName,"r")
		p1 = f.read()
		f.close()

		p2 = p1.split(";")

		for i in range(len(p2)):
			self.progParam.append(p2[i].strip().split(","))

	def __read_Default(self):
		f=open(self.defaultFileName,"r")
		p1=f.read()
		f.close()

		p2=p1.split(";")

		for i in range(len(p2)):
			self.progParam.append(p2[i].strip().split(","))

	def get_ProgParam(self,mode): # if mode=0; return actual vals, if mode=anything else, return default
		self.__read_File(mode)
		return self.progParam

	def set_ProgParam(self,param):
		self.progParam = param
		self.__write_File()

### For Logs

	def __read_Logs(self):	
		try:
			f=open(self.logFileName,"r")
			p1=f.read()
			f.close()

			if(p1 != ''):

				# print("__read_Logs: Try1")

				p2=p1.strip().split(";")

				# print("__read_Logs: Try2")

				# print(p2)
				# print(len(p2))

				for i in range(len(p2)):
					self.progParam.append(p2[i].strip())

				# print("__read_Logs: Try 3")

				self.logLines = len(self.progParam)
				# print("__read_Logs: # lines: "+str(self.logLines))
			else:
				self.progParam = []
				self.logLines = len(self.progParam)
		except:
			# print("__read_Logs: Excepted")
			f=open(self.logFileName,"w+")
			f.close()
			progParam = []
			self.logLines = len(progParam)

		# print("__read_Logs: Printing progParam")
		# self.__print_File()

	def __reverse_ProgParamList(self):	# WORKS
		tempArray = self.progParam
		self.progParam = []

		for i in range(self.logLines):
			self.progParam.append(tempArray[self.logLines-1-i])

	def __remove_First_Log_Item(self):	# WORKS
		tempArray = self.progParam
		self.progParam = []

		for i in range(1,self.logLines):
			self.progParam.append(tempArray[i])

	def __write_Logs(self):
		f=open(self.logFileName,"w+")

		# print("__write_Logs: Printing file contents (should be nothing)")
		# self.__print_File()

		for i in range(len(self.progParam)):
			f.write(self.progParam[i])
			if(i!=len(self.progParam)-1):
				f.write(";")

		f.close()

	def get_Logs(self):
		self.__read_Logs()
		self.__reverse_ProgParamList()
		return self.progParam

	def append_To_Log(self,text):	# Writes a string: 'text' to the end of a file.
									# If there are more than 'maxLogLines' lines (defined by #semi colon's +1), delete the first (oldest) line
		self.__read_Logs()

		if(self.logLines >= self.maxLogLines):
			print("append_To_Log: more than 100 lines")
			self.__remove_First_Log_Item()

		# print("append_To_Log: appending string: "+str(text))
		self.progParam.append(str(text))
		# print("append_To_Log: Printing progParam: ")
		# print(self.progParam)
		self.__write_Logs()			

	def __print_File(self):
		print(self.progParam)

# test=RW("file.txt")
# test.__read_File()
# test.__print_File()

# newVar = test.get_ProgParam()
# print(newVar)
# test.set_ProgParam(newVar)
# test.__write_File()
# test.__read_File()
# print("\n\n")
# print(test.get_ProgParam())
