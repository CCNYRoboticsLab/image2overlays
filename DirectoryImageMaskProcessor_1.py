from PIL import Image
import numpy as np
import os


class DirectoryImageMaskProcessor:
    def __init__(self, input_directory):
        self.input_directory = input_directory
        parent_directory = os.path.dirname(input_directory)
        self.red_output_directory = os.path.join(parent_directory, "red_crack_masks")
        self.green_output_directory = os.path.join(
            parent_directory, "green_spall_masks"
        )

    def process_directory(self):
        # Ensure the output directories exist
        os.makedirs(self.red_output_directory, exist_ok=True)
        os.makedirs(self.green_output_directory, exist_ok=True)

        # Process each image in the input directory
        for image_file in os.listdir(self.input_directory):
            if image_file.lower().endswith(("png", "jpg", "jpeg")):
                self.process_image(image_file)

    def process_image(self, image_file):
        # Load and convert the image
        image_path = os.path.join(self.input_directory, image_file)
        image = Image.open(image_path).convert("RGBA")

        # Split the loaded image into separate channels
        r, g, b, a = image.split()

        # Create and save the red and green masks
        self.create_and_save_mask(
            r, image_file, self.red_output_directory, mask_type="red"
        )
        self.create_and_save_mask(
            g, image_file, self.green_output_directory, mask_type="green"
        )

    def create_and_save_mask(self, channel, image_file, output_directory, mask_type):
        # Create a mask from the given channel
        mask = Image.merge(
            "RGBA",
            (
                channel if mask_type == "red" else Image.new("L", channel.size, 0),
                channel if mask_type == "green" else Image.new("L", channel.size, 0),
                Image.new("L", channel.size, 0),
                channel,
            ),
        )

        # Define the full path for the mask
        mask_path = os.path.join(output_directory, image_file)

        # Save the mask
        mask.save(mask_path)


# Example usage
if __name__ == "__main__":
    input_directory = (
        "images_folder"  # This directory should contain the images to process.
    )

    processor = DirectoryImageMaskProcessor(input_directory)
    processor.process_directory()

    print(
        f"Processing complete. Check the parent directory of '{input_directory}' for the results."
    )
