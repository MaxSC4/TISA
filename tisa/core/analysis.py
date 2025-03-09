import numpy as np
from PIL import Image


def calculate_label_percentages(segmented_image_path):
    """
    Calculate and return the percentage of each label in a segmented image.

    :param segmented_image_path: Path to the segmented image file (HxWx3, RGB).
    :return: Dictionary with labels as keys and a tuple (percentage, hex_color) as values.
    """
    # Open the segmented image and convert to NumPy array
    segmented_image = np.array(Image.open(segmented_image_path))

    # Flatten the segmented image to handle all unique colors directly (HxWx3 -> N, 3)
    flat_pixels = segmented_image.reshape(-1, segmented_image.shape[-1])

    # Identify unique colors and their counts
    unique_colors, counts = np.unique(flat_pixels, axis=0, return_counts=True)
    total_pixels = np.sum(counts)

    # Calculate percentages for each unique color
    label_percentages = {tuple(color): (count / total_pixels) * 100 for color, count in zip(unique_colors, counts)}

    # Map each unique color to its hex representation
    label_to_color = {
        tuple(color): f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        for color in unique_colors
    }

    # Combine percentages and colors
    label_data = {
        label_to_color[tuple(color)]: (label_percentages[tuple(color)], label_to_color[tuple(color)])
        for color in unique_colors
    }

    return label_data