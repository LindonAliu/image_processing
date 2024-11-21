import numpy as np

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
