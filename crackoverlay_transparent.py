# This Python script is performing image processing tasks related to crack segmentation and
# overlaying.
import cv2
import os
import configparser

import numpy as np

# Load the INI file and parse it
config = configparser.ConfigParser()
config.read("config.ini")  # Replace with the actual path to your INI file

# Define paths for both types of masks and their corresponding output directories
mask_dirs = {
    "crackmask": config["CrackSegmentation"]["mask_directory"],
    "filteredCrackMasks": config["CrackSegmentation"]["mask_directory"].replace("crackmask", "filteredCrackMasks")
}
raw_dir = config["Settings"]["image_path"]
output_dirs = {
    "crackmask": config["CrackOverlay"]["overlay_directory"],
    "filteredCrackMasks": config["CrackOverlay"]["overlay_directory"].replace("crackoverlay", "filteredCrackOverlays")
}

# Process each type of mask
for mask_type, mask_dir in mask_dirs.items():
    if not os.path.exists(mask_dir):
        print(f"Skipping {mask_type} processing: {mask_dir} does not exist.")
        continue

    output_dir = output_dirs[mask_type]
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Processing {mask_type}...")
    
    # Iterate over the files in the mask directory
    for mask_name in os.listdir(mask_dir):
        # Extract the image name from the filename
        raw_name = mask_name.split(".")[0] + ".jpg"
        if not os.path.isfile(os.path.join(raw_dir, raw_name)):
            raw_name = mask_name.split(".")[0] + ".JPG"

        # Load the mask and raw images
        mask = cv2.imread(os.path.join(mask_dir, mask_name), cv2.IMREAD_GRAYSCALE)
        raw = cv2.imread(os.path.join(raw_dir, raw_name))

        if mask is None or raw is None:
            print(f"Error reading {mask_name} or {raw_name}. Skipping...")
            continue
        # print(f"np.unique(binary_mask)= {np.unique(mask)}")
        # exit()
        # Convert the mask to a binary image
        # binary_mask = cv2.threshold(mask, 38, 255, cv2.THRESH_BINARY)[1] # pixel = 38 means crack 
        # Threshold for crack pixels (value to be set to 255)
        crack_threshold = 38

        # Values to set to 0
        zero_values = [0, 75]

        # Create a new binary mask with desired values
        binary_mask = np.zeros_like(mask)  # Create a zero-filled mask of the same shape

        # Set crack_threshold value to 255
        binary_mask[mask == crack_threshold] = 255

        # Set zero_values to 0
        for value in zero_values:
            binary_mask[mask == value] = 0
        # Get the dimensions of the mask and raw images
        mask_height, mask_width = binary_mask.shape[:2]
        raw_height, raw_width = raw.shape[:2]

        # Resize the mask to match the dimensions of the raw image
        binary_mask = cv2.resize(binary_mask, (raw_width, raw_height))

        # Create a weight map for the mask
        # weight_map = cv2.addWeighted(binary_mask, 0.5, binary_mask, 0.5, 0)
        
        # ... (Your code for loading images, etc.)

        # Create a base image filled with black (no color initially)
        weight_map = np.zeros((raw_height, raw_width, 3), dtype=np.uint8) 

        # Find the locations in the binary mask where there are cracks
        crack_locations = np.where(binary_mask != 0)  

        # Set the crack areas to green in the weight map
        weight_map[crack_locations] = (0, 120, 0)   # BGR for a green color

        # Now overlay the weight map directly onto the original image:
        overlay = cv2.addWeighted(raw, 1, weight_map, 0.5, 0) 

        # Save the intermediate results
        # cv2.imwrite(os.path.join(output_dir, f"{raw_name}_mask.jpg"), mask)
        # cv2.imwrite(os.path.join(output_dir, f"{raw_name}_binary_mask.jpg"), binary_mask)
        # cv2.imwrite(os.path.join(output_dir, f"{raw_name}_weight_map.jpg"), weight_map)

        # Save the overlaid image to the output directory
        output_name = os.path.join(output_dir, raw_name)
        cv2.imwrite(output_name, overlay)
        print(f"Saved {output_name}")

print("Processing complete!")
