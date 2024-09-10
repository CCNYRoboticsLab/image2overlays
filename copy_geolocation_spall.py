#!~/anaconda3/bin/python
# Copy geolocation data to crack overlay images
import configparser
import subprocess
from main import log_message, call_in_conda_env
from crackmask2spalloverlay import get_spall_overlay_directory

# Load the configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Extract image_path and mask_directory from the config file
raw_image_directory = config["Settings"]["image_path"]
# Assuming you want to use CrackSegmentation's mask_directory for this example
# mask_directory = config['CrackSegmentation']['mask_directory']
crack_overlay_directory = config["CrackOverlay"]["overlay_directory"]
spall_overlay_directory = crack_overlay_directory.replace(
    "crackoverlay", "filteredSpallOverlay"
)
# The path to your copy_geolocation.py script
copy_geolocation_script_path = "copy_geolocation.py"

# Call copy_geolocation.py with the extracted paths
# subprocess.run(['python', copy_geolocation_script_path, image_path, mask_directory], check=True)
# call_in_conda_env(f"python {copy_geolocation_script_path} {image_path} {mask_directory}", "/home/roboticslab/Developer/image2overlays/.conda")
call_in_conda_env(
    f"python {copy_geolocation_script_path} {raw_image_directory} {spall_overlay_directory}",
    "/home/roboticslab/Developer/image2overlays/.conda",
)

log_message("Copying geolocation info to spall overlay...")
