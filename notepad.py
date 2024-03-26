import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import os.path

root = tk.Tk()
root.title("Notepad")


def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

    if file_path:  # If a file was selected
        try:
            with open(file_path, 'r') as f:
                text_area.delete(1.0, "end")  # Clear existing text
                text_area.insert(1.0, f.read())
        except FileNotFoundError:
            # Show error message if file not found
            messagebox.showerror("Error", "File not found")
        except Exception as e:
            # Show error message for other potential errors
            messagebox.showerror("Error", "An error occurred while opening the file:", e)

def save_file():
    current_file = getattr(save_file, "current_file", None)  # Track current file

    if current_file is None:
        # If no existing file, do "Save As"
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            save_file.current_file = file_path  # Store for future saves
    else:
        file_path = current_file

    if file_path:
        try:
            with open(file_path, 'w') as f:
                f.write(text_area.get(1.0, "end"))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while saving the file:", e)

def save_as_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as f:
                f.write(text_area.get(1.0, "end"))
            save_file.current_file = file_path  # Update current file
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while saving the file:", e)

def about_notepad():
    messagebox.showinfo("About", "A simple notepad created using Python(Tkinter)")

# --- Function to save geometry ---
def save_geometry():
    width = root.winfo_width()
    height = root.winfo_height()
    x = root.winfo_x()  
    y = root.winfo_y()  

    config = configparser.ConfigParser()
    config['geometry'] = {'width': width, 'height': height, 'x': x, 'y': y}
    with open('window_config.ini', 'w') as configfile:
        config.write(configfile)
        
    root.destroy()

# --- Function to load geometry ---
def load_geometry():
    if os.path.exists('window_config.ini'):
        config = configparser.ConfigParser()
        config.read('window_config.ini')
        geometry_string = config['geometry'].get('width') + 'x' + config['geometry'].get('height')
        geometry_string += '+' + config['geometry'].get('x') + '+' + config['geometry'].get('y')
        root.geometry(geometry_string)

# --- Load geometry on startup ---
load_geometry()

# --- Bind the save_geometry function to the close event ---
root.protocol("WM_DELETE_WINDOW", save_geometry)


my_menu = tk.Menu(root)
my_submenu1 = tk.Menu(my_menu, tearoff=0)

my_submenu1.add_command(label="Open", command=open_file)
my_submenu1.add_command(label="Save", command=save_file)
my_submenu1.add_command(label="Save as")
my_submenu1.add_separator()
my_submenu1.add_command(label="Exit", command=exit)

my_submenu2 = tk.Menu(my_menu, tearoff=0)

my_submenu2.add_command(label="About Notepad", command=about_notepad)
root.config(menu=my_menu)

my_menu.add_cascade(label="File", menu=my_submenu1)
my_menu.add_cascade(label="Help", menu=my_submenu2)


scrollbar = tk.Scrollbar(root)
scrollbar.pack(fill="y", side="right")
text_area = tk.Text(root, yscrollcommand=scrollbar.set, exportselection=False, font=("Consolas", 11))
text_area.pack(fill="both", expand="true")
scrollbar.config(command=text_area.yview)



root.mainloop()
