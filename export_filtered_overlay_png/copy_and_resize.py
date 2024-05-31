import os
import shutil
from PIL import Image

def copy_and_resize(input_folder, output_folder, new_width=800):
    """Copies and resizes filtered_overlay.png images from subfolders in the input folder to the output folder.

    Args:
        input_folder (str): Path to the folder containing subfolders with images.
        output_folder (str): Path to the destination folder for the resized images.
        new_width (int, optional): The desired width for the resized images (default is 800 pixels).
    """

    os.makedirs(output_folder, exist_ok=True)  

    for subfolder in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder)

        if os.path.isdir(subfolder_path):
            filtered_overlay_path = os.path.join(subfolder_path, "filtered_overlay.png")

            if os.path.exists(filtered_overlay_path):
                new_filename = os.path.join(output_folder, subfolder)

                # Open the image
                img = Image.open(filtered_overlay_path)

                # Calculate the new height to maintain aspect ratio
                width, height = img.size
                new_height = int(new_width * height / width)

                # Resize the image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS) 

                # Save the resized image
                resized_img.save(new_filename) 
                print(f"Copied and resized {filtered_overlay_path} to {new_filename}")
            else:
                print(f"Warning: filtered_overlay.png not found in {subfolder_path}")

# --- (Use the same input/output paths as before) ---
# Get the input and output folder paths 
input_folder = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/curve"
output_folder = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/nn_filtered_crack_overlay"

copy_and_resize(input_folder, output_folder) 
