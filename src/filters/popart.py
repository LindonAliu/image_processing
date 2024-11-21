import numpy as np

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