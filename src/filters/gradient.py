import numpy as np

def apply_radial_color_gradient(image):
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
