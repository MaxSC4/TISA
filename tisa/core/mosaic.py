import os
import numpy as np
from PIL import Image

def split_image(image_path, rows, cols, output_dir, progress_callback=None):
    """
    Splits a high-resolution image into smaller tiles (rows x cols).
    """
    with Image.open(image_path) as img:
        width, height = img.size
        tile_width = width // cols
        tile_height = height // rows

        os.makedirs(output_dir, exist_ok=True)
        for i in range(rows):
            for j in range(cols):
                left = j * tile_width
                upper = i * tile_height
                right = (j + 1) * tile_width
                lower = (i + 1) * tile_height

                tile = img.crop((left, upper, right, lower))
                tile_name = f"tile_{i+1}_{j+1}.png"
                tile.save(os.path.join(output_dir, tile_name))

                if progress_callback:
                    progress = ((i * cols + j + 1) / (rows * cols)) * 100
                    progress_callback(progress)

    print(f"Image successfully split. Tiles saved in: {output_dir}")

def reconstruct_mosaic(input_folder, output_path, tile_prefix="tile"):
    """
    Reconstructs a mosaic from a folder of tiles named like 'tile_row_col.png'.
    Saves to output_path.
    """
    tiles = {}
    for filename in os.listdir(input_folder):
        if filename.startswith(tile_prefix) and filename.endswith(".png"):
            base_name = filename.replace(".png", "")
            # e.g. tile_2_3
            parts = base_name.split("_")
            row = int(parts[1])
            col = int(parts[2])
            tile_path = os.path.join(input_folder, filename)
            tiles[(row, col)] = Image.open(tile_path)

    if not tiles:
        raise ValueError("No valid tiles found.")

    rows = max(k[0] for k in tiles.keys())
    cols = max(k[1] for k in tiles.keys())

    tile_width, tile_height = next(iter(tiles.values())).size
    mosaic_width = cols * tile_width
    mosaic_height = rows * tile_height

    mosaic_img = Image.new("RGB", (mosaic_width, mosaic_height))
    for (row, col), tile in tiles.items():
        x_offset = (col - 1) * tile_width
        y_offset = (row - 1) * tile_height
        mosaic_img.paste(tile, (x_offset, y_offset))

    mosaic_img.save(output_path)
    print(f"Mosaic saved to {output_path}")
