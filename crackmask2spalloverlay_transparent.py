import cv2
import os
import configparser

import numpy as np

def get_spall_overlay_directory(crack_overlay_directory):
    return crack_overlay_directory.replace("filteredCrackOverlays", "filteredSpallOverlays")

def main():
    # Load the INI file and parse it
    config = configparser.ConfigParser()
    config.read("config.ini")  # Replace with the actual path to your INI file

    # Paths for the mask images, raw images, and output images
    # Read from the INI file
    mask_dir = config["CrackSegmentation"]["mask_directory"].replace("crackmask", "filteredCrackMasks")
    raw_dir = config["Settings"]["image_path"]
    crack_overlay_directory = config["CrackOverlay"]["overlay_directory"].replace("crackoverlay", "filteredCrackOverlays")
    spall_overlay_directory = get_spall_overlay_directory(crack_overlay_directory)

    # Ensure the output directory exists
    if not os.path.exists(spall_overlay_directory):
        os.makedirs(spall_overlay_directory)

    # Iterate over the files in the mask directory
    for mask_name in os.listdir(mask_dir):
        # Extract the image name from the filename
        raw_name_base = mask_name.split(".")[0]
        raw_name_jpg = f"{raw_name_base}.jpg"
        raw_name_JPG = f"{raw_name_base}.JPG"

        # Check for the existence of the raw image file with both extensions
        raw_path_jpg = os.path.join(raw_dir, raw_name_jpg)
        raw_path_JPG = os.path.join(raw_dir, raw_name_JPG)

        if os.path.exists(raw_path_jpg):
            raw_path = raw_path_jpg
        elif os.path.exists(raw_path_JPG):
            raw_path = raw_path_JPG
        else:
            print(f"Error: Raw image file not found for {mask_name}. Skipping...")
            continue
        
        # Load the mask and raw images
        mask = cv2.imread(os.path.join(mask_dir, mask_name), cv2.IMREAD_GRAYSCALE)
        raw = cv2.imread(raw_path)
        if mask is None or raw is None:
            print(f"Error reading {mask_name} or {raw_path}. Skipping...")
            continue
        print(raw.shape)
        print(mask.shape)

        # Where the mask is white, set the raw image to red
        # raw[mask == 38] = [0, 0, 255]
        # raw[mask == 75] = [255, 0, 0]
        
        # Create an empty weight map with the same dimensions as the raw image
        weight_map = np.zeros_like(raw)  
        
        # Set pixels where mask == 38 to the color [0, 0, 255] (blue)
        weight_map[mask == 75] = [255, 0, 0] 

        # Overlay the weight map onto the original image
        overlay = cv2.addWeighted(raw, 1, weight_map, 0.7, 0) 
        
        # Save the overlaid image to the output directory
        spall_overlaid_image_path = os.path.join(spall_overlay_directory, os.path.basename(raw_path))
        cv2.imwrite(spall_overlaid_image_path, overlay)
        print(f"Saved {spall_overlaid_image_path}")

    print("Processing complete!")

if __name__ == "__main__":
    main()
