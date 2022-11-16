import tkinter as tk
from tkinter import ttk
from tkmacosx import Button

#local
from identifiers import identifiers
from gateway import SendMessage

wasOverwritten = False

master = tk.Tk()
master.geometry("480x200")
master.resizable(False, False)
master.title("Anchored Meeting Light") 


def setStatus(status):
    wasOverwritten = True
    SendMessage(status)

def btnFree():
    setStatus(identifiers["free"])
def btnIdle():
    setStatus(identifiers["idle"])
def btnBusy():
    setStatus(identifiers["busy"])  

label = tk.Label(master, text="Set status:")

imgFree = tk.PhotoImage(file="images/green.png")
imgFreePushed = tk.PhotoImage(file="images/green_pushed.png")
imgIdle = tk.PhotoImage(file="images/orange.png")
imgIdlePushed = tk.PhotoImage(file="images/orange_pushed.png")
imgBusy = tk.PhotoImage(file="images/red.png")
imgBusyPushed = tk.PhotoImage(file="images/red_pushed.png")

defaultColor = master["background"]
btnFree = Button(
    master, 
    image=imgFree, 
    activeimage=imgFreePushed, 
    command=btnFree, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)
btnIdle = Button(
    master, 
    image=imgIdle, 
    activeimage=imgIdlePushed, 
    command=btnIdle, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)
btnBusy = Button(
    master, 
    image=imgBusy, 
    activeimage=imgBusyPushed, 
    command=btnBusy, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)

label2 = tk.Label(master, text="(selecting an option will escape current event)")

#grid
label.grid(row=0,column=0,columnspan=3)
btnFree.grid(row=1,column=0)
btnIdle.grid(row=1,column=1)
btnBusy.grid(row=1,column=2)
label2.grid(row=2,column=0,columnspan = 3)

# mainloop, runs infinitely
master.mainloop()