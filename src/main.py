##
## Chung Ang University Project, 2024
## image_processing
## File description:
## main
##

from app import AppState

def is_image_file(file_path):
    return file_path.endswith('.jpg') or file_path.endswith('.png')

def main():
    app: AppState = AppState()

if __name__ == '__main__':
    main()
