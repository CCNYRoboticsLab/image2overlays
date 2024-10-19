#!~/anaconda3/bin/python
import subprocess
from datetime import datetime
import os
import argparse
# import yaml
import configparser
import sys
# test

# Define flags for processing
concrete_mask = True
process_crack = True
process_stain = True
process_spall = True  # if crack is not processed, spall won't be processed.
concrete_post_filter = True


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: {message}")


def call_in_conda_env(script_command, conda_env_name="visualinspection113"):
    """
    Executes a given script command within a specified Conda environment.

    Parameters:
    - script_command: The command to run within the Conda environment.
    - conda_env_name: Optional. The name of the Conda environment to activate. Defaults to "visualinspection113".
    """
    # Try to find the conda activation script
    conda_paths = [
        "/home/roboticslab/anaconda3/bin/activate",  # Original path
        "/opt/conda/bin/activate",  # Docker-style path
        os.path.expanduser("~/anaconda3/bin/activate"),  # User's home directory
        os.path.expanduser("~/miniconda3/bin/activate"),  # Miniconda in user's home
        "/usr/local/anaconda3/bin/activate",  # System-wide Anaconda
    ]

    activate_path = next((path for path in conda_paths if os.path.exists(path)), None)

    if not activate_path:
        raise EnvironmentError("Could not find Conda activation script. Please specify the correct path.")

    # Construct the command to run the script within the Conda environment
    command = f"/bin/zsh -c 'source {activate_path} {conda_env_name} && {script_command}'"
    
    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_message(f"Error executing command: {e}")
        raise


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--concrete_mask', action='store_true')
    parser.add_argument('--process_crack', action='store_true')
    parser.add_argument('--process_stain', action='store_true')
    parser.add_argument('--process_spall', action='store_true')
    parser.add_argument('--concrete_post_filter', action='store_true')
    return parser.parse_args()


# def load_config():
#     with open('config.yaml', 'r') as f:
#         return yaml.safe_load(f)


def main():
    # config = load_config()
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Use config['concrete_mask'], config['process_crack'], etc.
    # ...

    # Replace your existing subprocess.call lines with call_in_conda_env function calls

    # Create output folder, run_timestamp subfolder
    log_message("Create output folder, run_timestamp subfolder.")
    call_in_conda_env("python CreateRunTimestampDirectory.py")

    # UpdateRawMaskOverlayConfigs.py
    log_message("Create raw, mask, overlay, mvs folders in run_timestamp folder.")
    call_in_conda_env("python UpdateRawMaskOverlayConfigs.py")

    if concrete_mask:
        log_message("Running concrete mask...")
        call_in_conda_env("python concretemask.py")

    #     log_message("Running filter raw...")
    #     call_in_conda_env("python filterRaw.py")

    # Run crack related processing

    if process_crack:
        # Run crack related processing
        log_message("Running crack segmentation...")
        call_in_conda_env("python cracksegmentation.py")
        # Produces: run_timestamp/mask/crack_mask

        # log_message("Running concrete mask...")
        # call_in_conda_env("python concretemask.py")
        # Produces: run_timestamp/mask/concrete_mask

        if concrete_post_filter:
            log_message("Running concrete post filter...")
            call_in_conda_env("python concretePostFilter.py")
            # Updates: run_timestamp/mask/crack_mask
            
        print(sys.argv[0])
        if sys.argv[0] == 'T':
            log_message("Converting crack masks to 3 categories according to directions...")
            call_in_conda_env("python crack23directions.py")
            # Produces: run_timestamp/mask/crack_mask_3directions

            log_message("Running crack2curve...")
            call_in_conda_env("python crack2curve.py")
            # Produces: run_timestamp/mask/crack_curve

        # # Export nnfilteredCrackOverlay
        # log_message("Export nnfilteredCrackOverlay...")
        # call_in_conda_env("python export_filtered_overlay_png/export_nn_filtered_mask.py")

        log_message("Running crack overlay...")
        call_in_conda_env("python crackoverlay_transparent.py")
        # Produces: run_timestamp/overlay/crack_overlay and filteredCrackOverlay and nnfilteredCrackOverlay?

        # log_message("Copying geolocation info to crack overlay...")
        # call_in_conda_env("python copy_geolocation_crack.py")

        # log_message("Convert overlay images to pointcloud. ")
        # call_in_conda_env("python overlay2pointcloud.py --damage_type crack")

        if process_spall:
            log_message("Creating spall overlay...")
            call_in_conda_env("python3 crackmask2spalloverlay_transparent.py")

        #     log_message("Copying geolocation info to spall overlay...")
        #     call_in_conda_env("python3 copy_geolocation_spall.py")

        #     log_message("las2potree for spall overlay")
        #     call_in_conda_env("python3 overlay2pointcloud.py --damage_type spall")

        #     log_message("Convert to Potree. ")
        #     call_in_conda_env("python3 las2potree.py --damage_type spall")

    if process_stain:
        # Run stain related processing
        log_message("Running stain segmentation...")
        call_in_conda_env("python stainsegmentation.py")

        if concrete_post_filter:
            log_message("Running concrete post filter...")
            call_in_conda_env("python concretePostFilterStain.py")

        log_message("Running stain overlay...")
        call_in_conda_env("python stainoverlay_transparent.py")
        exit()

        # log_message("Copying geolocation info to stain overlay...")
        # call_in_conda_env("python3 copy_geolocation_stain.py")

        # log_message("Convert overlay images to pointcloud. ")
        # call_in_conda_env("python3 overlay2pointcloud.py --damage_type stain")

        # log_message("Convert to Potree. ")
        # call_in_conda_env("python3 las2potree.py --damage_type stain")

    log_message("Script sequence completed.")


if __name__ == "__main__":
    main()
