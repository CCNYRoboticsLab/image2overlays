import argparse
import subprocess
import configparser
import os
from crackmask2spalloverlay import get_spall_overlay_directory

def remove_image_part(path):
    """Removes the 'images' part at the end of a given path.

    Args:
        path (str): The original file system path.

    Returns:
        str: The modified path without the 'images' segment.
    """

    parts = path.split(os.sep)  # Split the path using the OS-specific separator

    # Handle potential scenarios:
    if parts[-1] == "images":  # 'images' is the last segment
        parts = parts[:-1]
    elif parts[-2] == "images":  # 'images' is the second-to-last segment
        parts = parts[:-2]
    else:
        print(f"Warning: 'images' directory not found in the expected location within the path '{path}'")

    return os.sep.join(parts)
def run_odm(damage_type):
    """Executes the OpenDroneMap command with a project path based on damage type.

    Args:
        damage_type (str): The type of damage (either 'crack', 'stain', 'spall', or 'raw').
    """

    config = configparser.ConfigParser()
    config.read('config.ini')  # Read your config file

    if damage_type == 'crack':
        project_path = config['CrackOverlay']['overlay_directory']
    elif damage_type == 'stain':
        project_path = config['StainOverlay']['overlay_directory']
    elif damage_type == 'spall':
        project_path = get_spall_overlay_directory(config['CrackOverlay']['overlay_directory'])
    elif damage_type == 'raw':
        project_path = '/home/roboticslab/Downloads/OneDrive_2024-02-03/NYC Span 8-9/raw/images'  # Assuming you'll add this in config.ini
    else:
        raise ValueError("Invalid damage_type. Must be 'crack', 'spall', 'stain' or 'raw'.")

    command = [
        "docker", "run", "-ti", "--gpus", "all", "--rm",
        "-v", f"{remove_image_part(project_path)}:/datasets/code",
        "opendronemap/odm",
        "--project-path", "/datasets"
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OpenDroneMap with damage-specific overlays.")
    parser.add_argument("--damage_type", choices=['crack','spall', 'stain', 'raw'], default='raw', help="Type of damage: crack, spall, stain or raw.")  # Optional argument 
    args = parser.parse_args()


    run_odm(args.damage_type)
