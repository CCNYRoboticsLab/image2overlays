import os
import configparser
from pathlib import Path
from PIL import Image

# Get the directory of the current script
script_dir = Path(__file__).parent.absolute()

# Set the path to config.ini based on the script directory
config_ini_path = script_dir / "config.ini"
print(config_ini_path)

# Read parameters from config.ini using Python
config = configparser.ConfigParser()
config.read(config_ini_path)

raw_directory = config["Settings"]["image_path"]
mask_directory = config["CrackSegmentation"]["mask_directory"].replace(
    "crackmask", "concretemask"
)
config_param = config["CrackSegmentation"]["config"]
model = "saved/UperNet/01-17_12-56/best_model.pth"  # concreteNet

print(f"RAW_DIR={raw_directory}")
print(f"MASK_DIR={mask_directory}")
print(f"CONFIG={config_param}")
print(f"MODEL={model}")

# Ensure the mask_directory exists
os.makedirs(mask_directory, exist_ok=True)
print(f"Ensured existence of directory: {mask_directory}")

# Get the model path
model_path = (
    Path("/home/roboticslab/Developer/pytorch_concrete_flaws_segmentation") / model
)
print(f"MODEL_PATH={model_path}")

# Define the directory where inference.py is located
pytorch_segmentation_dir = (
    "/home/roboticslab/Developer/pytorch_concrete_flaws_segmentation"
)


def resize_image(image_path, output_dir, max_size):
    """
    Resizes an image to fit within a maximum dimension while preserving aspect ratio.

    Args:
        image_path (string): Path to the input image.
        output_dir (string): Path to the output directory for resized images.
        max_size (int): The maximum width or height of the resized image.
    """
    image = Image.open(image_path)
    width, height = image.size

    if width > height:
        scale = max_size / width
    else:
        scale = max_size / height

    new_width = int(width * scale)
    new_height = int(height * scale)
    new_size = (new_width, new_height)

    resized_image = image.resize(new_size, Image.LANCZOS)
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, filename)
    resized_image.save(output_path)


# Create the output directory
downsized_dir = os.path.join(os.path.dirname(raw_directory), "downsized_raw")
os.makedirs(downsized_dir, exist_ok=True)
max_size = 1024
# Resize and save images in the downsized directory
for filename in os.listdir(raw_directory):
    if (
        filename.endswith(".jpg")
        or filename.endswith(".png")
        or filename.endswith(".JPG")
    ):
        image_path = os.path.join(raw_directory, filename)
        new_size = (512, 512)  # Adjust this to your desired size
        resize_image(image_path, downsized_dir, max_size)
