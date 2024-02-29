import os
import argparse
import piexif
from PIL import Image


def process_single_image(raw_image_path, mask_image_path):
    """Copies geolocation (EXIF) data from a raw image to a corresponding mask image.

    Args:
        raw_image_path (str): Path to the raw image file.
        mask_image_path (str): Path to the mask image file.
    """

    if os.path.exists(mask_image_path):
        try:
            with Image.open(raw_image_path) as raw_image:
                exif_data = piexif.load(raw_image.info.get("exif", {}))

            # Handle cases where no EXIF data exists
            if exif_data:
                with Image.open(mask_image_path) as mask_image:
                    mask_image.save(mask_image_path, "JPEG", exif=piexif.dump(exif_data))
                print(f"Geolocation copied to: {mask_image_path}")

        except (piexif.InvalidImageDataError, OSError) as e:
            print(f"Error processing images: {e}")

def main(raw_images_dir=None, mask_images_dir=None):
    # ... (argument parsing - same as before) ...

    for raw_image_name in os.listdir(raw_images_dir):
        raw_image_path = os.path.join(raw_images_dir, raw_image_name)
        # ... (construct mask_image_path - same as before) ...

        process_single_image(raw_image_path, mask_image_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("raw_images_dir", help="Path to raw images directory")
    parser.add_argument("mask_images_dir", help="Path to mask images directory")
    args = parser.parse_args()
    main(args.raw_images_dir, args.mask_images_dir)
