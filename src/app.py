##
## Chung Ang University Project, 2024
## image_processing
## File description:
## app: the application state of the image processing application
##

from __future__ import annotations

from tkinter import Tk, Label

from gui import create_window, create_button, create_image_label, create_listbox
from gui import import_image_action, change_image, display_error_message

import os
import cv2
import numpy as np

def is_image_file(filepath) -> bool:
    return filepath.endswith('.jpg') or filepath.endswith('.png')

class AppState:
    def __init__(self):
        self.window: Tk = None

        self.image_filepath: str = ""
        self.image_label: Label = None

        self.original_pixel_array: np.ndarray = None
        self.pixel_array: np.ndarray = None

    def create_gui(self) -> AppState:
        self.window = create_window("Image Processing", 800, 600)
        self.image_label = create_image_label(self.window)
        create_button(self.window, "Import Image", (0, 0),
                      lambda: import_image_action(self.set_image_filepath))
        
        filters = {
            "Grayscale": lambda pixel_array: cv2.cvtColor(pixel_array, cv2.COLOR_RGB2GRAY),
            "Invert": lambda pixel_array: 255 - pixel_array,
            "Blur": lambda pixel_array: cv2.GaussianBlur(pixel_array, (21, 21), 0)
        }

        create_listbox(self.window, filters, (0, 30), self.apply_filter)
        return self

    def run(self) -> None:
        self.window.mainloop()

    def set_image_filepath(self, filepath: str) -> None:
        if not is_image_file(filepath):
            display_error_message("Please select a .jpg or .png file.")
            return
        
        if not os.path.exists(filepath):
            display_error_message("The file does not exist.")
            return

        pixel_array = cv2.imread(filepath)
        if pixel_array is None:
            display_error_message("The image could not be loaded.")
            return
        pixel_array = cv2.cvtColor(pixel_array, cv2.COLOR_BGR2RGB)

        self.pixel_array = pixel_array
        self.original_pixel_array = pixel_array.copy()
        self.image_filepath = filepath
        print("filepath in application statement was updated by " + filepath)

        if self.image_label:
            change_image(self.image_label, self.pixel_array)

    def apply_filter(self, filter_function):
        if self.original_pixel_array is not None:
            filtered_image = filter_function(self.original_pixel_array)
            # Gérer les images en niveaux de gris
            if len(filtered_image.shape) == 2:
                filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2RGB)
            self.pixel_array = filtered_image
            change_image(self.image_label, self.pixel_array)
        else:
            display_error_message("Aucune image n'est chargée.")
