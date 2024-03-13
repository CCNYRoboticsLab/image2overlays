#!~/anaconda3/bin/python
import subprocess
from datetime import datetime

# Define flags for processing
process_crack = False
process_stain = False
process_spall = True


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
    # Construct the command to run the script within the Conda environment
    command = f"/bin/bash -c 'source /home/roboticslab/anaconda3/bin/activate {conda_env_name} && {script_command}'"
    # Execute the command
    subprocess.call(command, shell=True)


def main():  # sourcery skip: extract-duplicate-method
    # Replace your existing subprocess.call lines with call_in_conda_env function calls

    # Create output folder, run_timestamp subfolder
    log_message("Create output folder, run_timestamp subfolder.")
    call_in_conda_env("python CreateRunTimestampDirectory.py")

    # UpdateRawMaskOverlayConfigs.py
    log_message("Create raw, mask, overlay, mvs folders in run_timestamp folder.")
    call_in_conda_env("python UpdateRawMaskOverlayConfigs.py")

    if process_crack:
        # Run crack related processing
        log_message("Running crack segmentation...")
        call_in_conda_env("python cracksegmentation.py")

        log_message("Converting crack masks to 3 categories according to directions...")
        call_in_conda_env("python crack23directions.py")

        log_message("Running crack overlay...")
        call_in_conda_env("python crackoverlay.py")

        log_message("Copying geolocation info to crack overlay...")
        call_in_conda_env("python copy_geolocation_crack.py")

        log_message("Convert overlay images to pointcloud. ")
        call_in_conda_env("python overlay2pointcloud.py --damage_type crack")

        if process_spall:
            log_message("Creating spall overlay...")
            call_in_conda_env("python3 crackmask2spalloverlay.py")

            log_message("Copying geolocation info to spall overlay...")
            call_in_conda_env("python3 copy_geolocation_spall.py")

            log_message("las2potree for spall overlay")
            call_in_conda_env("python3 overlay2pointcloud.py --damage_type spall")

            log_message("Convert to Potree. ")
            call_in_conda_env("python3 las2potree.py --damage_type spall")

    if process_stain:
        # Run stain related processing
        log_message("Running stain segmentation...")
        call_in_conda_env("python stainsegmentation.py")

        log_message("Running stain overlay...")
        call_in_conda_env("python stainoverlay.py")

        log_message("Copying geolocation info to stain overlay...")
        call_in_conda_env("python3 copy_geolocation_stain.py")

        log_message("Convert overlay images to pointcloud. ")
        call_in_conda_env("python3 overlay2pointcloud.py --damage_type stain")

        log_message("Convert to Potree. ")
        call_in_conda_env("python3 las2potree.py --damage_type stain")

    log_message("Script sequence completed.")


if __name__ == "__main__":
    main()
