from ctypes import cdll
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import time
import json
import os 
root = tk.Tk()
_sopen = cdll.msvcrt._sopen
_close = cdll.msvcrt._close
_SH_DENYRW = 0x10

def getrowcount():
    count = len(open("test.txt").readlines())
    return count
def codetofile(filename,code):
    curfile = open(filename,"w+")
    curfile.write(code)
def fetchcode(filename):
    curfile = open(filename)
    return(curfile.read())
def createcodesnippet(name,code):
    codetofile(name,code)
class codesnippet: #added a class that handles code snippet creation
    def __init__(self,name):
        self.name = name
        self.code = fetchcode(name)

def is_open(filename):
    if not os.access(filename, os.F_OK):
        return False # file doesn't exist
    h = _sopen(filename, 0, _SH_DENYRW, 0)
    if h == 3:
        _close(h)
        return False # file is not opened by anyone else
    return True # file is already open
def refreshTick():
	Luatofile("gameTick = 1","GameTick.lua")
	time.sleep(0.16)
	Luatofile("--gameTick = 1","GameTick.lua")
	return
def Luatofile(source,filename):
	curfilename = open(filename,"w")
	curfilename.write(source)
	curfilename.close()
	return
def executeBtn():
	
	curText=texteditor.get("1.0","end")
	runOncelua=open("RunOnce.lua","w")
	runOncelua.write(curText)
	refreshTick()
	return

def saveascodesnippet(): #the function gets called when save as code snippet button is pressed
    codecontent = texteditor.get("1.0","end")
    codename = simpledialog.askstring(title="Save as code snippet",prompt="filename:")
    createcodesnippet(codename,codecontent)
texteditor=tk.Text(root,height=30,width=80,bg="white")
texteditor.pack(side="left",fill="both", expand=True)

flist = os.listdir() #change stuff inside this for accurate journey stuff, doesn't matter now if you put it under root folder of journey install.
flistbox = tk.Listbox(root)
flistbox.pack(fill="both", expand=True)
m = tk.Menu(root, tearoff = 0)
m.add_command(label ="Cut")
m.add_command(label ="Copy")
m.add_command(label ="Paste")
m.add_command(label ="Reload")
m.add_separator()
m.add_command(label ="Rename")
  
def do_popup(event):
    try:
        flistbox.selection_clear(0,tk.END)
        flistbox.selection_set(flistbox.nearest(event.y))
        flistbox.activate(flistbox.nearest(event.y))
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
  
flistbox.bind("<Button-3>", do_popup)
# Listbox operations
for item in flist:
    flistbox.insert(tk.END, item)
def showcontent(event):
    x = flistbox.curselection()[0]
    file = flistbox.get(x)
    with open(file) as file:
        try:
            file = file.read()
            
        except ValueError:
            messagebox.showerror("Oops!", "Something went wrong while accessing the file. Make sure you have selected a proper text file.")

    texteditor.delete('1.0', tk.END)
    texteditor.insert(tk.END, file)
flistbox.bind("<<ListboxSelect>>", showcontent)
flistscrollbar = tk.Scrollbar(flistbox)
flistscrollbar.pack(side = "right", fill = "both")
flistbox.config(yscrollcommand = flistscrollbar.set)
flistscrollbar.config(command = flistbox.yview)
sendLua = tk.Button(root,text="Execute",padx=40,pady=5,fg="black",bg="gray",command=executeBtn)
savecodeassnippets = tk.Button(root,text="SaveAsSnippet",padx=40,pady=5,fg="black",bg="gray",command=saveascodesnippet)#added a button for saving as code snippet
sendLua.pack(side="right",anchor="s")
savecodeassnippets.pack(side="right",anchor="s")
root.mainloop()
#DOTO: add a table-of-content file for loading settings for individual code snippets when traversing the code snippet directory.Contains required settings for each codesnippet such as name(used to identify the code snippet),
#isLoop(a boolean value that is saved to each code snippet),shortcuts(key shortcut to activate the code)
#to alazar: sry for my broken continuity in coding, its always too late when I try to fix TT
