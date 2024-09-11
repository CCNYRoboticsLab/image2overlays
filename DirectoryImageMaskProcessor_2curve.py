from PIL import Image
import os
from red2curve_nn import CrackClassifier


class DirectoryImageMaskProcessor_2curve:
    def __init__(self, raw_directory_path, input_directory):
        self.raw_directory_path = raw_directory_path
        self.input_directory = input_directory
        parent_directory = os.path.dirname(input_directory)
        # self.red_output_directory = os.path.join(parent_directory, "red_crack_masks")
        # self.green_output_directory = os.path.join(
        #     parent_directory, "green_spall_masks"
        # )
        # self.horizontal_masks_directory = os.path.join(
        #     parent_directory, "horizontal_crack_masks"
        # )
        # self.vertical_masks_directory = os.path.join(
        #     parent_directory, "vertical_crack_masks"
        # )
        # self.diagonal_masks_directory = os.path.join(
        #     parent_directory, "diagonal_crack_masks"
        # )
        self.output_directory = os.path.join(parent_directory, "curve")

    def process_directory(self):
        # Ensure the output directories exist
        # os.makedirs(self.red_output_directory, exist_ok=True)
        # os.makedirs(self.green_output_directory, exist_ok=True)
        # os.makedirs(self.horizontal_crack_masks, exist_ok=True)
        # os.makedirs(self.vertical_crack_masks, exist_ok=True)
        # os.makedirs(self.diagonal_crack_masks, exist_ok=True)

        image_files = [
            f
            for f in os.listdir(self.input_directory)
            if f.lower().endswith(("png", "jpg", "jpeg"))
        ]
        total_images = len(image_files)
        print(f"Found {total_images} images to process.")
        


        for idx, red_mask_filename in enumerate(image_files, start=1):
            print(f"Processing image {idx}/{total_images}: {red_mask_filename}")
            # Construct the raw image path using the directory and filename
            raw_image_base = os.path.splitext(red_mask_filename)[0]
            raw_image_path = None
            for ext in ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']:
                potential_path = os.path.join(self.raw_directory_path, raw_image_base + ext)
                if os.path.exists(potential_path):
                    raw_image_path = potential_path
                    break
            
            if raw_image_path is None:
                print(f"Warning: No matching raw image found for {red_mask_filename}")
                continue
            
            self.process_image(raw_image_path, red_mask_filename)

        print("All images processed successfully.")

    def process_image(self, raw_image_path, image_file):
        # Load and convert the image
        image_path = os.path.join(self.input_directory, image_file)
        output_directory_w_filename = os.path.join(self.output_directory, image_file)
        CrackClassifier.classify_and_save_cracks(
            raw_image_path, image_path, output_directory_w_filename
        )
        print(f"Saved curved crack mask: {output_directory_w_filename}")
        # image = Image.open(image_path).convert("RGBA")

        # # Split the loaded image into separate channels
        # r, g, b, a = image.split()

        # # Create and save the red and green masks
        # self.create_and_save_mask(
        #     r, image_file, self.red_output_directory, mask_type="red"
        # )
        # self.create_and_save_mask(
        #     g, image_file, self.green_output_directory, mask_type="green"
        # )

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
        print(f"Saved {mask_type} mask: {mask_path}")


# Example usage
if __name__ == "__main__":
    input_directory = "images_folder"  # Adjust this path to your folder of images

    processor = DirectoryImageMaskProcessor_2curve(input_directory)
    processor.process_directory()

    print(
        f"Processing complete. Check the parent directory of '{input_directory}' for the 'red_crack_masks' and 'green_spall_masks' folders."
    )
