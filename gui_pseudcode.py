import os
import tkinter as tk
from PIL import ImageTk, Image

# Connect to the ext2 file system
os.chdir('/path/to/directory')

# Load the file icon image
file_icon = Image.open('/path/to/file_icon.png')
file_icon = file_icon.resize((16, 16))
file_icon = ImageTk.PhotoImage(file_icon)

# Create a Tkinter window
root = tk.Tk()

# Create a listbox widget to display the directory contents
listbox = tk.Listbox(root)
for item in os.listdir():
    # Create a horizontal box to hold the file icon and filename
    hbox = tk.Frame(listbox)
    icon_label = tk.Label(hbox, image=file_icon)
    icon_label.pack(side=tk.LEFT)
    filename_label = tk.Label(hbox, text=item)
    filename_label.pack(side=tk.LEFT)
    hbox.pack()
    listbox.insert(tk.END, hbox)

# Pack the listbox widget and start the main loop
listbox.pack()
root.mainloop()
