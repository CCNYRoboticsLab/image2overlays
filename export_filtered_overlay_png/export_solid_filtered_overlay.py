import os
import shutil


def copy_filtered_overlays(input_folder, output_folder):
    """Copies filtered_overlay.png images from subfolders in the input folder to the output folder.

    Args:
        input_folder (str): Path to the folder containing subfolders with images.
        output_folder (str): Path to the destination folder for the filtered overlay images.
    """

    os.makedirs(
        output_folder, exist_ok=True
    )  # Create output folder if it doesn't exist

    for subfolder in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder)

        # Check if the item is a directory (we're expecting folders like S1074591.png)
        if os.path.isdir(subfolder_path):
            filtered_overlay_path = os.path.join(
                subfolder_path, "solid_filtered_overlay.png"
            )

            # Check if filtered_overlay.png exists in the subfolder
            if os.path.exists(filtered_overlay_path):
                # Construct the new filename in the output folder (using the subfolder name)
                new_filename = os.path.join(output_folder, subfolder)
                shutil.copy2(filtered_overlay_path, new_filename)  # Copy with metadata
                print(f"Copied {filtered_overlay_path} to {new_filename}")
            else:
                print(f"Warning: filtered_overlay.png not found in {subfolder_path}")


# Get the input and output folder paths
input_folder = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/curve"
output_folder = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images_out/2024-04-26_07-29-38/nn_solidfiltered_crack_overlay"

# Call the function to copy the images
copy_filtered_overlays(input_folder, output_folder)
