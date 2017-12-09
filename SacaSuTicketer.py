import tkinter as tk
from tkinter import ttk
import os
import time
import TextEditor as te
import StringExtractor as se

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
        self.frame3 = PageTwo(container,self,self.frame1)
        self.frame4 = PageThree(container,self,self.frame1)
        self.frame5 = PageFour(container,self,self.frame1)
        
        self.frames[StartPage] = self.frame1
        self.frame1.grid(row=0,column=0, sticky="nsew")

        self.frames[PageOne] = self.frame2
        self.frame2.grid(row=0,column=0,sticky="nsew")

        self.frames[PageTwo] = self.frame3
        self.frame3.grid(row=0,column=0,sticky="nsew")

        self.frames[PageThree] = self.frame4
        self.frame4.grid(row=0,column=0,sticky="nsew")

        self.frames[PageFour] = self.frame5
        self.frame5.grid(row=0,column=0,sticky="nsew")

        
        
##        for F in (StartPage,PageOne):
##            
##            frame = F(container,self)
##            self.frames[F] = frame
##            frame.grid(row=0,column=0, sticky ="nsew")

        self.show_frame(StartPage)
                
    def show_frame(self,cont):            
        frame = self.frames[cont]
        frame.tkraise()

    

class StartPage(tk.Frame,Main):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        mainlabel = ttk.Label(self,text="Main Menu", font=LARGE_FONT)
        mainlabel.grid(row=0,column=0,padx=5,pady=5)
        
        urllabel = ttk.Label(self,text="Smash.gg URL", font=NORM_FONT)
        urllabel.grid(row=1,column=0,padx=5,pady=5)
        self.tourneyURL = tk.StringVar()
        entryURL =ttk.Entry(self,textvariable=self.tourneyURL, width=30)
        entryURL.grid(row=1,column=1,columnspan=2,padx=5,pady=5)
        entryURL.focus()

        self.controller = controller
        self.event_name = ""
        self.event_slug = ""
        self.tournament_slug = ""
        
        button = ttk.Button(self, text="Go",
                            command=lambda: button_window(self))
        button.grid(row=2,column=2,padx=5,pady=3)

        button.bind('<Return>', lambda command: button.invoke())


def button_window(startPage):
    popup = tk.Toplevel()
    popup.wm_title("Tournament Events")
    popup.iconbitmap("ngcc.ico")
    title = ttk.Label(popup, text="Choose an Event", font=LARGE_FONT)
    title.grid(row=0,column=0,padx=5,pady=5)
    url = startPage.tourneyURL.get()
    try:
        slug = se.get_tournament_slug_from_smashgg_urls(url)
        startPage.tournament_slug = slug
        event_dict = se.get_tournament_event_slugs(slug)

        i = 1
        for event_name in event_dict:
            button_temp = ttk.Button(popup, text=event_name,
                                     command=lambda event_name=event_name: button_window_function(startPage,
                                                                                                  popup,
                                                                                                  event_name,
                                                                                                  event_dict[event_name]))
            button_temp.grid(row=i,column=0,padx=5,pady=3)
            i += 1
    except:
        title.configure(text="Error, check your link")
        title.grid(row=0,column=0,padx=5,pady=5)
        button = ttk.Button(popup, text="Ok", command=lambda: popup.destroy())
        button.grid(row=1,column=0,padx=5,pady=5)
    popup.grab_set()

def button_window_function(startPage,popup,event_name,event_slug):
    startPage.event_name = event_name
    startPage.event_slug = event_slug
    startPage.controller.frame5.mainlabel.configure(text="Choose a mode for %s" % event_name)
    startPage.controller.show_frame(PageFour)
    popup.grab_release()
    popup.destroy()
                



class PageFour(tk.Frame,Main):
    def __init__(self,parent,controller,startPage):
        ttk.Frame.__init__(self,parent)
        
        
        self.mainlabel = ttk.Label(self,text="", font=LARGE_FONT)
        self.mainlabel.grid(row=0,column=0,padx=5,pady=5,columnspan=3,sticky="w")

        self.controller = controller


        button = ttk.Button(self, text="Recent Results",
                             command=lambda: self.recent_results_button())
        button.grid(row=1,column=3,padx=3,pady=5)

        button1 = ttk.Button(self, text="Upcoming Matches",
                             command=lambda: self.upcoming_results_button())
        button1.grid(row=1,column=2,padx=3,pady=5)

        button2 = ttk.Button(self, text="Ongoing Matches",
                             command=lambda: self.ongoing_results_button())
        button2.grid(row=1,column=1,padx=3,pady=5)

        gobackbutton = ttk.Button(self, text="Go Back",
                               command=lambda:self.go_back_button())
        gobackbutton.grid(row=1,column=0,padx=3,pady=5)


    def recent_results_button(self):
        self.controller.show_frame(PageOne)

    def ongoing_results_button(self):
        self.controller.show_frame(PageTwo)

    def upcoming_results_button(self):
        self.controller.show_frame(PageThree)

    def go_back_button(self):
        self.controller.show_frame(StartPage)


class PageOne(tk.Frame,Main):
    def __init__(self,parent,controller,startPage):
        ttk.Frame.__init__(self,parent)
        
        mainlabel = ttk.Label(self,text="Recent Results Menu", font=LARGE_FONT)
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


        
        self.invoked = 0
        self.update_after = None

        startbutton.bind('<Return>', lambda command: startbutton.invoke())
        stopbutton.bind('<Escape>', lambda command: stopbutton.invoke())
        gobackbutton.bind('<BackSpace>', lambda command: gobackbutton.invoke())

        
    def start_button(self):
        self.get_time_invoked()
        self.update_clock()
        
    def get_time_invoked(self):
        now = int(time.time())
        self.invoked = now

    def stop_button(self):
        self.after_cancel(self.update_after)
        self.timer.configure(text="Stopping..")
        self.after(1000, self.timer.configure(text="Press Start"))


    def go_back_button(self):
        self.after_cancel(self.update_after)
        self.controller.show_frame(PageFour)
        self.after(1000, self.timer.configure(text="Press Start"))


#recent_txt(url,time) time = how many seconds threshold for match results to be counted.
#timeleft = how many seconds between updates.
#self.after(1000, xxx) 1000 = 1second or 1000ms
    
    def update_clock(self):
        now = int(time.time())
        seconds = now - self.invoked
        timeleft = 205 - seconds
        if timeleft > -1 and timeleft <= 200:
            timeleft = "Time before update:  " + str(timeleft)
        elif timeleft > 200:
            slug = self.startPage.tournament_slug
            event_slug = self.startPage.event_slug
            te.recent_txt(slug, event_slug,900)
            timeleft = "Updated..."

        elif timeleft == -1:
            timeleft = "Updating..."
            self.get_time_invoked()
        else:
            timeleft = "Starting..."
        self.timer.configure(text=timeleft)
        # call this function again in one second
        self.update_after = self.after(1000, self.update_clock)




class PageTwo(tk.Frame,Main):
    def __init__(self,parent,controller,startPage):
        ttk.Frame.__init__(self,parent)
        
        mainlabel = ttk.Label(self,text="Ongoing Matches Menu", font=LARGE_FONT)
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
        self.update_after = None

        startbutton.bind('<Return>', lambda command: startbutton.invoke())
        stopbutton.bind('<Escape>', lambda command: stopbutton.invoke())
        gobackbutton.bind('<BackSpace>', lambda command: gobackbutton.invoke())

        
    def start_button(self):
        self.get_time_invoked()
        self.update_clock()
        
    def get_time_invoked(self):
        now = int(time.time())
        self.invoked = now

    def stop_button(self):
        self.after_cancel(self.update_after)
        self.timer.configure(text="Stopping..")
        self.after(1000, self.timer.configure(text="Press Start"))

    def go_back_button(self):
        self.after_cancel(self.update_after)
        self.controller.show_frame(PageFour)
        self.after(1000, self.timer.configure(text="Press Start"))


#recent_txt(url,time) time = how many seconds threshold for match results to be counted.
#timeleft = how many seconds between updates.
#self.after(1000, xxx) 1000 = 1second or 1000ms
    
    def update_clock(self):
        now = int(time.time())
        seconds = now - self.invoked
        timeleft = 205 - seconds
        if timeleft > -1 and timeleft <= 200:
            timeleft = "Time before update:  " + str(timeleft)
        elif timeleft > 200:
            slug = self.startPage.tournament_slug
            event_slug = self.startPage.event_slug
            te.ongoing_txt(slug, event_slug)
            timeleft = "Updated..."

        elif timeleft == -1:
            timeleft = "Updating..."
            self.get_time_invoked()
        else:
            timeleft = "Starting..."


        self.timer.configure(text=timeleft)
        # call this function again in one second
        self.update_after = self.after(1000, self.update_clock)



class PageThree(tk.Frame,Main):
    def __init__(self,parent,controller,startPage):
        ttk.Frame.__init__(self,parent)
        
        mainlabel = ttk.Label(self,text="Upcoming Matches Menu", font=LARGE_FONT)
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
        self.update_after = None

        startbutton.bind('<Return>', lambda command: startbutton.invoke())
        stopbutton.bind('<Escape>', lambda command: stopbutton.invoke())
        gobackbutton.bind('<BackSpace>', lambda command: gobackbutton.invoke())

        
    def start_button(self):
        self.get_time_invoked()
        self.update_clock()
        
    def get_time_invoked(self):
        now = int(time.time())
        self.invoked = now

    def stop_button(self):
        self.after_cancel(self.update_after)
        self.timer.configure(text="Stopping..")
        self.after(1000, self.timer.configure(text="Press Start"))

    def go_back_button(self):
        self.after_cancel(self.update_after)
        self.controller.show_frame(PageFour)
        self.after(1000, self.timer.configure(text="Press Start"))

#recent_txt(url,time) time = how many seconds threshold for match results to be counted.
#timeleft = how many seconds between updates.
#self.after(1000, xxx) 1000 = 1second or 1000ms
    
    def update_clock(self):
        now = int(time.time())
        seconds = now - self.invoked
        timeleft = 205 - seconds
        if timeleft > -1 and timeleft <= 200:
            timeleft = "Time before update:  " + str(timeleft)
        elif timeleft > 200:
            slug = self.startPage.tournament_slug
            event_slug = self.startPage.event_slug
            te.upcoming_txt(slug, event_slug)
            timeleft = "Updated..."

        elif timeleft == -1:
            timeleft = "Updating..."
            self.get_time_invoked()
        else:
            timeleft = "Starting..."

        self.timer.configure(text=timeleft)
        # call this function again in one second
        self.update_after = self.after(1000, self.update_clock)








app = Main()
app.mainloop()
        
