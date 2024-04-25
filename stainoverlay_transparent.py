import cv2
import os
import configparser

import numpy as np

# Load the INI file and parse it
config = configparser.ConfigParser()
config.read("config.ini")  # Replace with the actual path to your INI file

# Paths for the mask images, raw images, and output images
# Read from the INI file
mask_dir = config["StainSegmentation"]["mask_directory"].replace("stainmask", "filteredStainMasks")
raw_dir = config["Settings"]["image_path"]
output_dir = config["StainOverlay"]["overlay_directory"].replace("stainoverlay", "filteredStainOverlays")

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the files in the mask directory
for mask_name in os.listdir(mask_dir):
    # Extract the image name from the filename
    raw_name = mask_name.split(".")[0] + ".jpg"

    # Load the mask and raw images
    mask = cv2.imread(os.path.join(mask_dir, mask_name), cv2.IMREAD_GRAYSCALE)
    raw = cv2.imread(os.path.join(raw_dir, raw_name))

    if mask is None or raw is None:
        print(f"Error reading {mask_name} or {raw_name}. Skipping...")
        continue

    print(raw.shape)
    print(mask.shape)

    # Create an empty weight map with the same dimensions as the raw image
    weight_map = np.zeros_like(raw)  

    # Set pixels where mask == 38 to the color [0, 0, 255] (blue)
    weight_map[mask == 38] = [0, 0, 255] 

    # Overlay the weight map onto the original image
    overlay = cv2.addWeighted(raw, 1, weight_map, 0.5, 0) 
    
    # Save the intermediate results
    # cv2.imwrite(os.path.join(output_dir, f"{raw_name}_mask.jpg"), mask)
    # # cv2.imwrite(os.path.join(output_dir, f"{raw_name}_binary_mask.jpg"), binary_mask)
    # cv2.imwrite(os.path.join(output_dir, f"{raw_name}_weight_map.jpg"), weight_map)


    # Save the overlaid image to the output directory
    output_name = os.path.join(output_dir, raw_name)
    cv2.imwrite(output_name, overlay)
    print(f"Saved {output_name}")

print("Processing complete!")
