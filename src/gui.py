##
## Chung Ang University Project, 2024
## image_processing
## File description:
## gui: utils function for creating GUI elements
##

from tkinter import filedialog, messagebox, Canvas, Scrollbar
from tkinter import Button, Label, Tk, Listbox, Frame
from tkinter import LEFT, RIGHT, BOTH, Y, HORIZONTAL, VERTICAL, BOTTOM, X

from PIL import Image, ImageTk
import numpy as np
from typing import Tuple

def import_image_action(import_image_callback: callable) -> None:
    filename = filedialog.askopenfilename()
    if filename:
        import_image_callback(filename)

def on_filter_select(event, listbox, filters, apply_filter_callback):
    selection = listbox.curselection()
    if selection:
        filter_name = listbox.get(selection[0])
        filter_function = filters[filter_name]
        apply_filter_callback(filter_function)

def create_filter_frame(window: Tk, filters: dict, apply_filter_callback: callable, import_image_callback: callable,
                        save_image_in_file_action: callable, update_original_image_callback: callable) -> Frame:
    """Create a frame that contains the filter list and buttons."""
    frame = Frame(window, padx=10, pady=10)
    frame.pack(side=LEFT, fill=Y)

    import_button = Button(frame, text="Import image", command=lambda: import_image_action(import_image_callback))
    import_button.pack(pady=5)

    listbox_label = Label(frame, text="Filters :")
    listbox_label.pack(pady=5)

    listbox = Listbox(frame, height=15)
    for filter_name in filters.keys():
        listbox.insert('end', filter_name)
    listbox.pack(pady=5)
    listbox.bind("<<ListboxSelect>>", lambda event: on_filter_select(event, listbox, filters, apply_filter_callback))

    save_in_file_button = Button(frame, text="Save image as", command=lambda: save_image_in_file_action())
    save_in_file_button.pack(pady=5)

    save_button = Button(frame, text="Save image", command=lambda: update_original_image_callback())
    save_button.pack(pady=5)

    return frame

def create_image_frame(window: Tk) -> Tuple[Canvas, Label]:
    """Create a frame to display the image."""
    frame = Frame(window)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)

    canvas = Canvas(frame, bg='white')
    canvas.pack(side=LEFT, expand=True, fill=BOTH)

    hbar = Scrollbar(frame, orient=HORIZONTAL, command=canvas.xview)
    hbar.pack(side=BOTTOM, fill=X)
    vbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    vbar.pack(side=RIGHT, fill=Y)

    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.config(scrollregion=canvas.bbox("all"))

    return canvas, canvas

def change_image(canvas: Canvas, image_source) -> None:
    """Change the image displayed in the window."""
    if isinstance(image_source, str):
        # image_source is a file path
        try:
            image = Image.open(image_source)
        except IOError:
            display_error_message("Error: The image could not be loaded.")
            return
    elif isinstance(image_source, np.ndarray):
        # image_source is a pixel array
        try:
            image = Image.fromarray(image_source)
        except Exception as e:
            display_error_message(f"Error: {e}")
            return
    else:
        display_error_message("Error: Invalid image source.")
        return

    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=image_tk)
    canvas.image = image_tk
    canvas.config(scrollregion=canvas.bbox("all"))

def display_error_message(message: str) -> None:
    """Display an error message to the user."""
    messagebox.showerror("Error", message)

def create_window(title: str, width: int, height: int) -> Tk:
    """Create a window with the given title, width, and height."""
    window: Tk = Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")
    return window
