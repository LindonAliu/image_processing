##
## Chung Ang University Project, 2024
## image_processing
## File description:
## gui: utils function for creating GUI elements
##

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Button, Label, Tk

from PIL import Image, ImageTk

import numpy as np

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

def create_image_label(window: Tk) -> Label:
    """Create a label to display the image in the window."""
    label: Label = Label(window)
    label.grid(row=1, column=0)
    return label

def change_image(image_label: Label, image_source) -> None:
    """Change the image displayed in the window."""
    if isinstance(image_source, str):
        # image_source is a file path
        try:
            image = Image.open(image_source)
        except IOError:
            display_error_message("The image could not be loaded.")
            return
    elif isinstance(image_source, np.ndarray):
        # image_source is a pixel array
        try:
            image = Image.fromarray(image_source)
        except Exception as e:
            display_error_message(f"An error occurred: {e}")
            return
    else:
        display_error_message("Invalid image source.")
        return

    image = ImageTk.PhotoImage(image)

    image_label.configure(image=image)
    image_label.image = image
    return

def display_error_message(message: str) -> None:
    """Display an error message to the user."""
    messagebox.showerror("Error", message)

def create_window(title: str, width: int, height: int) -> Tk:
    """Create a window with the given title, width, and height."""
    window: Tk = Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")
    return window