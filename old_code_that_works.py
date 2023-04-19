import os
import tkinter as tk
from PIL import ImageTk, Image
import ctypes

from functools import partial
#kesha's attempt to open all images in curr directory
# from functools import partial
def buttonClickImages(img_path):
    # images = [file for file in os.listdir(img_path) if file.endswith('.png')] #get list of files that end in .png (these are the images)
    # print(images)
    #open each image
    # for image in images:
    #     print("Inside loop")
    #     os.system("xli " + img_path + "/" +image)



def buttonClickChildDir(path):
    # print("I hate OS")
    new_window = tk.Toplevel(root)
    new_dir = tk.Listbox(new_window)
    for item in os.listdir(path):
        print(item)
        #box to hold the names and icons
        new_frame = tk.Frame(new_dir)
        my_path = os.path.join(path, item)

        #differentiate between files and dirs and change icon accordingly
        if os.path.isdir(my_path):
            icon_label = tk.Label(new_frame, image=dir_icon)
            icon_label.pack(side=tk.LEFT)
            node_label = tk.Label(new_frame, text=item)
            node_label.pack(side=tk.LEFT)
            new_frame.pack()
            new_dir.insert(tk.END, item)
            #can we make it so that it endlessly opens directories-> YES
            # my_path = os.path.join(path, item)
            make_dir_clickable(icon_label, my_path) #idk
        else: #it is a file
                #is it a txt or png?
            if is_image_file(os.path.join(PARENT_DIR, item)):
                #display image icon
                icon_label = tk.Label(new_frame, image=image_icon)
                icon_label.bind("<Button-1>", lambda event, img_path=my_path: buttonClickImages(img_path))
            else:
                icon_label = tk.Label(new_frame, image=file_icon)
                icon_label.bind("<Button-1>", lambda event, txt_path=my_path: buttonClickText(txt_path))
            icon_label.pack(side=tk.LEFT)
            node_label = tk.Label(new_frame, text=item)
            node_label.pack(side=tk.LEFT)
            new_frame.pack()
            new_dir.insert(tk.END, item)
    new_dir.pack()


#labels
labels_for_all_icons = []

#now generalize generalize opening directories
def make_dir_clickable(icon_label, dir_path):
    icon_label.bind("<Button-1>", lambda event: buttonClickChildDir(dir_path))


#START IN PARENT DIR: display the directory contents
starting_dir = tk.Listbox(root)
for item in os.listdir():
    print(item)
    #box to hold the names and icons
    parent_frame = tk.Frame(starting_dir)
    my_path = os.path.join(PARENT_DIR, item)

    #differentiate between files and dirs and change icon accordingly
    if os.path.isdir(item):
        icon_label = tk.Label(parent_frame, image=dir_icon)
        labels_for_all_icons.append(icon_label)
        make_dir_clickable(icon_label, my_path)
    else: #it is a file
        #is it a txt or png?
        if is_image_file(my_path):
            #display image icon
            icon_label = tk.Label(parent_frame, image=image_icon)
            # labels_for_all_icons.append(icon_label)
            icon_label.bind("<Button-1>", lambda event, img_path=os.path.join(PARENT_DIR, item): buttonClickImages(img_path))
        else:
            icon_label = tk.Label(parent_frame, image=file_icon)
            icon_label.bind("<Button-1>", lambda event, txt_path=os.path.join(PARENT_DIR, item): buttonClickText(txt_path))
            # labels_for_all_icons.append(icon_label)
    icon_label.pack(side=tk.LEFT)
    node_label = tk.Label(parent_frame, text=item)
    node_label.pack(side=tk.LEFT)
    parent_frame.pack()
    starting_dir.insert(tk.END, parent_frame)
    # labels_for_all_icons.append(icon_label)


#make new window to open a dir in a new window on click
#labels_for_all_icons[0].bind("<Button-1>", lambda event: buttonClick("/u/miatey/FinalProj/t0.dir/data"))


#open all files in a dir on click
#labels_for_all_icons[4].bind("<Button-1>", lambda event: buttonClickImages("/u/miatey/FinalProj/t0.dir/amongus"))

#start
starting_dir.pack()
root.mainloop()
