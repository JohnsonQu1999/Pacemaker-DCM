import serial

import struct
import subprocess


#Check if board is connected function



class Serial():
	def checksend(self, modearr, pararr):
		if self.checkConnection()==0:
			self.concat(modearr, pararr)
			return 0
		return -1


	def checkConnection(self):
		MyOut = subprocess.Popen('python -m serial.tools.list_ports 1366:1015 -q', 
		            stdout=subprocess.PIPE, 
		            stderr=subprocess.STDOUT)
		stdout,stderr = MyOut.communicate()
		print(stdout)
		if stdout == (b'COM4                \r\n'):
			#call writing function
			print("connected")
			return 0
			
		else: 
			print('board not found')
			return -1

	def concat(self, modearr, pararr):
		modearr.extend(pararr)
		self.getParity(modearr)

	def send(self, pararr):
		port = "COM4"
		ser = serial.Serial(port, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0)
		packet = bytearray() 
		for i in range(len(pararr)):
			packet.append(pararr[i])

		print(ser.isOpen())
		print(packet)
		ser.write(packet)
		ser.close()
		print("done")

	def getParity(self, pararr):
		count = 0
		for i in range(len(pararr)):
			count = count + bin(pararr[i]).count('1') #parity bit = 1 when odd number of ones
		print(count)
		count = count%2
		if count == 1:
			parity = [255]
		else:
			parity = [0]
		parity.extend(pararr)
		print(parity)
		self.send(parity)

