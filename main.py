#!~/anaconda3/bin/python
import subprocess
from datetime import datetime

# Define flags for processing
process_crack = False
process_stain = True

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: {message}")

def call_in_conda_env(script_command):
    # Define the Conda environment name
    conda_env_name = "visualinspection113"
    # Construct the command to run the script within the Conda environment
    command = f"/bin/bash -c 'conda run -n {conda_env_name} --no-capture-output {script_command}'"
    # Execute the command
    subprocess.call(command, shell=True)

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
    
    log_message("Running crack overlay...")
    call_in_conda_env("python crackoverlay.py")

if process_stain:
    # Run stain related processing
    log_message("Running stain segmentation...")
    call_in_conda_env("python stainsegmentation.py")
    
    log_message("Running stain overlay...")
    call_in_conda_env("python stainoverlay.py")

log_message("Script sequence completed.")
