##
## Chung Ang University Project, 2024
## image_processing
## File description:
## app: the application state of the image processing application
##

from tkinter import Tk
from gui import create_window, create_button, import_image_action

class AppState:
    def __init__(self):
        self.image_filepath: str = ""
        self.window: Tk = create_window("Image Processing", 800, 600)

        create_button(self.window, "Import Image",
                      lambda: import_image_action(self.set_image_filepath))
        self.window.mainloop()

    def set_image_filepath(self, filepath: str) -> None:
        self.image_filepath = filepath
        print("filepath in application statement was updated by " + filepath)
