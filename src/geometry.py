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

    round_mask = get_round_mask(radius)

    cv2.imshow("Resized", dest_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return dest


def get_round_mask(radius: int):
    # get a round mask to add fisheye round border to image 