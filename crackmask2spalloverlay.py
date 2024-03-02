import cv2
import os
import configparser

def get_spall_overlay_directory(crack_overlay_directory):
    return crack_overlay_directory.replace("crackoverlay", "spalloverlay")

def main():
    # Load the INI file and parse it
    config = configparser.ConfigParser()
    config.read("config.ini")  # Replace with the actual path to your INI file

    # Paths for the mask images, raw images, and output images
    # Read from the INI file
    mask_dir = config["CrackSegmentation"]["mask_directory"]
    raw_dir = config["Settings"]["image_path"]
    crack_overlay_directory = config["CrackOverlay"]["overlay_directory"]
    spall_overlay_directory = get_spall_overlay_directory(crack_overlay_directory)

    # Ensure the output directory exists
    if not os.path.exists(spall_overlay_directory):
        os.makedirs(spall_overlay_directory)

    # Iterate over the files in the mask directory
    for mask_name in os.listdir(mask_dir):
        # Extract the image name from the filename
        raw_name = mask_name.split(".")[0] + ".JPG"

        # Load the mask and raw images
        mask = cv2.imread(os.path.join(mask_dir, mask_name), cv2.IMREAD_GRAYSCALE)
        raw = cv2.imread(os.path.join(raw_dir, raw_name))
        if mask is None or raw is None:
            print(f"Error reading {mask_name} or {raw_name}. Skipping...")
            continue
        print(raw.shape)
        print(mask.shape)

        # Where the mask is white, set the raw image to red
        # raw[mask == 38] = [0, 0, 255]
        raw[mask == 75] = [0, 0, 255]
        # Save the overlaid image to the output directory
        spall_overlaid_image_path = os.path.join(spall_overlay_directory, raw_name)
        cv2.imwrite(spall_overlaid_image_path, raw)
        print(f"Saved {spall_overlaid_image_path}")

    print("Processing complete!")

if __name__ == "__main__":
    main()
