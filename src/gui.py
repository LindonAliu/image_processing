##
## Chung Ang University Project, 2024
## image_processing
## File description:
## gui: utils function for creating GUI elements
##

from tkinter import *
from tkinter import filedialog
from typing import Tuple

def import_image_action(update_filepath_callback: callable) -> None:
    filename = filedialog.askopenfilename()
    if filename:
        update_filepath_callback(filename)

def create_button(window: Tk, text: str, position: Tuple[int, int], command: callable) -> Button:
    """Create a button that allows the user to import an image."""
    button: Button = Button(window, text=text, command=command)
    button.place(x=position[0], y=position[1])
    return button

def create_window(title: str, width: int, height: int) -> Tk:
    """Create a window with the given title, width, and height."""
    window: Tk = Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")
    return window
