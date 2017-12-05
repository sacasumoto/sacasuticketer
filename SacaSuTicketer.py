import tkinter as tk
from tkinter import ttk
import os
import time
import TextEditor as te

LARGE_FONT = ("Veranda", 12)
NORM_FONT = ("Veranda",10)
SMALL_FONT = ("Veranda",8)

'''
Choose which one you want to do
between the different ones


'''



def Quit(root):
    os._exit(1)

class Main(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)
        container.pack(side="top",fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.wm_title('SacaSuTicketer')
        self.iconbitmap('ngcc.ico')

        menubar =tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=1)
        filemenu.add_command(label="Exit",command=lambda: Quit(container))
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self,menu=menubar)

        self.frames = {}

        self.frame1 = StartPage(container,self)
        self.frame2 = PageOne(container,self,self.frame1)

        self.frames[StartPage] = self.frame1
        self.frame1.grid(row=0,column=0, sticky="nsew")

        self.frames[PageOne] = self.frame2
        self.frame2.grid(row=0,column=0,sticky="nsew")
        
##        for F in (StartPage,PageOne):
##            
##            frame = F(container,self)
##            self.frames[F] = frame
##            frame.grid(row=0,column=0, sticky ="nsew")

        self.show_frame(StartPage)
                
    def show_frame(self,cont):
            
        frame = self.frames[cont]
##        if cont == PageOne:
##            frame.get_time_invoked()
        frame.tkraise()




class StartPage(tk.Frame,Main):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        mainlabel = ttk.Label(self,text="Main Menu", font=LARGE_FONT)
        mainlabel.grid(row=0,column=0,padx=5,pady=5)

        urllabel = ttk.Label(self,text="Smash.gg URL")
        urllabel.grid(row=1,column=0,padx=5,pady=5)
        self.tourneyURL = tk.StringVar()
        entryURL =ttk.Entry(self,textvariable=self.tourneyURL, width=30)
        entryURL.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        entryURL.focus()


    

        button = ttk.Button(self, text="Recent Results",
                             command=lambda: self.two_things())
        button.grid(row=2,column=1)
        self.controller = controller
        self.variable = ""
        entryURL.bind('<Return>', lambda command: button.invoke())
    def two_things(self):
        self.variable = self.tourneyURL.get()
        self.controller.show_frame(PageOne)


class PageOne(tk.Frame,Main):
    def __init__(self,parent,controller,startPage):
        ttk.Frame.__init__(self,parent)
        
        mainlabel = ttk.Label(self,text="Results Menu", font=LARGE_FONT)
        mainlabel.grid(row=0,column=0,padx=5,pady=5)
 
        startbutton = ttk.Button(self, text="Start",
                                command=lambda:self.start_button())
        startbutton.grid(row=1,column=1,padx=2,pady=2)

        stopbutton = ttk.Button(self, text="Stop",
                               command=lambda:self.stop_button())
        stopbutton.grid(row=1,column=2,padx=2,pady=2)

        gobackbutton = ttk.Button(self, text="Go Back",
                               command=lambda:self.go_back_button())
        gobackbutton.grid(row=1,column=3,padx=2,pady=2)

        self.controller = controller

        self.timer = ttk.Label(self,text="Press Start",font=NORM_FONT)
        self.timer.grid(row=0,column=1, columnspan=2,padx=5,pady=5)

        self.startPage = startPage
        self.url = ""
        self.invoked = 0
        self.buttonpressed = 0

        
    def start_button(self):
        self.get_time_invoked()
        self.buttonpressed = 1
        self.update_clock()
        
    def get_time_invoked(self):
        now = int(time.time())
        self.invoked = now

    def stop_button(self):
        self.buttonpressed = 0

    def go_back_button(self):
        self.buttonpressed = 0
        self.controller.show_frame(StartPage)

#recent_txt(url,time) time = how many seconds threshold for match results to be counted.
#timeleft = how many seconds between updates.
#self.after(1000, xxx) 1000 = 1second or 1000ms
    
    def update_clock(self):
        if self.buttonpressed == 1:
            now = int(time.time())
            seconds = now - self.invoked
            timeleft = 205 - seconds
            if timeleft > -1 and timeleft <= 200:
                timeleft = "Time before update:  " + str(timeleft)
            elif timeleft > 10:
                self.url = self.startPage.variable
                te.recent_txt(self.url,900)
                timeleft = "Updated..."

            elif timeleft == -1:
                timeleft = "Updating..."
                self.get_time_invoked()
            else:
                timeleft = "Starting..."
        else:
            timeleft = "Press Start"
        self.timer.configure(text=timeleft)
        # call this function again in one second
        self.after(1000, self.update_clock)


app = Main()
app.mainloop()
        
