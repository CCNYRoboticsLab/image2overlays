import os
import shutil
from PIL import Image
from multiprocessing import Pool

def process_image(args):
    """Processes a single image: copies and resizes it.

    Args:
        args (tuple): A tuple containing (subfolder_path, output_folder, new_width)
    """

    subfolder_path, output_folder, new_width = args  # Unpack the arguments
    filtered_overlay_path = os.path.join(subfolder_path, "filtered_overlay.png")

    if os.path.exists(filtered_overlay_path):
        new_filename = os.path.join(output_folder, os.path.basename(subfolder_path))

        img = Image.open(filtered_overlay_path)
        width, height = img.size
        new_height = int(new_width * height / width)

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_img.save(new_filename)
        print(f"Copied and resized {filtered_overlay_path} to {new_filename}")
    else:
        print(f"Warning: filtered_overlay.png not found in {subfolder_path}")

def copy_and_resize_parallel(input_folder, output_folder, new_width=800):
    """Copies and resizes images in parallel using multiprocessing.

    Args:
        input_folder (str): Path to the folder containing subfolders with images.
        output_folder (str): Path to the destination folder for the resized images.
        new_width (int, optional): The desired width for the resized images (default is 800 pixels).
    """
    
    os.makedirs(output_folder, exist_ok=True)

    # Prepare arguments for each image (subfolder)
    args = [(os.path.join(input_folder, subfolder), output_folder, new_width) 
            for subfolder in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, subfolder))]

    # Use a Pool of workers to process images in parallel
    with Pool() as pool:  # Automatically uses the optimal number of processes based on your CPU cores
        pool.map(process_image, args)


# --- (Use the same input/output paths as before) ---
input_folder = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/curve"
output_folder = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/nn_filtered_crack_overlay"

copy_and_resize_parallel(input_folder, output_folder) 
