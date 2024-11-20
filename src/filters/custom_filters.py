##
## Chung Ang University Project, 2024
## image_processing
## File description:
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



def radial_color_gradient(image):
    # Apply a radial color gradient effect to the image
  
    # Dimensions of the image
    height, width, _ = image.shape
    center_x, center_y = width // 2, height // 2

    # Determine the radius of the fisheye circle
    radius = min(center_x, center_y)

    # Create a grid for calculating distances from the center
    y, x = np.ogrid[:height, :width]
    distance_from_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

    # Create a mask for the fisheye circular region
    fisheye_mask = distance_from_center <= radius

    # Normalize the distance values (0 at the center, 1 at the edge of the circle)
    normalized_distance = np.zeros_like(distance_from_center, dtype=np.float32)
    normalized_distance[fisheye_mask] = distance_from_center[fisheye_mask] / radius

    # Define a more sophisticated color palette for the gradient
    warm_color = np.array([255, 100, 50])  # Soft orange
    cold_color = np.array([0, 200, 150])    # Aqua-green
    mid_color = np.array([0, 50, 200])    # Deep blue

    # Apply multi-step gradient transitions
    gradient = np.zeros_like(image, dtype=np.float32)
    for c in range(3):  # Loop over color channels (R, G, B)
        gradient[..., c] = np.where(
            normalized_distance < 0.5,
            cold_color[c] * (1 - normalized_distance * 2) + mid_color[c] * (normalized_distance * 2),
            mid_color[c] * (2 - normalized_distance * 2) + warm_color[c] * ((normalized_distance - 0.5) * 2)
        )

    # Convert the original image to grayscale to preserve brightness
    grayscale = np.dot(image[..., :3], [0.299, 0.587, 0.114])

    # Recolor the fisheye region while keeping the grayscale intensity
    recolored_image = np.zeros_like(image, dtype=np.float32)
    for c in range(3):  # Loop over color channels (R, G, B)
        recolored_image[..., c] = gradient[..., c] / 255.0 * grayscale

    # Ensure the gradient is applied only inside the fisheye region
    result = image.copy()
    recolored_fisheye = recolored_image.astype(np.uint8)
    result[fisheye_mask] = recolored_fisheye[fisheye_mask]

    # Smooth the transition near the edge for a cleaner look
    edge_fade = np.clip(1 - (distance_from_center - radius * 0.9) / (radius * 0.1), 0, 1)
    result = (result * edge_fade[:, :, np.newaxis] + image * (1 - edge_fade[:, :, np.newaxis])).astype(np.uint8)

    return result

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





def apply_pop_art_filter(image):
    # Further refined pop art effect with more levels, vibrant colors, and bold outlines.
    
    # Step 1: Convert the image to grayscale
    grayscale = np.dot(image[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)

    # Step 2: Apply Gaussian blur for smoothing
    def gaussian_blur(img, kernel_size=5, sigma=1.5):
        # Applies Gaussian blur to smooth the image.
        k = kernel_size // 2
        x, y = np.mgrid[-k:k+1, -k:k+1]
        gaussian_kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        gaussian_kernel /= gaussian_kernel.sum()

        padded_img = np.pad(img, k, mode='reflect')
        blurred_img = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                region = padded_img[i:i+kernel_size, j:j+kernel_size]
                blurred_img[i, j] = np.sum(region * gaussian_kernel)
        return blurred_img

    blurred_grayscale = gaussian_blur(grayscale)

    # Step 3: Enhanced edge detection
    def gradient_edge_detection(img):
        """Detects edges using gradients."""
        gradient_x = np.abs(np.gradient(img, axis=0))
        gradient_y = np.abs(np.gradient(img, axis=1))
        edges = gradient_x + gradient_y
        return np.clip(edges, 0, 255).astype(np.uint8)

    edges = gradient_edge_detection(blurred_grayscale)
    edges = (edges > 60).astype(np.uint8) * 255  # Refined threshold for more detail

    # Step 4: Quantize the grayscale image into 7 levels
    def quantize_image(img, levels):
        # Quantizes the image into a specified number of levels.
        step = 255 // levels
        return (img // step) * step

    quantized = quantize_image(blurred_grayscale, levels=7)  # 7 levels for finer segmentation

    # Step 5: Assign vibrant colors to regions
    color_map = {
        0: [0, 0, 128],     # Dark Blue
        36: [75, 0, 130],   # Indigo
        72: [0, 0, 255],    # Bright Blue
        108: [139, 0, 255], # Violet
        144: [255, 0, 255], # Magenta
        180: [0, 255, 255], # Cyan
        216: [255, 255, 0], # Yellow
        255: [255, 69, 0],  # Red-Orange
    }
    pop_art_image = np.zeros_like(image)
    for level, color in color_map.items():
        mask = quantized == level
        pop_art_image[mask] = color

    # Step 6: Overlay bold black outlines
    edge_positions = np.where(edges > 0)
    pop_art_image[edge_positions[0], edge_positions[1]] = [0, 0, 0]  # Add black outlines

    # Step 7: Preserve original black pixels
    black_pixel_mask = (np.sum(image, axis=-1) == 0)
    pop_art_image[black_pixel_mask] = [0, 0, 0]

    return pop_art_image



def apply_painting_filter(image):
    # Apply a painting effect to the image

    # Step 1: Convert to grayscale
    grayscale = np.dot(image[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)

    # Step 2: Apply Gaussian blur to reduce noise
    def gaussian_blur(img, kernel_size=7, sigma=1.2):
        k = kernel_size // 2
        x, y = np.mgrid[-k:k+1, -k:k+1]
        gaussian_kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        gaussian_kernel /= gaussian_kernel.sum()

        if len(img.shape) == 2:  # Grayscale
            padded_img = np.pad(img, k, mode='reflect')
            blurred_img = np.zeros_like(img)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    region = padded_img[i:i+kernel_size, j:j+kernel_size]
                    blurred_img[i, j] = np.sum(region * gaussian_kernel)
            return blurred_img
        elif len(img.shape) == 3:  # RGB
            blurred_img = np.zeros_like(img)
            for c in range(3):  # Process each channel independently
                padded_img = np.pad(img[..., c], k, mode='reflect')
                for i in range(img.shape[0]):
                    for j in range(img.shape[1]):
                        region = padded_img[i:i+kernel_size, j:j+kernel_size]
                        blurred_img[i, j, c] = np.sum(region * gaussian_kernel)
            return blurred_img

    blurred = gaussian_blur(grayscale)

    # Step 3: Edge detection using Laplacian
    def laplacian_edge_detection(img):
        kernel = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])
        k = kernel.shape[0] // 2
        padded_img = np.pad(img, k, mode='reflect')
        edges = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                region = padded_img[i:i+kernel.shape[0], j:j+kernel.shape[1]]
                edges[i, j] = np.sum(region * kernel)
        return np.abs(edges)

    edges = laplacian_edge_detection(blurred)
    edge_mask = (edges > 20).astype(np.uint8) * 255  # Lower threshold for cleaner edges

    # Step 4: Quantize colors into a smoother palette
    def quantize_image(img, levels=15):  # Increased levels for smoother transitions
        step = 255 // levels
        return (img // step) * step

    quantized_image = quantize_image(image, levels=12)

    # Step 5: Blend quantized image with edge mask
    edge_mask_inverted = 255 - edge_mask
    edge_mask_3d = np.repeat(edge_mask_inverted[:, :, np.newaxis], 3, axis=2)

    painting_image = np.clip((quantized_image * 0.95 + edge_mask_3d * 0.07), 0, 255).astype(np.uint8)

    # Step 6: Final smoothing pass for blending
    painting_image = gaussian_blur(painting_image, kernel_size=5, sigma=0.5)  # Softer final smoothing pass

    return painting_image





