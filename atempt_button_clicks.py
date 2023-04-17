import os
import tkinter as tk
from PIL import ImageTk, Image

# Set the directory we want to first open
DIR = '/u/miatey/FinalProj/t0.dir'

# Connect to the ext2 file system
os.chdir(DIR)

# Create a Tkinter window
root = tk.Tk()

# Load the directory icon
dir_icon = Image.open('/u/miatey/FinalProj/dir_icon.png')
dir_icon = dir_icon.resize((16, 16))
dir_icon = ImageTk.PhotoImage(dir_icon)

# Load the file icon
file_icon = Image.open('/u/miatey/FinalProj/file_icon.png')
file_icon = file_icon.resize((16, 16))
file_icon = ImageTk.PhotoImage(file_icon)

# Create a frame to hold the icons and file names
frame = tk.Frame(root)

# Define a function to list the contents of a directory
def list_directory(directory):
    return os.listdir(directory)

# Define a function to display the contents of a directory in the GUI
def list_directory_contents(directory):
    # Clear the current list of files
    for child in frame.winfo_children():
        child.destroy()

    # List the contents of the specified directory
    files = list_directory(directory)

    # Display the files in the GUI
    for file in files:
        create_icon(file, os.path.join(directory, file))

# Define a function to open a directory when its icon is clicked
def open_directory(directory):
    if os.path.isdir(directory):
        list_directory_contents(directory)

# Define a function to load an icon for a file or directory
def load_icon(file_path):
    # Load the icon image for the file or directory
    if os.path.isdir(file_path):
        # Use a folder icon for directories
        icon_path = '/u/miatey/FinalProj/dir_icon.png'
    else:
        # Use a file icon for files
        icon_path = '/u/miatey/FinalProj/file_icon.png'
    icon_image = Image.open(icon_path)

    # Resize the image to a smaller size
    icon_size = (64, 64)
    icon_image = icon_image.resize(icon_size, Image.ANTIALIAS)

    # Convert the image to a Tkinter-compatible format
    icon_image_tk = ImageTk.PhotoImage(icon_image)

    return icon_image_tk

# Define a function to create an icon for a file or directory
def create_icon(file_name, file_path, parent_frame=frame):
    # Load the icon image
    icon_image = load_icon(file_path)

    # Create the label widget
    label = tk.Label(parent_frame, text=file_name, image=icon_image, compound='top', font=('Arial', 10))

    # Check if the file is a directory
    if os.path.isdir(file_path):
        # Define the button click function
        def open_directory():
            # Create a new window to show the files within the directory
            new_window = tk.Toplevel(root)
            new_window.title(file_name)

            # Create a new frame to hold the list of files
            new_frame = tk.Frame(new_window)
            new_frame.pack(side='top', fill='both', expand=True)

            # List the contents of the directory in the new frame
            files = list_directory(file_path)
            for file in files:
                create_icon(file, os.path.join(file_path, file), new_frame)

        # Create the button widget
        button = tk.Button(label, text='Open', command=open_directory)
        button.pack(side='bottom')

        # Add the button to the label widget
        label.pack(side='top', padx=5, pady=5)
        label.pack_propagate(False)
        button.pack(pady=5)
    else:
        # Add the label widget to the frame
        label.pack(side='top', padx=5, pady=5)
        label.pack_propagate(False)



# # Create the starting directory input widget
# starting_dir = tk.Entry(root, width=50)
# starting_dir.insert(0, DIR)
# starting_dir.pack()

# Display the contents of the starting directory
list_directory_contents(DIR)

# Start the main event loop
root.mainloop()
