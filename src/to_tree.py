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
    print(os.getcwd())
    img = get_random_image()
    img = cv2.imread("CAU/image-processing/image_processing/sapin.png")

    radius = sphere.shape[0]

    width_tree, height_tree = img.shape[:2]
    marker = [0, 0, 0]
    width_cball = 0

    for i in range(width_tree):
        for j in range(height_tree):
            if np.all(img[i, j] == marker):
                width_cball += 1
            else:
                if width_cball != 0:
                    width_cball = width_cball//2
                    sphere2 = resize(sphere, 2*width_cball/radius)
                
                    i = i - width_cball
                    j = j - 2*width_cball

                    for k in range(2*width_cball):
                        for l in range(2*width_cball):
                            if np.sqrt((k-width_cball)**2+(l-width_cball)**2)<=width_cball:
                                img[i+k, j+l, :] = sphere2[k, l, :]
                    width_cball = 0
                    break

    cv2.imshow("result", img)
    cv2.waitKey(0)



def get_random_image():
    img_path = "../sapin" + str(random.randint(1,2)) #Change when more images
    img_path = "CAU/image-processing/image_processing/sapin" + str(random.randint(2,2)) + ".png" #Change when more images

    return cv2.imread(img_path)

def resize(img, scale_factor):
    original_width, original_height = img.shape[:2]
    
    # reduced dim
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    
    resized_img = np.zeros((new_width, new_height, 3), dtype=np.uint8)
    
    # get pixels values
    for i in range(new_width):
        for j in range(new_height):
            orig_x = int(i / scale_factor)
            orig_y = int(j / scale_factor)
        
            resized_img[i, j] = img[orig_x, orig_y]
    
    return resized_img
    

#resize_image_manual(cv2.imread("CAU/image-processing/image_processing/sapin2.png"), 0.5)

#to_tree(cv2.imread("CAU/image-processing/image_processing/fisheye_without_bg.png"))
to_tree(cv2.imread("CAU/image-processing/image_processing/fisheye_team13.png"))





"""from PIL import Image
    import numpy as np

    # Charger l'image
    image_path = 'CAU/image-processing/image_processing/sapin2.png'  # Remplace par le chemin de l'image
    image = Image.open(image_path)
    pixels = np.array(image)

# Extraire les couleurs uniques présentes
    if len(pixels.shape) == 3:  # Vérifier que l'image est en couleur
        unique_colors = set(map(tuple, pixels.reshape(-1, 3)))
    else:
        raise ValueError("L'image ne contient pas de données couleur.")

# Comparer avec toutes les valeurs possibles
    all_colors = {(r, g, b) for r in range(256) for g in range(256) for b in range(256)}
    missing_colors = all_colors - unique_colors

    print(f"Nombre de couleurs présentes : {len(unique_colors)}")
    print(f"Nombre de couleurs absentes : {len(missing_colors)}")

# Exemple : Afficher quelques couleurs absentes
    print("Quelques couleurs absentes :", list(missing_colors)[:10])"""