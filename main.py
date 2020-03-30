from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image
import tkinter.font as font
from array import *
from pynput.keyboard import Key, Listener
import os
from multiprocessing import Process
import pickle
import numpy as np
import cv2
from time import sleep

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.currentButtonEngage = -1
        self.master.bind_all('<Key>', self.key)

        #widgets can take whole window
        self.pack(fill=BOTH, expand=1)
        self.w, self.h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry("%dx%d" % (self.w, self.h))
        self.image =Image.open('C:\\my_data\\robotics\\Windows_Multitasker\\assets\\main_bg.jpg')
        self.image = self.image.resize((self.w,self.h ))
        self.bg_image = ImageTk.PhotoImage(self.image)
        self.c = Canvas(self, bg="#1f1f1f", height=self.h, width=self.w)
        self.c.pack(expand=YES, fill=BOTH)
        self.Home()


    def Home(self, Master = None):
        try:
            os.remove('smart_open.txt')
        except:
            print("NO such file found")

        with open("smart_open.txt", "w") as myfile:
            myfile.write("SMART_OPEN=0")
            myfile.close()

        self.c.create_image(0, 0, image = self.bg_image, anchor=NW)
        self.transparentImageButton = Button(self, text="Remove background ", height = "2",width = "16",bd = 0,wraplength = "200",fg = "white",activeforeground="white",bg = "#6699ff",activebackground='#6699ff',command=self.bgRemove)
        self.transparentImageButton.place(x=200, y=120)
        self.transparentImageButton['font'] = font.Font(size = 14)

        self.smartKeyButton = Button(self, text="Smartkeys", height = "2",width = "16",bd = 0,wraplength = "100",fg = "white",activeforeground="white",bg = "#6699ff",activebackground='#6699ff',command=self.smartKeys)
        self.smartKeyButton.place(x=1000, y=115)
        self.smartKeyButton['font'] = font.Font(size = 14)

    def bgRemove(self):
        self.transparentImageButton.destroy()
        self.smartKeyButton.destroy()
        self.c.delete('all')
        self.image =Image.open('C:\\my_data\\robotics\\Windows_Multitasker\\assets\\tr_bg.jpg')
        self.image = self.image.resize((self.w,self.h ))
        self.smart_bg_image = ImageTk.PhotoImage(self.image)
        self.c.create_image(0, 0, image = self.smart_bg_image, anchor=NW)
        self.c.bind("<Button 1>", self.checkCoordinates)
        self.tr_backButton = Button(self, text = "Back", width = 7,bd = 3,highlightbackground = "orange",font = font.Font(size = 14), bg = "white", fg = "black",command = self.tr_back)
        self.tr_backButton.place(x = 10, y = 10)
        self.tr_label = Label(self, text = "",width = 70,height = 2,highlightthickness= 3,highlightbackground = "black",font = font.Font(size = 14), bg = "white", fg = "black")
        self.tr_label.place(x = 50, y = 250)

    def checkCoordinates(self, event):
        if event.x >= 902 and event.x <= 930 and event.y > 260 and event.y < 300:
            self.tr_browseFunction()
        if event.x >= 900 and event.x <= 930 and event.y > 575 and event.y < 608:
            filepath = self.tr_label.cget('text')
            if filepath != "" and filepath != "Its not the right filetype. expected jpg,png or jpeg":
                self.tr_label.config(text = "processing image", fg = "blue")
                img = cv2.imread(filepath)
                print(img)
                mask = np.zeros(img.shape[:2],np.uint8)

                bgdModel = np.zeros((1,65),np.float64)
                fgdModel = np.zeros((1,65),np.float64)

                rect = (1,1,665,344)
                cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

                mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                img = img*mask2[:,:,np.newaxis]

                tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
                b, g, r = cv2.split(img)
                rgba = [b,g,r, alpha]
                dst = cv2.merge(rgba,4)
                print(filepath.split("\\")[len(filepath.split("\\")) - 1].split(".")[0] + ".png")
                cv2.imwrite(filepath.split("\\")[len(filepath.split("\\")) - 1].split(".")[0] + ".png", dst)
                sleep(0.2)
                self.tr_label.config(text = "Done boss!", fg = "green")

    def tr_browseFunction(self):
        filename = filedialog.askopenfilename()
        img_type = ["jpeg", "jpg","png"]
        if filename != "":
            if(filename.split(".")[1] not in img_type):
                self.tr_label.config(text = "Its not the right filetype. expected jpg,png or jpeg", fg = "red")
            else:
                self.tr_label.config(text =filename, fg = "black")

    def tr_back(self):
        self.c.delete('all')
        self.tr_backButton.destroy()
        self.tr_label.destroy()
        self.Home()

    def smartKeys(self, master = None):
        with open("smart_open.txt", "w") as myfile:
            myfile.write("SMART_OPEN=1")
            myfile.close()

        self.transparentImageButton.destroy()
        self.smartKeyButton.destroy()
        self.c.delete('all')

        self.image =Image.open('C:\\my_data\\robotics\\Windows_Multitasker\\assets\\smart_bg.jpg')
        self.image = self.image.resize((self.w,self.h ))
        self.smart_bg_image = ImageTk.PhotoImage(self.image)
        self.c.create_image(0, 0, image = self.smart_bg_image, anchor=NW)
        self.smart_backButton = Button(self, text = "Back", width = 7,font = font.Font(size = 14),fg = "white",activeforeground="white",bg = "#6699ff",activebackground='#6699ff',command = self.smart_back)
        self.smart_backButton.place(x = 10, y = 10)

        self.smartFrame = Frame(self.c)
        self.smartFrame.bind("<Button-1>",self.smartCheck)
        self.smart_window = self.c.create_window((230, 140), height = "440",width = "820",anchor='nw',window=self.smartFrame)
        self.shiftLabel = list()
        self.shiftButton = list()
        self.smartFileopenButton = list()
        self.shiftButtonToggle = [0, 0 ,0 ,0 , 0, 0]
        self.smart_path = ["","","","","","",""]
        self.smart_key = ["","","","","","",""]
        y1 = 20
        with open("var.txt", "r") as myfile:
            i = 0
            for line in myfile:
                if i < 6 and line != "\n":
                    data = line.split("=")
                    print(data, "    ",i)
                    self.smart_key[i] = data[0]
                    self.smart_path[i] = data[1].split('\n')[0]
                    i = i + 1
            myfile.close()

        for i in range(0, 6):
            self.shiftLabel.append( Label(self.smartFrame, text = "Alt_left ",width = 8,height = 2,font = font.Font(size = 14), bg = "black", fg = "white"))
            self.shiftButton.append( Button(self.smartFrame, text = self.smart_key[i], width = 10,font = font.Font(size = 17), bg = "black", fg = "white"))
            self.smartFileopenButton.append( Button(self.smartFrame, text = self.smart_path[i],width = 20,font = font.Font(size = 17), bg = "black", fg = "white"))
            self.shiftLabel[i].place(x = 30, y = y1 )
            self.shiftButton[i].place(x = 250, y = y1 )
            self.smartFileopenButton[i].place(x = 500, y = y1)
            y1 = y1 + 70
        self.shiftButton[0].bind("<Button-1>", lambda event,a = 0:self.smartButton_bg_change(a))
        self.shiftButton[1].bind("<Button-1>", lambda event,a = 1:self.smartButton_bg_change(a))
        self.shiftButton[2].bind("<Button-1>", lambda event, a = 2:self.smartButton_bg_change(a))
        self.shiftButton[3].bind("<Button-1>", lambda event, a = 3:self.smartButton_bg_change(a))
        self.shiftButton[4].bind("<Button-1>", lambda event, a = 4:self.smartButton_bg_change(a))
        self.shiftButton[5].bind("<Button-1>", lambda event, a = 5:self.smartButton_bg_change(a))

        self.smartFileopenButton[0].bind("<Button-1>", lambda event,a = 0:self.smart_browseFunction(a))
        self.smartFileopenButton[1].bind("<Button-1>", lambda event,a = 1:self.smart_browseFunction(a))
        self.smartFileopenButton[2].bind("<Button-1>", lambda event,a = 2:self.smart_browseFunction(a))
        self.smartFileopenButton[3].bind("<Button-1>", lambda event,a = 3:self.smart_browseFunction(a))
        self.smartFileopenButton[4].bind("<Button-1>", lambda event,a = 4:self.smart_browseFunction(a))
        self.smartFileopenButton[5].bind("<Button-1>", lambda event,a = 5:self.smart_browseFunction(a))
        try:
            os.remove('var.txt')
        except:
            print('file do not exist')
        with open("var.txt", "w") as myfile:
            for i in range(0, 6):
                data = self.shiftButton[i].cget('text') + "=" + self.smartFileopenButton[i].cget('text') + "\n"
                myfile.write(data)

            myfile.close()

    def smartButton_bg_change(self, a):
        for i in range(0, 6):
            if i != a:
                self.shiftButtonToggle[i] = 0
                self.shiftButton[i].config(bg="black", fg = "white")
            else:
                self.shiftButtonToggle[i] = 1
                self.currentButtonEngage = i
                self.shiftButton[i].config(bg="white", fg = "black")

    def smart_browseFunction(self, a):
        print(a)
        filename = filedialog.askopenfilename()
        if filename != "":
            self.smart_path[a] = filename
            self.smartFileopenButton[a].config(text = self.smart_path[a], height = 2,width = 29,font = font.Font(size = 12))
        try:
            os.remove('var.txt')
        except:
            print('file do not exist')
        with open("var.txt", "w") as myfile:
            for i in range(0, 6):
                data = self.shiftButton[i].cget('text') + "=" + self.smartFileopenButton[i].cget('text') + "\n"
                myfile.write(data)
            myfile.close()

    def smartCheck(self, event):
        print(self.currentButtonEngage)
        if self.currentButtonEngage != -1:
            self.shiftButton[self.currentButtonEngage].config(bg = "black", fg = "white")
            self.currentButtonEngage = -1

    def key(self, event):
        for i in range(0, 6):
            if self.shiftButtonToggle[i] == 1:
                self.currentButtonEngage = i
                break
        if(self.currentButtonEngage != -1):
            if event.keysym != "Escape":
                self.shiftButton[self.currentButtonEngage].config(text = event.keysym)

            else:
                self.shiftButton[self.currentButtonEngage].config(text = "")
                self.smartFileopenButton[self.currentButtonEngage].config(text = "Browse", height = 1,width = 20,font = font.Font(size = 17))
        try:
            os.remove('var.txt')
        except:
            print('file do not exist')
        with open("var.txt", "w") as myfile:
            for i in range(0, 6):
                data = self.shiftButton[i].cget('text') + "=" + self.smartFileopenButton[i].cget('text') + "\n"
                myfile.write(data)
            myfile.close()

    def smart_back(self):

        try:
            os.remove('smart_open.txt')
        except:
            print("NO such file found")

        with open("smart_open.txt", "w") as myfile:
            myfile.write("SMART_OPEN=0")
            myfile.close()
        self.c.delete('all')
        self.smart_backButton.destroy()
        self.Home()

def func1():
    # initialize tkinter
    root = Tk()
    app = Window(root)

    root.wm_title("Ismart Rock")
    # show window
    root.mainloop()

def func2():
    os.system('keylogger.py')
    print("hello")

if __name__ == '__main__':
  p1 = Process(target=func1)
  p1.start()
  p2 = Process(target=func2)
  p2.start()
  p1.join()
  p2.join()
