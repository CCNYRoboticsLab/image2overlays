# This script is to parse the ini file to:
# - get the path for crack_spall mask file
# - get the path for 'curve' folder and make sure it exist
# - extract only the crack mask
# - convert this crack mask into curve and straight and save curves into the 'curve' folder
import os
import configparser
from pathlib import Path

from DirectoryImageMaskProcessor_1 import DirectoryImageMaskProcessor
from DirectoryImageMaskProcessor_2curve import (
    DirectoryImageMaskProcessor_2curve,
)


class CrackMaskProcessor:
    def __init__(self, config_file):
        self.config_file = config_file
        self.raw_directory = None
        self.mask_directory = None
        self.config_param = None
        self.model = None
        self._parse_config()

    def _parse_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        self.raw_directory = config["Settings"]["image_path"]
        self.mask_directory = config["CrackSegmentation"]["mask_directory"]
        self.config_param = config["CrackSegmentation"]["config"]
        self.model = config["CrackSegmentation"]["model"]

        print(f"Configurations loaded:")
        print(f"RAW_DIR={self.raw_directory}")
        print(f"MASK_DIR={self.mask_directory}")
        print(f"CONFIG={self.config_param}")
        print(f"MODEL={self.model}")

    def ensure_directories_exist(self):
        if not os.path.exists(self.mask_directory):
            os.makedirs(self.mask_directory)
            print(f"Ensured existence of directory: {self.mask_directory}")

    def get_raw_directory_path(self):
        return self.raw_directory

    def get_crack_spall_mask_path(self):
        return self.mask_directory

    def get_red_crack_mask_path(self):
        return self.mask_directory.replace("crackmask", "red_crack_masks")

    # def get_and_ensure_3masks_directory(self):
    #     # Replace 'crackmask' with '3masks' in the mask_directory path
    #     masks_directory = self.mask_directory.replace("crackmask", "3masks")

    #     # Ensure the '3masks' directory exists
    #     if not os.path.exists(masks_directory):
    #         os.makedirs(masks_directory)
    #         print(f"Ensured existence of directory: {masks_directory}")

    #     return masks_directory
    
    def get_and_ensure_curve_directory(self):
        # Replace 'crackmask' with 'curve' in the mask_directory path
        masks_directory = self.mask_directory.replace("crackmask", "curve")

        # Ensure the 'curve' directory exists
        if not os.path.exists(masks_directory):
            os.makedirs(masks_directory)
            print(f"Ensured existence of directory: {masks_directory}")

        return masks_directory


# Main part of the script
def extract_crack(crack_spall_mask_path):
    input_directory = crack_spall_mask_path

    processor_extract_crack = DirectoryImageMaskProcessor(input_directory)
    processor_extract_crack.process_directory()

    print(
        f"Processing complete. Check the parent directory of '{input_directory}' for the results."
    )


if __name__ == "__main__":
    script_dir = Path(__file__).parent.absolute()
    config_ini_path = script_dir / "config.ini"
    print(f"Config INI Path: {config_ini_path}")

    processor = CrackMaskProcessor(config_ini_path)
    processor.ensure_directories_exist()
    
    raw_directory_path = processor.get_raw_directory_path()

    crack_spall_mask_path = processor.get_crack_spall_mask_path()
    print(f"Crack/Spall Mask Path: {crack_spall_mask_path}")

    # Extracting red crack images into a seperate file
    # extract_crack(crack_spall_mask_path)

    # Get red_crack_masks directory path
    red_crack_mask_path = processor.get_red_crack_mask_path()
    print(f"red_crack_mask Path: {red_crack_mask_path}")

    # Before processing the directory, ensure it exists
    os.makedirs(red_crack_mask_path, exist_ok=True)

    # Check if the directory is empty
    if not os.listdir(red_crack_mask_path):
        print(f"Warning: The directory '{red_crack_mask_path}' is empty.")
        print("Please ensure that the 'crack23directions.py' has been run and generated the red crack mask images.")
        exit(1)

    # List the files in the directory
    files = [f for f in os.listdir(red_crack_mask_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]
    print(f"Found {len(files)} image files in {red_crack_mask_path}")

    if not files:
        print("No image files found. Please check the file extensions and ensure the images are present.")
        exit(1)

    curve_directory_path = processor.get_and_ensure_curve_directory()
    processor_extract_3 = DirectoryImageMaskProcessor_2curve(raw_directory_path, red_crack_mask_path)
    processor_extract_3.process_directory()

    print(f"Processing complete. Check the directory '{curve_directory_path}' for the results.")
