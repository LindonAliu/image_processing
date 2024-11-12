##
## Chung Ang University Project, 2024
## image_processing
## File description:
## gui: utils function for creating GUI elements
##

from tkinter import *
from tkinter import filedialog

def import_image_action(update_filepath_callback: callable) -> None:
    filename = filedialog.askopenfilename()
    update_filepath_callback(filename)

def create_button(window: Tk, text: str, command: callable) -> None:
    """Create a button that allows the user to import an image."""
    button: Button = Button(window, text=text, command=command)
    button.pack()

def create_window(title: str, width: int, height: int) -> Tk:
    """Create a window with the given title, width, and height."""
    window: Tk = Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")
    return window
