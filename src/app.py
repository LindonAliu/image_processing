##
## Chung Ang University Project, 2024
## image_processing
## File description:
## app: the application state of the image processing application
##

from __future__ import annotations

from tkinter import Tk, Label, Canvas

from gui import create_window, create_filter_frame, create_image_frame
from gui import change_image, display_error_message

import os
import cv2
import numpy as np
from tkinter import filedialog
from filters.gradient import apply_radial_color_gradient
from filters.painting import apply_painting_filter
from filters.popart import apply_pop_art_filter
from filters.custom_filters import apply_sepia_filter, apply_black_and_white_filter, apply_vintage_filter, apply_grain_filter, glass_distortion_effect, posterize_filter
from filters.fisheye import img_to_fisheye

def is_image_file(filepath) -> bool:
    return filepath.endswith('.jpg') or filepath.endswith('.png')

class AppState:
    def __init__(self):
        self.window: Tk = None
        self.canvas: Canvas = None
        self.original_pixel_array: np.ndarray = None
        self.pixel_array: np.ndarray = None
        self.scale: float = 1.0

    def create_gui(self) -> AppState:
        self.window = create_window("Image Processing", 800, 600)

        filters = {
            "Sepia": apply_sepia_filter,
            "Black and white": apply_black_and_white_filter,
            "Vintage": apply_vintage_filter,
            "Grain": apply_grain_filter,
            "Pop art": apply_pop_art_filter,
            "Painting": apply_painting_filter,
            "Warm to Cold Gradient": apply_radial_color_gradient,
            "Glass Distortion Effect": glass_distortion_effect,
            "Posterize": posterize_filter,
            "Fisheye": lambda pixel_array: img_to_fisheye(pixel_array, 0.00005),
        }

        create_filter_frame(self.window, filters, self.apply_filter, self.import_image, self.save_image)
        self.canvas, _ = create_image_frame(self.window)

        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        self.canvas.focus_set()
        return self

    def zoom(self, event):
        if self.pixel_array is None:
            return
        if event.num == 4:
            self.scale *= 1.1
        elif event.num == 5:
            self.scale /= 1.1

        self.update_image()

    def update_image(self):
        if self.pixel_array is not None:
            height, width = self.pixel_array.shape[:2]
            new_size = (int(width * self.scale), int(height * self.scale))
            resized_image = cv2.resize(self.pixel_array, new_size, interpolation=cv2.INTER_LINEAR)
            change_image(self.canvas, resized_image)
            print("Update image")

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

        self.update_image()

    def apply_filter(self, filter_function):
        if self.original_pixel_array is not None:
            filtered_image = filter_function(self.original_pixel_array)
            if len(filtered_image.shape) == 2:
                filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2RGB)
            self.pixel_array = filtered_image
            self.update_image()
        else:
            display_error_message("Error: the filter could not be applied.")

    def save_image(self):
        if self.pixel_array is not None:
            filename = filedialog.asksaveasfilename()
            if filename:
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    display_error_message("Error: Please save the file with a .png, .jpg, or .jpeg extension.")
                else:
                    cv2.imwrite(filename, cv2.cvtColor(self.pixel_array, cv2.COLOR_RGB2BGR))
        else:
            display_error_message("Error: no image to save.")
