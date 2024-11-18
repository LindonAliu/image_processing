import cv2
import numpy as np
import random

def img_to_fisheye(file, k):
    # file : input file
    # k : distortion parameter

    img = cv2.imread(file)
    height, width = img.shape[:2]

    if height != width: 
        dim = np.min([height, width])
        center_x, center_y = round(height/2), round(width/2)
        half = round(dim/2)
        img = img[ center_x-half:center_x+half, center_y-half:center_y+half ] 
        width, height = dim, dim

    center_x, center_y = width/2, height/2
    dest = np.zeros_like(img)

    # calculates the barrel deformation
    new_coordinates_x, new_coordinates_y = [], []

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
                new_coordinates_x.append(x)
                new_coordinates_y.append(y)

    start_point = (np.min(np.array(new_coordinates_x)), np.max(np.array(new_coordinates_y)))  # Coordonnées (x, y)
    end_point = (np.max(np.array(new_coordinates_x)), np.max(np.array(new_coordinates_y)))  # Coordonnées (x, y)
    cv2.line(dest, start_point, end_point, (255, 0, 0), 3)

    x_min = np.min(np.array(new_coordinates_x))
    x_max = np.max(np.array(new_coordinates_x))
    y_min = np.min(np.array(new_coordinates_y))
    y_max = np.max(np.array(new_coordinates_y))

    dest_resized = dest[x_min:x_max, y_min:y_max]

    round_mask = get_round_mask(dest_resized)
    dest = add_mask(dest_resized, round_mask)
    dest = add_blur(dest, round_mask)

    return dest


def get_round_mask(src):
    # get a round mask to add fisheye round border to image 
    height, width = src.shape[:2]
    dest = np.ones((width, height))*255

    center = round(width/2)
    r_max = round( np.sqrt( (height-center)**2 )  ) - 2
    r_middle = r_max - round(1/32*r_max)
    r_little = r_max - round(2/32*r_max)
    
    for x in range(width):
        for y in range(height):
            r = np.sqrt( (x-center)**2 + (y-center)**2 )
            if r >= r_max :
                dest[x, y] = 0
            elif r >= r_middle:
                dest[x, y] = 1
            elif r >= r_little :
                dest[x, y] = 2


    return dest

def add_mask(src, mask):
    dest = np.ones_like(src)
    width, height = src.shape[:2]

    for x in range(width):
        for y in range(height):
            if mask[x,y] == 0:
                dest[x,y] = np.array([0,0,0])
            elif mask[x,y] == 1:
                dest[x,y] = get_darker(src[x,y], 80)
            elif mask[x,y] == 2:
                dest[x,y] = get_darker(src[x,y], 50)
            else:
                dest[x, y] = get_darker(src[x,y], 20)

    return dest

def get_darker(src, index):
    dest = np.zeros(3)

    for i in range(3):
        if src[i] - index < 0:
            dest[i] = 0
        else: 
            dest[i] = src[i] - index

    return dest

def add_blur(src, mask): 
    width, height = src.shape[:2]
    padding = 3 // 2
    blurred_image = src.copy()

    # Parcours de tous les pixels de l'image
    for x in range(padding, height - padding):
        for y in range(padding, width - padding):
            if mask[x, y] != 255:  
                kernel_region = src[x-padding:x+padding+1, y-padding:y+padding+1]
                blurred_image[x, y] = np.mean(kernel_region, axis=(0, 1))
            
    return blurred_image