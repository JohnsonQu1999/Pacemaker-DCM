# # # modeDic ={
# # # 	"AOO":"101010",
# # # 	"VOO":"010101"
# # # }

# # # testStr = "hello"
# # # print(testStr[0])
# # # mode = "AOO"
# # # print(modeDic[mode])

# # modeDict = {
# # 	"Off":"0000000000000000000000000",
# # 	"AAT":"1100001010100110000000000",
# # 	"VVT":"1100000101011000000000000",
# # 	"AOO":"1100001010000000000000000",
# # 	"AAI":"1100001010100110110000000",
# # 	"VOO":"1100000101000000000000000",
# # 	"VVI":"1100000101011000110000000",
# # 	"VDD":"1101100101011001011110000",
# # 	"DOO":"1101001111000000000000000",
# # 	"DDI":"1101001111111110000000000",
# # 	"DDD":"1101111111111111111110000",
# # 	"AOOR":"1110001010000000000001111",
# # 	"AAIR":"1110001010100110110001111",
# # 	"VOOR":"1110000101000000000001111",
# # 	"VVIR":"1110000101011000110001111",
# # 	"VDDR":"1111100101011001011111111",
# # 	"DOOR":"1111001111000000000001111",
# # 	"DDIR":"1111001111111110000001111",
# # 	"DDDR":"1111111111111111111111111"
# # }
# # mode = "DDD"

# # for thing in modeDict[mode]:
# # 	print(thing)

# progParam = []

# f=open("defaultUserData.txt","r")
# p1=f.read()
# f.close()

# p2=p1.split(";")

# for i in range(len(p2)):
# 	progParam.append(p2[i].strip().split(","))

# print(progParam)

# testFloat = 3.5
# progParam = ['3.5']

# print(str(float(testFloat)))
# print(str(float(progParam[0])))

# print((float(testFloat)) == (float(progParam[0])))

# from rw import*

# thing = RW()
# # l = ['']
# # print(str(len(l)))
# thing.append_To_Log("6")

# print(thing.get_Logs())

# test = [1,2,3,4]
# # print(test)
# # test = []
# # print(test)
# # test.append(1)
# # print(test)

# tempArray = test
# test = []

# for i in range(1,4):
# 	test.append(tempArray[i])

# print(test)

# from copy import deepcopy

# first = [[1,2],[3,4],[5,6]]
# second = deepcopy(first)

# first[0][0] = 10

# for i in range(len(first)):
# 	print(first[i])
# 	print(second[i])

import tkinter as tk
import random


class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.tx_value = tk.StringVar()
        self.tx_value.set("test")
        self.blink_status = 1

        self.tx_label = tk.Label(self, textvariable=self.tx_value, relief=tk.GROOVE, width=4, height=2)
        self.tx_label.grid(row=0, column=4, sticky=tk.E)
        self.blink_tx()

    def blink_tx_step_2(self, color=None):
        if color != None:
            self.tx_label["bg"] = color
        self.after(3500, self.blink_tx)

    def blink_tx(self):
        if self.blink_status == 1:
            self.tx_label["bg"] = 'green'
            self.tx_value.set('Tx')
            self.blink_status = random.randint(0, 2)
            self.after(1000, self.blink_tx_step_2, 'blue')
        elif self.blink_status == 0:
            self.tx_label["bg"] = 'red'
            self.tx_value.set('*')
            self.blink_status = random.randint(0, 2)
            self.after(2000, self.blink_tx_step_2, 'orange')
        else:
            self.tx_label["bg"] = 'red'
            self.tx_value.set('x')
            self.blink_status = random.randint(0, 2)
            self.after(2000, self.blink_tx_step_2)

app = MainApp()
app.mainloop()