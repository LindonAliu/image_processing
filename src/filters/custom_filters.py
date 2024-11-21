##
## Chung Ang University Project, 2024
## image_processing
## File description: custom filters
## filters
##

import numpy as np

def apply_sepia_filter(image):
   # Add a sepia tone to the image
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_image = np.dot(image[..., :3], sepia_filter.T)
    sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
    return sepia_image

def apply_black_and_white_filter(image):
    # Convert the image to black and white
    grayscale = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    bw_image = np.repeat(grayscale[:, :, np.newaxis], 3, axis=2).astype(np.uint8)
    return bw_image

def apply_vintage_filter(image):
    # Apply a vintage effect to the image
    sepia_image = apply_sepia_filter(image)
    noise = np.random.normal(0, 25, sepia_image.shape).astype(np.uint8)
    vintage_image = np.clip(sepia_image + noise * 0.1, 0, 255).astype(np.uint8)
    return vintage_image

def apply_grain_filter(image, intensity=0.3):
    # Add grain to the image
    noise = np.random.normal(0, 50, image.shape).astype(np.int16)
    grainy_image = image.astype(np.int16) * (1 - intensity) + noise * intensity
    grainy_image = np.clip(grainy_image, 0, 255).astype(np.uint8)
    return grainy_image

def posterize_filter(image, num_colors=4):
    # Apply a posterization effect to the image

    # Calculate the step size for quantization
    step = 256 // num_colors
    
    # Quantize the image by rounding to the nearest step
    posterized_image = (image // step) * step + step // 2  # Center the color values in each range
    posterized_image = np.clip(posterized_image, 0, 255)  # Ensure valid color range

    return posterized_image.astype(np.uint8)

def glass_distortion_effect(image, displacement_strength=0.5):
    # Apply a glass distortion effect to the image

    height, width, channels = image.shape

    # Generate random displacement maps for x and y directions
    displacement_x = np.random.uniform(-displacement_strength, displacement_strength, size=(height, width))
    displacement_y = np.random.uniform(-displacement_strength, displacement_strength, size=(height, width))

    # Create mesh grid of pixel coordinates
    x, y = np.meshgrid(np.arange(width), np.arange(height))

    # Apply the displacement to the grid
    displaced_x = np.clip(x + displacement_x, 0, width - 1).astype(int)
    displaced_y = np.clip(y + displacement_y, 0, height - 1).astype(int)

    # Create the distorted image by sampling from the displaced coordinates
    distorted_image = image[displaced_y, displaced_x]

    return distorted_image











