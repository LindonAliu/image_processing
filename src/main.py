##
## Chung Ang University Project, 2024
## image_processing
## File description:
## main
##

from app import AppState

def main():
    app: AppState = AppState()
    app.create_gui().run()

if __name__ == '__main__':
    main()
