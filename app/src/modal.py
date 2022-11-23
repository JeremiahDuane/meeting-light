#LIBRARIES
import tkinter as tk
from tkinter import ttk, filedialog
from tkmacosx import Button

#LOCAL
from config import Identifiers, Port
from gateway import SendMessage
from arpy import ScanSubnetForHosts, SaveHosts

IMAGE_DIRECTORY = "images"

#NEW WINDOW
root = tk.Tk()
root.wm_geometry("490x245")
root.resizable(False, False)
root.title("Anchored Meeting Light") 

#FRAMES
frameStatusSelection = tk.Frame(root)
frameStatusSelection.pack(side="top", fill="both", expand=True)
frameStatusSelection.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

frameArpy = tk.Frame(root)
frameArpy.pack(side="top", fill="both", expand=True)
frameArpy.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

frameDirectories = tk.Frame(root)
frameDirectories.pack(side="top", fill="both", expand=True)
frameDirectories.place(in_=root, x=0, y=0, relwidth=1, relheight=1)

defaultColor = frameStatusSelection["background"]

#STATUS SELECTION FRAME
def setStatus(status):
    SendMessage(status)

def btnFree():
    setStatus(Identifiers["free"])
def btnIdle():
    setStatus(Identifiers["idle"])
def btnBusy():
    setStatus(Identifiers["busy"])  
def btnArpy():
    ScanSubnetForHosts()

##define labels for the status selection frame
label = tk.Label(frameStatusSelection, text="Set status:")
label2 = tk.Label(frameStatusSelection, text="(selecting an option will escape current event)")

##define images for each button in active and inactive states
imgFree = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/green.png")
imgFreePushed = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/green_pushed.png")
imgIdle = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/orange.png")
imgIdlePushed = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/orange_pushed.png")
imgBusy = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/red.png")
imgBusyPushed = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/red_pushed.png")
imgArpy = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/antenna.png")
imgDirectory = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/folder.png")

##define buttons
btnFree = Button(
    frameStatusSelection, 
    image=imgFree, 
    activeimage=imgFreePushed, 
    command=btnFree, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)
btnIdle = Button(
    frameStatusSelection, 
    image=imgIdle, 
    activeimage=imgIdlePushed, 
    command=btnIdle, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
)
btnBusy = Button(
    frameStatusSelection, 
    image=imgBusy, 
    activeimage=imgBusyPushed, 
    command=btnBusy, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor
)
btnArpy = Button(
    frameStatusSelection, 
    image=imgArpy, 
    command=frameArpy.lift, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
    width=30,
    height=30
)
btnDirectories = Button(
    frameStatusSelection, 
    image=imgDirectory, 
    command=frameDirectories.lift, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
    width=30,
    height=30
)
##place components in grid
btnDirectories.grid(in_=frameStatusSelection,row=1,column=0,columnspan=1,sticky="w")
btnArpy.grid(in_=frameStatusSelection,row=1,column=2,columnspan=1,sticky="e")
label.grid(in_=frameStatusSelection,row=1,column=1,columnspan=1)
btnFree.grid(in_=frameStatusSelection,row=2,column=0)
btnIdle.grid(in_=frameStatusSelection,row=2,column=1)
btnBusy.grid(in_=frameStatusSelection,row=2,column=2)
label2.grid(in_=frameStatusSelection,row=3,column=0,columnspan = 3)

#ARPY FRAME
def ReloadDevices():
    lbxDevices.delete(0, lbxDevices.size()-1)
    hosts = ScanSubnetForHosts()
    SaveHosts(hosts)
    InsertDevices(hosts)
def InsertDevices(devices):   
    deviceCount = len(devices)
    if deviceCount == 0:
        lbxDevices.insert('end', "No devices found...")
    else:
        for device in devices:
            lbxDevices.insert('end',device)
def InitDeviceListbox():
    devices = []
    for device in open("./bin/addresses.txt", "r"):
        devices.append(device)
    InsertDevices(devices)

##define labels for arpy frame
lblDevices = tk.Label(frameArpy, text="Devices:")

##define listbox for arpy frame
lbxDevices = tk.Listbox(frameArpy, height = 7, width=30)

##define images for back button
imgBack = tk.PhotoImage(file=f"{IMAGE_DIRECTORY}/back.png")

##define buttons for arpy frame
btnReload = Button(
    frameArpy, 
    text="Reload", 
    command=ReloadDevices
)
btnStatusSelection1 = Button(
    frameArpy, 
    image=imgBack, 
    command=frameStatusSelection.lift, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
    width=30,
    height=30
)

##place components in grid
btnStatusSelection1.grid(row=1,column=0)
lblDevices.grid(row=1,column=1,padx=60)
lbxDevices.grid(row=2,column=1,padx=60)
btnReload.grid(row=3,column=1,padx=60, pady=20)

#DIRECTORIES FRAME
def SelectDirectory():
    file = filedialog.askdirectory(parent=root,title='Choose a folder')
    SaveDirectory(file)
    print(file)

def SaveDirectory(dir):
    with open("./bin/directories.txt", "a") as f:
        f.write(f"{dir}\n")
    lbxDirectories.insert("end", dir)

def InitDirectoryListbox():
    for path in open("./bin/directories.txt", "r"):
        lbxDirectories.insert("end", path)

def ClearDirectories():
    open("./bin/directories.txt", "w").close()
    lbxDirectories.delete(0, lbxDirectories.size()-1)

##define labels for arpy frame
lblDirectories = tk.Label(frameDirectories, text="Directories:")

##define listbox for arpy frame
lbxDirectories = tk.Listbox(frameDirectories, height = 7, width=30)

##define buttons for arpy frame
btnSelectDirectory = Button(
    frameDirectories, 
    text="    ADD PATH    ", 
    command=SelectDirectory
)
btnClearDirectories = Button(
    frameDirectories, 
    text="       CLEAR        ", 
    command=ClearDirectories
)
btnStatusSelection2 = Button(
    frameDirectories, 
    image=imgBack, 
    command=frameStatusSelection.lift, 
    bd=10, 
    activebackground=defaultColor, 
    bg=defaultColor,
    width=30,
    height=30
)

##place components in grid
btnStatusSelection2.grid(row=0,column=0, columnspan=1)
lblDirectories.grid(row=0,column=1,padx=60)
lbxDirectories.grid(row=1,column=1,padx=60)
btnSelectDirectory.grid(row=2,column=1,columnspan=1, padx=(0, 140), pady=10)
btnClearDirectories.grid(row=2,column=1, columnspan=1,padx=(140, 0), pady=10)


#MAIN
def Modal():
    frameStatusSelection.lift()
    InitDeviceListbox()
    InitDirectoryListbox()
    root.mainloop()
    
if __name__ == "__main__":
    Modal()