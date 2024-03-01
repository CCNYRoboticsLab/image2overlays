import os
import argparse
import piexif
from PIL import Image
from copy_geo_exiftool import process_single_image

def main(raw_images_dir=None, mask_images_dir=None):
    # ... (argument parsing - same as before) ...

    for raw_image_name in os.listdir(raw_images_dir):
        raw_image_path = os.path.join(raw_images_dir, raw_image_name)
        # ... (construct mask_image_path - same as before) ...
        # Assuming mask images have a similar naming convention
        mask_image_name = raw_image_name.replace(
            "raw", "mask"
        )  # Example transformation
        mask_image_path = os.path.join(mask_images_dir, mask_image_name)
        if os.path.exists(mask_image_path):
            process_single_image(raw_image_path, mask_image_path)
        else:
            print("Mask image not found. Skipping to the next image.")
            # raise FileNotFoundError("Mask image not found at specified path.")



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("raw_images_dir", help="Path to raw images directory")
    parser.add_argument("mask_images_dir", help="Path to mask images directory")
    args = parser.parse_args()
    main(args.raw_images_dir, args.mask_images_dir)
