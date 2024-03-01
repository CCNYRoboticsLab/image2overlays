import argparse
import subprocess
import configparser
import os

def get_overlay_directory(overlay_images_directory):
    """Removes the 'images' part at the end of a given path.

    Args:
        path (str): The original file system path.

    Returns:
        str: The modified path without the 'images' segment.
    """

    parts = overlay_images_directory.split(os.sep)  # Split the path using the OS-specific separator

    # Handle potential scenarios:
    if parts[-1] == "images":  # 'images' is the last segment
        parts = parts[:-1]
    elif parts[-2] == "images":  # 'images' is the second-to-last segment
        parts = parts[:-2]
    else:
        print(f"Warning: 'images' directory not found in the expected location within the path '{overlay_images_directory}'")

    return os.sep.join(parts)
def get_las_file(overlay_images_directory):
    overlay_directory = get_overlay_directory(overlay_images_directory)
    return os.path.join(
        overlay_directory, "odm_georeferencing", "odm_georeferenced_model.laz"
    )
def get_potree_output_directory(overlay_images_directory):
    overlay_directory = get_overlay_directory(overlay_images_directory)
    return os.path.join(
        overlay_directory, "potree"
    )
def run_PotreeConverter(damage_type):
    """Executes the PotreeConverter command with a project path based on damage type.

    Args:
        damage_type (str): The type of damage (either 'crack' or 'stain').
    """

    config = configparser.ConfigParser()
    config.read('config.ini')  # Read your config file

    if damage_type == 'crack':
        overlay_images_directory = config['CrackOverlay']['overlay_directory']
    elif damage_type == 'stain':
        overlay_images_directory = config['StainOverlay']['overlay_directory']
    else:
        raise ValueError("Invalid damage_type. Must be 'crack' or 'stain'.")

    command = [
        "/home/roboticslab/Downloads/PotreeConverter-2.1.1/build/PotreeConverter",
        f"{get_las_file(overlay_images_directory)}",
        "-o",
        f"{get_potree_output_directory(overlay_images_directory)}"
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OpenDroneMap with damage-specific overlays.")
    parser.add_argument("--damage_type", choices=['crack', 'stain'], required=True, help="Type of damage: crack or stain")  # Optional argument 
    args = parser.parse_args()


    run_PotreeConverter(args.damage_type)
