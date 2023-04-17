import os
import tkinter as tk
from PIL import ImageTk, Image

#set dir we want to first open
DIR = '/u/miatey/FinalProj/t0.dir'

#connect to the ext2 file system
os.chdir(DIR)

#create a Tkinter window
root = tk.Tk()

#load dir icon
dir_icon = Image.open('/u/miatey/FinalProj/dir_icon.png')
dir_icon = dir_icon.resize((16, 16))
dir_icon = ImageTk.PhotoImage(dir_icon)

#load file icon
file_icon = Image.open('/u/miatey/FinalProj/file_icon.png')
file_icon = file_icon.resize((16, 16))
file_icon = ImageTk.PhotoImage(file_icon)


#display the directory contents
starting_dir = tk.Listbox(root)
for item in os.listdir():
    #box to hold the names and icons
    hbox = tk.Frame(starting_dir)

    #differentiate between files and dirs and change icon accordingly
    if os.path.isdir(item):
        icon_label = tk.Label(hbox, image=dir_icon)
    else: 
        icon_label = tk.Label(hbox, image=file_icon)
    icon_label.pack(side=tk.LEFT)
    node_label = tk.Label(hbox, text=item)
    node_label.pack(side=tk.LEFT)
    hbox.pack()
    starting_dir.insert(tk.END, hbox)


#start
starting_dir.pack()
root.mainloop()