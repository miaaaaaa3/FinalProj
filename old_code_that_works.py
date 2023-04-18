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


from functools import partial
def buttonClick(path):
    print("I hate OS")
    new_window = tk.Toplevel(root)
    new_dir = tk.Listbox(new_window)
    for item in os.listdir(path):
        print(item)
        #box to hold the names and icons
        new_frame = tk.Frame(new_dir)

        #differentiate between files and dirs and change icon accordingly
        if os.path.isdir(item):
            icon_label = tk.Label(new_frame, image=dir_icon)
            icon_label.pack(side=tk.LEFT)
            node_label = tk.Label(new_frame, text=item)
            node_label.pack(side=tk.LEFT)
            new_frame.pack()
            new_dir.insert(tk.END, item)
        else:
            icon_label = tk.Label(new_frame, image=file_icon)
            icon_label.pack(side=tk.LEFT)
            node_label = tk.Label(new_frame, text=item)
            node_label.pack(side=tk.LEFT)
            new_frame.pack()
            new_dir.insert(tk.END, item)
    new_dir.pack()


#kesha's attempt to open all images in curr directory
from functools import partial
def buttonClickImages(img_path):
    images = [file for file in os.listdir(img_path) if file.endswith('.png')] #get list of files that end in .png (these are the images)
    print(images)
    #open each image
    for image in images:
        print("Inside loop")
        os.system("xli " + img_path + "/" +image)


#labels
labels_for_all_icons = []


#display the directory contents
starting_dir = tk.Listbox(root)
for item in os.listdir():
    print(item)
    #box to hold the names and icons
    hbox = tk.Frame(starting_dir)

    #differentiate between files and dirs and change icon accordingly
    if os.path.isdir(item):
        icon_label = tk.Label(hbox, image=dir_icon)
        # icon_label.bind("<Button-1>", lambda event: buttonClick(item))
    else: 
        icon_label = tk.Label(hbox, image=file_icon)
    icon_label.pack(side=tk.LEFT)
    #to do later: 
    # icon_label.bind("<Button-1>", buttonClick)
    node_label = tk.Label(hbox, text=item)
    node_label.pack(side=tk.LEFT)
    hbox.pack()
    starting_dir.insert(tk.END, hbox)
    labels_for_all_icons.append(icon_label)

#make new window to open a dir in a new window on click
labels_for_all_icons[1].bind("<Button-1>", lambda event: buttonClick("/u/miatey/FinalProj/t0.dir/data"))
#open all files in a dir on click
labels_for_all_icons[4].bind("<Button-1>", lambda event: buttonClickImages("/u/miatey/FinalProj/t0.dir/amongus"))



#kesha's attempt to open an image w/ xli
#os.system("xli " + '/u/miatey/FinalProj/dir_icon.png')




#start
starting_dir.pack()
root.mainloop()
