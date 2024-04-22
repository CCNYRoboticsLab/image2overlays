# This script reads the crackMask images and the concreteMask folder to create filteredCrack folder which has those result images.
import cv2
import os
import configparser
import numpy as np

# Load the INI file and parse it
config = configparser.ConfigParser()
config.read("config.ini")  # Replace with the actual path to your INI file

# Paths for the concreteMask images, raw images, and output images
# Read from the INI file
# mask_dir = config["Segmentation"]["mask_directory"]
# raw_dir = config["Settings"]["raw_directory"]
# output_dir = config["Overlay"]["overlay_transparent_directory"]
concreteMask_dir = config["CrackSegmentation"]["mask_directory"].replace("crackmask", "concretemask")
crackMask_dir = config["CrackSegmentation"]["mask_directory"]
output_dir = config["CrackSegmentation"]["mask_directory"].replace("crackmask", "filteredCrack")

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the files in the mask directory
for concreteMask_name in os.listdir(concreteMask_dir):
    # Extract the image name from the filename
    crackMask_name = concreteMask_name.split(".")[0] + ".png"

    # Load the mask and raw images
    mask_image = cv2.imread(
        os.path.join(concreteMask_dir, concreteMask_name), cv2.IMREAD_GRAYSCALE
    )
    original_image = cv2.imread(os.path.join(crackMask_dir, crackMask_name))

    if mask_image is None or original_image is None:
        print(f"Error reading {concreteMask_name} or {crackMask_name}. Skipping...")
        continue

    # Ensure the original image and mask have the same dimensions
    if original_image.shape[:2] != mask_image.shape[:2]:
        mask_image = cv2.resize(
            mask_image, (original_image.shape[1], original_image.shape[0])
        )

    # Apply the mask to the original image
    masked_original = cv2.bitwise_and(original_image, original_image, mask=mask_image)

    # Save the overlaid image to the output directory
    output_name = os.path.join(output_dir, crackMask_name)
    cv2.imwrite(output_name, masked_original)
    print(f"Saved {output_name}")

print("Processing complete!")
