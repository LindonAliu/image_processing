##
## Chung Ang University Project, 2024
## image_processing
## File description:
## to_tree: christmas part, to render final image
##
import random
import cv2
import numpy as np
import os


def to_tree(sphere):
    img = cv2.imread("./assets/sapin.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    sphere_nb = 0
    spheres = ["./assets/christmas_ball/fisheye" + str(i) + ".png" for i in range(1, 7)]

    #radius = sphere.shape[0]
    width_tree, height_tree = img.shape[:2]
    marker = [0, 0, 0]
    width_cball = 0

    for i in range(width_tree):
        for j in range(height_tree):
            if np.all(img[i, j] == marker):
                width_cball += 1
            else:
                if width_cball != 0:
                    width_cball +=1 #so that we don't loose if impair
                    width_cball = width_cball//2
                    radius = sphere.shape[0]

                    sphere2 = resize(sphere, 2*width_cball/radius)
                
                    i = i - width_cball
                    j = j - 2*width_cball

                    for k in range(2*width_cball):
                        for l in range(2*width_cball):
                            if np.sqrt((k-width_cball)**2+(l-width_cball)**2)<=width_cball:
                                if np.all(sphere2[k, l, :] == [0, 0, 0]): #to delete black pixels (as it will otherwise be counted as a marker)
                                    sphere2[k, l, :] = [1, 1, 1]
                                img[i+k, j+l, :] = sphere2[k, l, :]
                    width_cball = 0

                    sphere = cv2.imread(spheres[sphere_nb])
                    sphere = cv2.cvtColor(sphere, cv2.COLOR_BGR2RGB)
                    sphere_nb = np.min([sphere_nb+1, len(spheres)-1]) 


                    break
    return img

def resize(img, scale_factor):
    original_width, original_height = img.shape[:2]
    
    # reduced dim
    new_width = round(original_width * scale_factor) 
    new_height = round(original_height * scale_factor) 
    
    resized_img = np.zeros((new_width, new_height, 3), dtype=np.uint8)
    
    # get pixels values
    for i in range(new_width):
        for j in range(new_height):
            orig_x = int(i / scale_factor)
            orig_y = int(j / scale_factor)
        
            resized_img[i, j] = img[orig_x, orig_y]
    
    return resized_img

