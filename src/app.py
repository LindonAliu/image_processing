##
## Chung Ang University Project, 2024
## image_processing
## File description:
## app: the application state of the image processing application
##

from __future__ import annotations

from tkinter import Tk, Label

from gui import create_window, create_filter_frame, create_image_frame
from gui import change_image, display_error_message

import os
import cv2
import numpy as np
from tkinter import filedialog

def is_image_file(filepath) -> bool:
    return filepath.endswith('.jpg') or filepath.endswith('.png')

class AppState:
    def __init__(self):
        self.window: Tk = None
        self.image_label: Label = None
        self.original_pixel_array: np.ndarray = None
        self.pixel_array: np.ndarray = None

    def create_gui(self) -> AppState:
        self.window = create_window("Image Processing", 800, 600)

        filters = {
            "Original": lambda _: self.original_pixel_array.copy(),
            "Grayscale": lambda pixel_array: cv2.cvtColor(pixel_array, cv2.COLOR_RGB2GRAY),
            "Invert": lambda pixel_array: 255 - pixel_array,
            "Blur": lambda pixel_array: cv2.GaussianBlur(pixel_array, (21, 21), 0)
        }

        create_filter_frame(self.window, filters, self.apply_filter, self.import_image, self.save_image)
        _, self.image_label = create_image_frame(self.window)

        return self

    def run(self) -> None:
        self.window.mainloop()

    def import_image(self, filepath: str) -> None:
        if not is_image_file(filepath):
            display_error_message("Error: Please select a .jpg or .png file.")
            return

        if not os.path.exists(filepath):
            display_error_message("Error: The file does not exist.")
            return

        pixel_array = cv2.imread(filepath)
        if pixel_array is None:
            display_error_message("Error: The image could not be loaded.")
            return
        pixel_array = cv2.cvtColor(pixel_array, cv2.COLOR_BGR2RGB)

        self.pixel_array = pixel_array
        self.original_pixel_array = pixel_array.copy()

        if self.image_label:
            change_image(self.image_label, self.pixel_array)

    def apply_filter(self, filter_function):
        if self.original_pixel_array is not None:
            filtered_image = filter_function(self.original_pixel_array)
            if len(filtered_image.shape) == 2:
                filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2RGB)
            self.pixel_array = filtered_image
            change_image(self.image_label, self.pixel_array)
        else:
            display_error_message("Error: the filter could not be applied.")

    def save_image(self):
        if self.pixel_array is not None:
            filename = filedialog.asksaveasfilename()
            if filename:
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    display_error_message("Error: Please save the file with a .png, .jpg, or .jpeg extension.")
                else:
                    cv2.imwrite(filename, self.pixel_array)
        else:
            display_error_message("Error: no image to save.")
