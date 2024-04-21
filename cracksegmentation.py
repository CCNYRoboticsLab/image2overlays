# This script is to replace "segmentation.sh"
import os
import configparser
from pathlib import Path

# Get the directory of the current script
script_dir = Path(__file__).parent.absolute()

# Set the path to config.ini based on the script directory
config_ini_path = script_dir / "config.ini"
print(config_ini_path)

# Read parameters from config.ini using Python
config = configparser.ConfigParser()
config.read(config_ini_path)

raw_directory = config["Settings"]["image_path"]
mask_directory = config["CrackSegmentation"]["mask_directory"]
config_param = config["CrackSegmentation"]["config"]
model = config["CrackSegmentation"]["model"]

print(f"RAW_DIR={raw_directory}")
print(f"MASK_DIR={mask_directory}")
print(f"CONFIG={config_param}")
print(f"MODEL={model}")

# Ensure the mask_directory exists
# os.makedirs(mask_directory, exist_ok=True)
# print(f"Ensured existence of directory: {mask_directory}")
# Ensure the output directory exists
if not os.path.exists(mask_directory):
    os.makedirs(mask_directory)

# Get the model path
model_path = Path("/home/roboticslab/Developer/pytorch_concrete_flaws_segmentation") / model
print(f"MODEL_PATH={model_path}")

# Define the directory where inference.py is located
pytorch_segmentation_dir = "/home/roboticslab/Developer/pytorch_concrete_flaws_segmentation"

# Combined command to activate conda environment and run the Python script
# source '/home/roboticslab/miniconda3/etc/profile.d/conda.sh' && \
# conda activate visualinspection113 && \
command = f"""
cd "{pytorch_segmentation_dir}" && python3 inference.py \
    --config "{config_param}" \
    --model "{model_path}" \
    --images "{raw_directory}" \
    --output "{mask_directory}" \
    --extension jpg png JPG
"""

os.system(command)
