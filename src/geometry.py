import cv2
import numpy as np

def img_to_fisheye(file, k):
    # file : input file
    # k : distortion parameter

    img = cv2.imread(file)
    height, width = img.shape[:2]

    dest = np.zeros_like(img)

    # calculates the barrel deformation
    center_x, center_y = width/2, height/2

    for y in range(width):
        for x in range(height):

            dx = x - center_x
            dy = y - center_y

            r = np.sqrt(dx**2+dy**2) #source radius
            rd = r*(1 + k*r**2) #distorted radius


            if r != 0:
                scale = rd/r
            else :
                scale = 1

            new_x = int(center_x + (dx * scale))
            new_y = int(center_y + (dy * scale))
            
            if 0 <= new_y < width and 0 <= new_x < height:
                dest[x, y] = img[new_x, new_y]

    return dest


