import tkinter as tk
from tkinter import ttk
from tkmacosx import Button

#local
from identifiers import identifiers
from gateway import SendMessage
from arpy import scan_subnet_for_hosts

def setStatus(status):
    wasOverwritten = True
    SendMessage(status)
def btnFree():
    setStatus(identifiers["free"])
def btnIdle():
    setStatus(identifiers["idle"])
def btnBusy():
    setStatus(identifiers["busy"])  
def btnArpy():
    scan_subnet_for_hosts()

root = tk.Tk()
root.wm_geometry("480x240")
root.resizable(False, False)
root.title("Anchored Meeting Light") 

statusSelectionFrame = tk.Frame(root)
statusSelectionFrame.pack(side="top", fill="both", expand=True)
statusSelectionFrame.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

arpyFrame = tk.Frame(root)
arpyFrame.pack(side="top", fill="both", expand=True)
arpyFrame.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

imgFree = tk.PhotoImage(file="images/green.png")
imgFreePushed = tk.PhotoImage(file="images/green_pushed.png")
imgIdle = tk.PhotoImage(file="images/orange.png")
imgIdlePushed = tk.PhotoImage(file="images/orange_pushed.png")
imgBusy = tk.PhotoImage(file="images/red.png")
imgBusyPushed = tk.PhotoImage(file="images/red_pushed.png")
imgArpy = tk.PhotoImage(file="images/antenna.png")
imgBack = tk.PhotoImage(file="images/back.png")

defaultColor = statusSelectionFrame["background"]
btnFree = Button(
    statusSelectionFrame, 
    image=imgFree, 
    activeimage=imgFreePushed, 
    command=btnFree, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)
btnIdle = Button(
    statusSelectionFrame, 
    image=imgIdle, 
    activeimage=imgIdlePushed, 
    command=btnIdle, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)
btnBusy = Button(
    statusSelectionFrame, 
    image=imgBusy, 
    activeimage=imgBusyPushed, 
    command=btnBusy, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor
)
btnArpy = Button(
    statusSelectionFrame, 
    image=imgArpy, 
    command=arpyFrame.lift, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
    width=30,
    height=30
)

label = tk.Label(statusSelectionFrame, text="Set status:")
label2 = tk.Label(statusSelectionFrame, text="(selecting an option will escape current event)")

btnArpy.grid(in_=statusSelectionFrame,row=1,column=0,columnspan=1,sticky="w")
label.grid(in_=statusSelectionFrame,row=1,column=1,columnspan=1)
btnFree.grid(in_=statusSelectionFrame,row=2,column=0)
btnIdle.grid(in_=statusSelectionFrame,row=2,column=1)
btnBusy.grid(in_=statusSelectionFrame,row=2,column=2)
label2.grid(in_=statusSelectionFrame,row=3,column=0,columnspan = 3)

#ARPY
lbxDevices = tk.Listbox(arpyFrame, height = 7, width=30)

def reloadDevices():
    lbxDevices.delete(0, lbxDevices.size()-1)
    scan_subnet_for_hosts()
    lbxDevices()

def loadDevices():    
    devices = []
    for device in open("./bin/addresses.txt", "r"):
        devices.append(device)
    deviceCount = len(devices)
    if deviceCount == 0:
        lbxDevices.insert('end', "No devices found...")
    else:
        for device in devices:
            lbxDevices.insert('end',device)

lblDevices = tk.Label(arpyFrame, text="Devices:")
btnReload = Button(arpyFrame, text="Reload", command=reloadDevices)
btnStatusSelection = Button(
    arpyFrame, 
    image=imgBack, 
    command=statusSelectionFrame.lift, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
    width=30,
    height=30
)
btnStatusSelection.grid(row=1,column=0)
lblDevices.grid(row=1,column=1,padx=60)
lbxDevices.grid(row=2,column=1,padx=60)
btnReload.grid(row=3,column=1,padx=60, pady=20)


if __name__ == "__main__":
    statusSelectionFrame.lift()
    loadDevices()
    root.mainloop()
