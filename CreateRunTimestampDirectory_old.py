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
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)
    #
    # # Print a message to confirm that the folder was created
    # print(f"Created output directory: {output_directory}")

    # # Create the output directory
    # output_directory = os.path.splitext(video_path)[0] + "_out"

    # Get the current time and date
    now = datetime.datetime.now()

    # Format the time and date into a string
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Create the run_timestamp directory
    run_directory: str = os.path.join(output_directory, timestamp)

    # Add the output directory line to the config file
    config["Settings"]["output_directory"] = run_directory
    config["Settings"]["output_dir_Message"] = "output_directory is auto-generated."

    # Write the updated config file
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    if not os.path.exists(run_directory):
        os.makedirs(run_directory)

    # Copy the config.ini file to the run directory
    config_file = os.path.join("config.ini")
    if os.path.exists(config_file):
        shutil.copy(config_file, os.path.join(run_directory, "previous_config.ini"))

    # Create output directories for related output folders
    # output_directories = ["output", "images", "logs"]
    # for output_directory in output_directories:
    #     output_path = os.path.join(run_directory, output_directory)
    #     if not os.path.exists(output_path):
    #         os.makedirs(output_path)


# Call the function to create a run directory
create_run_directory()
