import configparser
import shutil
from configparser import ConfigParser
import os


def UpdateRawMaskOverlayConfigs():
    config: ConfigParser = configparser.ConfigParser()
    config.read("config.ini")
    output_directory = config["Settings"]["output_directory"]

    config["CrackSegmentation"]["mask_directory"] = output_directory + "/crackmask"
    config["CrackSegmentation"]["mask_dir_Message"] = "mask_directory is auto-generated."

    config["StainSegmentation"]["mask_directory"] = output_directory + "/stainmask"
    config["StainSegmentation"]["mask_dir_Message"] = "mask_directory is auto-generated."

    config["CrackOverlay"]["overlay_directory"] = output_directory + "/crackoverlay/images"
    config["CrackOverlay"]["overlay_dir_Message"] = "overlay_directory is auto-generated."

    config["StainOverlay"]["overlay_directory"] = output_directory + "/stainoverlay/images"
    config["StainOverlay"]["overlay_dir_Message"] = "overlay_directory is auto-generated."


    # Write the updated config file
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    # Copy the config.ini file to the run directory
    config_file = os.path.join("config.ini")
    if os.path.exists(config_file):
        shutil.copy(config_file, os.path.join(output_directory, "updated_config.ini"))


UpdateRawMaskOverlayConfigs()
