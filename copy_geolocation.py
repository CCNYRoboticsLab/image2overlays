import os
import argparse
import piexif
from PIL import Image


def main(raw_images_dir=None, mask_images_dir=None):
    # If directories are not provided directly, parse them from command-line arguments
    if raw_images_dir is None or mask_images_dir is None:
        parser = argparse.ArgumentParser(
            description="Copy geolocation data from raw images to mask images."
        )
        parser.add_argument(
            "raw_images_dir",
            type=str,
            help="Path to the directory containing the raw images.",
        )
        parser.add_argument(
            "mask_images_dir",
            type=str,
            help="Path to the directory containing the mask images.",
        )

        # Parse command-line arguments
        args = parser.parse_args()
        raw_images_dir = args.raw_images_dir
        mask_images_dir = args.mask_images_dir

    # Loop through raw images
    for raw_image_name in os.listdir(raw_images_dir):
        raw_image_path = os.path.join(raw_images_dir, raw_image_name)

        # Assuming mask images have a similar naming convention
        mask_image_name = raw_image_name.replace(
            "raw", "mask"
        )  # Example transformation
        mask_image_path = os.path.join(mask_images_dir, mask_image_name)

        if os.path.exists(mask_image_path):
            # Extract EXIF data from the raw image
            with Image.open(raw_image_path) as raw_image:
                exif_data = piexif.load(raw_image.info.get("exif", {}))

            # Load the mask image
            with Image.open(mask_image_path) as mask_image:
                mask_image.save(mask_image_path, "JPEG", exif=piexif.dump(exif_data))

    print("Geolocation information copied to mask images.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("raw_images_dir", help="Path to raw images directory")
    parser.add_argument("mask_images_dir", help="Path to mask images directory")
    args = parser.parse_args()
    main(args.raw_images_dir, args.mask_images_dir)
