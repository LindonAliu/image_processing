##
## Chung Ang University Project, 2024
## image_processing
## File description:
## main
##
from geometry import img_to_fisheye
import cv2

from app import AppState

def main():
    app: AppState = AppState()
    app.create_gui().run()

    file = "team13_photo.jpg"
    dest = img_to_fisheye(file, 0.00005)

    cv2.imshow("Original",cv2.imread(file))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow("Barrel Distortion Effect", dest)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
