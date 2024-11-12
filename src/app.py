##
## Chung Ang University Project, 2024
## image_processing
## File description:
## app: the application state of the image processing application
##

from __future__ import annotations
from tkinter import Tk
from gui import create_window, create_button, import_image_action

class AppState:
    def __init__(self):
        self.image_filepath: str = ""
        self.window: Tk = None
    
    def create_gui(self) -> AppState:
        self.window = create_window("Image Processing", 800, 600)
        create_button(self.window, "Import Image", (0, 0),
                      lambda: import_image_action(self.set_image_filepath))
        return self

    def run(self) -> None:
        self.window.mainloop()

    def get_image_filepath(self) -> str:
        return self.image_filepath

    def set_image_filepath(self, filepath: str) -> None:
        self.image_filepath = filepath
        print("filepath in application statement was updated by " + filepath)
