##
## Chung Ang University Project, 2024
## image_processing
## File description:
## gui: utils function for creating GUI elements
##
from tkinter import filedialog, messagebox
from tkinter import Button, Label, Tk, Listbox, Frame, LEFT, RIGHT, BOTH, Y
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
                        save_image_action: callable) -> Frame:
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

    save_button = Button(frame, text="Save image", command=lambda: save_image_action())
    save_button.pack(pady=5)

    return frame

def create_image_frame(window: Tk) -> Tuple[Frame, Label]:
    """Create a frame to display the image."""
    frame = Frame(window)
    frame.pack(side=RIGHT, expand=True, fill=BOTH)

    label = Label(frame)
    label.pack(expand=True)

    return frame, label

def change_image(image_label: Label, image_source) -> None:
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

    image = image.resize((600, 400), Image.LANCZOS)
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
