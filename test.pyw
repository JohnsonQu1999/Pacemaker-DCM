# import tkinter

# class Win(tkinter.Tk):

#     def __init__(self,master=None):
#         tkinter.Tk.__init__(self,master)
#         self.overrideredirect(True)
#         self._offsetx = 0
#         self._offsety = 0
#         self.bind('<Button-1>',self.clickwin)
#         self.bind('<B1-Motion>',self.dragwin)

#     def dragwin(self,event):
#         x = self.winfo_pointerx() - self._offsetx
#         y = self.winfo_pointery() - self._offsety
#         self.geometry('+{x}+{y}'.format(x=x,y=y))

#     def clickwin(self,event):
#         self._offsetx = event.x
#         self._offsety = event.y


# win = Win()
# win.mainloop()

# from tkinter import *

# # pip install pillow
# from PIL import Image, ImageTk

# class Window(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.master = master
#         self.pack(fill=BOTH, expand=1)
        
#         load = Image.open("Pacemaker_512.png")
#         render = ImageTk.PhotoImage(load)
#         img = Label(self, image=render)
#         img.image = render
#         img.place(x=0, y=0)

        
# root = Tk()
# app = Window(root)
# root.wm_title("Tkinter window")
# root.geometry("200x120")
# root.mainloop()

for num in range(28,101):
	print(str(num/10)+",")