import os
import numpy as np
import multiprocessing
from PIL import Image
from .models_tf import perform_custom_segmentation

FIXED_PALETTE = [(255, 0, 0), (255, 5, 0), (255, 10, 0), (255, 15, 0), (255, 20, 0), (255, 25, 0), (255, 30, 0), (255, 35, 0), (255, 40, 0), (255, 45, 0), (255, 50, 0), (255, 55, 0), (255, 60, 0), (255, 65, 0), (255, 70, 0), (255, 75, 0), (255, 80, 0), (255, 85, 0), (255, 90, 0), (255, 95, 0), (255, 100, 0), (255, 105, 0), (255, 110, 0), (255, 115, 0), (255, 120, 0), (255, 125, 0), (255, 130, 0), (255, 136, 0), (255, 141, 0), (255, 146, 0), (255, 151, 0), (255, 156, 0), (255, 161, 0), (255, 166, 0), (255, 171, 0), (255, 176, 0), (255, 181, 0), (255, 186, 0), (255, 191, 0), (255, 196, 0), (255, 201, 0), (255, 206, 0), (255, 211, 0), 
(255, 216, 0), (255, 221, 0), (255, 226, 0), (255, 231, 0), (255, 236, 0), (254, 240, 0), (252, 244, 0), (250, 247, 0), (249, 250, 0), (247, 254, 0), (243, 255, 0), (237, 255, 0), (232, 255, 0), (227, 255, 0), (222, 255, 0), (217, 255, 0), (212, 255, 0), (207, 255, 0), (202, 255, 0), (197, 255, 0), (192, 255, 0), (187, 255, 0), (182, 255, 0), (177, 255, 0), (172, 255, 0), (167, 255, 0), (162, 255, 0), (157, 255, 0), (152, 255, 0), (147, 255, 0), (142, 255, 0), (137, 255, 0), (132, 255, 0), (127, 255, 0), (122, 255, 0), (117, 255, 0), (112, 255, 0), (107, 255, 0), (101, 255, 0), (96, 255, 0), (91, 255, 0), (86, 255, 0), (81, 255, 0), (76, 255, 0), (71, 255, 0), (66, 255, 0), (61, 255, 0), (56, 255, 0), (51, 255, 0), (46, 255, 0), (41, 255, 0), (36, 255, 0), (31, 255, 0), (26, 255, 0), (21, 255, 0), (16, 255, 0), (11, 255, 0), (7, 255, 1), (5, 255, 4), (4, 255, 7), (2, 255, 11), (0, 255, 14), (0, 255, 18), (0, 255, 23), (0, 
255, 28), (0, 255, 34), (0, 255, 39), (0, 255, 44), (0, 255, 49), (0, 255, 54), (0, 255, 59), (0, 255, 64), (0, 255, 69), (0, 255, 74), (0, 255, 79), (0, 255, 84), (0, 255, 89), (0, 255, 94), (0, 255, 99), (0, 255, 104), (0, 255, 109), (0, 255, 114), (0, 255, 119), (0, 255, 124), (0, 255, 129), (0, 255, 134), (0, 255, 139), (0, 255, 144), (0, 255, 149), (0, 255, 154), (0, 255, 159), (0, 255, 164), (0, 255, 170), (0, 255, 175), (0, 255, 180), (0, 255, 185), (0, 255, 190), (0, 255, 195), (0, 255, 200), (0, 255, 205), (0, 255, 210), (0, 255, 215), (0, 255, 220), (0, 255, 225), (0, 255, 230), (0, 255, 235), (0, 255, 240), (0, 255, 245), (0, 255, 250), (0, 254, 255), (0, 249, 255), (0, 244, 255), (0, 239, 255), (0, 234, 255), (0, 229, 255), (0, 224, 255), (0, 219, 255), (0, 214, 255), (0, 209, 255), (0, 203, 255), (0, 198, 255), (0, 193, 255), (0, 188, 255), (0, 183, 255), (0, 178, 255), (0, 173, 255), (0, 168, 255), (0, 163, 255), (0, 158, 255), (0, 153, 255), (0, 148, 255), (0, 143, 255), (0, 138, 255), (0, 133, 255), (0, 128, 255), (0, 123, 255), (0, 118, 255), (0, 113, 255), (0, 108, 255), (0, 103, 255), (0, 98, 255), (0, 93, 255), (0, 88, 255), (0, 83, 255), (0, 78, 255), (0, 73, 255), (0, 67, 255), (0, 62, 255), (0, 57, 255), (0, 52, 255), (0, 47, 255), (0, 42, 255), (0, 37, 255), (0, 32, 255), (0, 27, 255), (0, 22, 255), (0, 17, 255), (1, 13, 255), (2, 10, 255), (4, 6, 255), (6, 3, 255), (7, 0, 255), (12, 0, 255), (17, 0, 255), (22, 0, 255), (27, 0, 255), (32, 0, 255), (37, 0, 255), (42, 0, 255), (47, 0, 255), (52, 0, 255), (57, 0, 
255), (62, 0, 255), (68, 0, 255), (73, 0, 255), (78, 0, 255), (83, 0, 255), (88, 0, 255), (93, 0, 255), (98, 0, 255), (103, 0, 255), (108, 0, 255), (113, 0, 255), (118, 0, 255), (123, 0, 255), (128, 0, 255), (133, 0, 255), (138, 0, 255), (143, 0, 255), (148, 0, 255), (153, 0, 255), (158, 0, 255), (163, 0, 255), (168, 0, 255), (173, 0, 255), (178, 0, 255), (183, 0, 255), (188, 0, 255), (193, 0, 255), (198, 0, 255), (204, 0, 255), (209, 0, 255), (214, 0, 255), (219, 0, 255), (224, 0, 255), (229, 0, 255), (234, 0, 255), (239, 0, 255), (244, 0, 255), (247, 0, 253), (249, 0, 250), (251, 0, 246), (252, 0, 243), (254, 0, 240), (255, 0, 235), (255, 0, 230), (255, 0, 225), (255, 0, 220), (255, 0, 215), (255, 0, 210), (255, 0, 205), (255, 0, 200), (255, 0, 195), (255, 0, 190), (255, 0, 185), (255, 0, 180), (255, 0, 175), (255, 0, 169), (255, 0, 164), (255, 0, 159), (255, 0, 154), (255, 0, 149), (255, 0, 144), (255, 0, 139), (255, 0, 134), (255, 0, 129), (255, 0, 124), (255, 0, 119), (255, 0, 114), (255, 0, 109), (255, 0, 104), (255, 0, 99), (255, 0, 94), (255, 0, 89), (255, 0, 84), (255, 0, 79), (255, 0, 74), (255, 0, 69), (255, 0, 64), (255, 0, 59), (255, 0, 54), (255, 0, 49), (255, 0, 44), (255, 0, 39), (255, 0, 33), (255, 0, 28), (255, 0, 23)]

def apply_fixed_palette(segmented_image_array, palette):
    """
    Apply a fixed palette of colors to a segmented image (label map).

    :param segmented_image_array: NumPy array (HxW or HxWx3) representing the segmented labels.
    :param palette: List of RGB colors to apply, indexed by label.
    :return: Colorized segmented image as a NumPy array (HxWx3).
    """
    # Si l'image est 3D (RGB), prendre un seul canal (premier canal suffisant pour les labels)
    if segmented_image_array.ndim == 3 and segmented_image_array.shape[-1] == 3:
        segmented_image_array = segmented_image_array[..., 0]  # Utiliser un seul canal

    # Vérifier que l'image est bien 2D après la conversion
    if segmented_image_array.ndim != 2:
        raise ValueError(f"Expected a 2D labeled image, but got shape: {segmented_image_array.shape}")

    # Créer une image colorisée avec 3 canaux (HxWx3)
    height, width = segmented_image_array.shape
    colorized_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Appliquer les couleurs de la palette selon les labels
    for label, color in enumerate(palette):
        mask = segmented_image_array == label  # Masque pour le label actuel
        colorized_image[mask] = color  # Appliquer la couleur correspondante

    return colorized_image

def auto_crop(image, threshold=20):
    image_array = np.array(image)

    gray = np.mean(image_array, axis=1)

    mask = gray > threshold

    coords = np.argwhere(mask)
    if coords.size == 0:
        return image
    
    x_min, y_min = coords.min(axis=0)
    x_max, y_max = coords.max(axis=0)

    cropped_image = image.crop((y_min, x_min, y_max, x_max))
    return cropped_image

def process_single_tile(tile_path, output_folder, params, palette):
    try:
        with Image.open(tile_path) as img:
            image_array = np.array(img)
            print(f"Image shape: {image_array.shape}")  # Vérifie la taille de l'image

            segmented_list = perform_custom_segmentation(image_array, params)

            if segmented_list is None:
                raise ValueError("perform_custom_segmentation returned None")
            
            if not isinstance(segmented_list, (list, np.ndarray)):
                raise TypeError(f"Unexpected return type: {type(segmented_list)}")
            
            if len(segmented_list) == 0:
                raise ValueError("Segmentation list is empty")
            
            segmented_array = np.array(segmented_list[-1])
            print(f"Segmented array shape: {segmented_array.shape}")  # Vérifie la sortie

            segmented_image = Image.fromarray(segmented_array.astype(np.uint8))
            segmented_image = auto_crop(segmented_image)

            segmented_array = np.array(segmented_image)

            if segmented_array.ndim == 3 and segmented_array.shape[-1] == 3:
                segmented_array = segmented_array[..., 0]
                print("Segmented array reduced to single channel")

            colorized_image = apply_fixed_palette(segmented_array, palette)
            output_path = os.path.join(output_folder, os.path.basename(tile_path))
            Image.fromarray(colorized_image).save(output_path)

            return f"Processed {os.path.basename(tile_path)}"
    except Exception as e:
        return f"Failed to process {os.path.basename(tile_path)}: {e}"

def process_folder(input_folder, output_folder, params, color_palette=FIXED_PALETTE, progress_callback=None):
    """
    Processes all images in a folder by segmenting + palette.
    """
    os.makedirs(output_folder, exist_ok=True)
    tile_files = [
        os.path.join(input_folder, f)
        for f in os.listdir(input_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))
    ]

    total = len(tile_files)
    for idx, tile in enumerate(tile_files):
        result = process_single_tile(tile, output_folder, params, color_palette)
        print(result)
        if progress_callback:
            progress = int(((idx + 1) / total) * 100)
            progress_callback(progress)
