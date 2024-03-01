#!~/anaconda3/bin/python
#Copy geolocation data to stain overlay images
import configparser
from main import log_message, call_in_conda_env

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Extract image_path and overlay_directory from the config file
image_path = config['Settings']['image_path']
overlay_directory = config['StainOverlay']['overlay_directory']
# The path to your copy_geolocation.py script
copy_geolocation_script_path = 'copy_geolocation.py'

# Call copy_geolocation.py with the extracted paths
call_in_conda_env(f"python {copy_geolocation_script_path} {image_path} {overlay_directory}", "/home/roboticslab/Developer/image2overlays/.conda")

log_message("Copying geolocation info to stain overlay...")