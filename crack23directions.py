# This script is to parse the ini file to:
# - get the path for crack_spall mask file
# - get the path for '3masks' folder and make sure it exist
# - extract only the crack mask
# - convert this crack mask into 3 masks based on crack direction and save them into the '3masks' folder
import os
import configparser
from pathlib import Path

from DirectoryImageMaskProcessor_1 import DirectoryImageMaskProcessor


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

    def get_crack_spall_mask_path(self):
        return self.mask_directory

    def get_and_ensure_3masks_directory(self):
        # Replace 'crackmask' with '3masks' in the mask_directory path
        masks_directory = self.mask_directory.replace("crackmask", "3masks")

        # Ensure the '3masks' directory exists
        if not os.path.exists(masks_directory):
            os.makedirs(masks_directory)
            print(f"Ensured existence of directory: {masks_directory}")

        return masks_directory


# Main part of the script
if __name__ == "__main__":
    script_dir = Path(__file__).parent.absolute()
    config_ini_path = script_dir / "config.ini"
    print(f"Config INI Path: {config_ini_path}")

    processor = CrackMaskProcessor(config_ini_path)
    processor.ensure_directories_exist()

    crack_spall_mask_path = processor.get_crack_spall_mask_path()
    print(f"Crack/Spall Mask Path: {crack_spall_mask_path}")

    masks_directory_path = processor.get_and_ensure_3masks_directory()
    print(f"'3masks' Directory Path: {masks_directory_path}")

    # Extracting red crack images into a seperate file
    input_directory = crack_spall_mask_path

    processor = DirectoryImageMaskProcessor(input_directory)
    processor.process_directory()

    print(
        f"Processing complete. Check the parent directory of '{input_directory}' for the results."
    )
