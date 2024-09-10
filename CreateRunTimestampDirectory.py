#Script name: CreateRunTimestampDirectory.py
import os
import datetime
import shutil
import configparser


def create_run_directory():
    # Read the video path from the ini file
    config = configparser.ConfigParser()
    config.read("config.ini")
    image_path = config["Settings"]["image_path"]

    # Create the output directory
    output_directory = os.path.splitext(image_path)[0] + "_out"

    # Add the output directory line to the config file
    config["Settings"]["output_directory"] = output_directory
    config["Settings"]["output_dir_Message"] = "output_directory is auto-generated."

    # Write the updated config file
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Copy the config.ini file to the run directory
    config_file = os.path.join("config.ini")
    if os.path.exists(config_file):
        shutil.copy(config_file, os.path.join(output_directory, "previous_config.ini"))

# Call the function to create a run directory
create_run_directory()
