import os
import argparse
from PIL import Image
from copy_geo_exiftool import process_single_image

def main(raw_images_dir, mask_images_dir, converted_masks_dir):
    """
    Converts PNG masks to JPEG, copies geolocation data, and places them in a new directory.

    Args:
        raw_images_dir: Path to the directory containing raw images.
        mask_images_dir: Path to the directory containing PNG mask images.
        converted_masks_dir: Path to the directory where converted JPEG masks will be stored.
    """

    os.makedirs(converted_masks_dir, exist_ok=True)  # Create the output directory if it doesn't exist

    for raw_image_name in os.listdir(raw_images_dir):
        if not raw_image_name.lower().endswith(".jpg"):
            print(raw_image_name.lower())
            continue  # Skip non-JPEG files

        # Construct paths for mask and converted mask images
        raw_image_path = os.path.join(raw_images_dir, raw_image_name)
        mask_image_name = raw_image_name.replace(".JPG", ".png")
        mask_image_path = os.path.join(mask_images_dir, mask_image_name)
        converted_mask_path = os.path.join(converted_masks_dir, mask_image_name.replace(".png", ".jpg"))

        if os.path.exists(mask_image_path):
            try:
                mask_image = Image.open(mask_image_path)
                if mask_image.format == "PNG":
                    mask_image.convert("RGB").save(converted_mask_path)  # Convert to JPEG and save
                    process_single_image(raw_image_path, converted_mask_path)  # Copy geolocation
                else:
                    print(f"Mask {mask_image_name} is not PNG. Skipping.")
            except Exception as e:
                print(f"raw_image_path: {raw_image_path}")
                print(f"Error processing {mask_image_name}: {e}")
        else:
            print(f"Mask image {mask_image_name} not found. Skipping.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_images_dir", help="Path to raw images directory")
    parser.add_argument("mask_images_dir", help="Path to mask images directory")
    parser.add_argument("converted_masks_dir", help="Path to converted masks directory")
    args = parser.parse_args()

    main(args.raw_images_dir, args.mask_images_dir, args.converted_masks_dir)

# python copy_geolocation_nn_jpg.py '/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images' '/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/nn_solidfiltered_crack_overlay' '/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/nn_solidfiltered_crack_overlay_jpg'