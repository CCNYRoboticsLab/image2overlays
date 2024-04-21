import numpy as np
from skimage.measure import label, regionprops
from PIL import Image, ImageDraw
import os


class CrackClassifier:
    def __init__(self):
        pass

    @classmethod
    def classify_and_save_cracks(cls, red_mask_image_path, output_folder):
        # Load the red mask image
        red_mask = Image.open(red_mask_image_path)

        # Convert to numpy array and get the alpha channel as the mask
        red_mask_np = np.array(red_mask)
        alpha_channel = red_mask_np[
            :, :, 3
        ]  # Assuming the alpha channel is the last one

        # Label connected components
        labeled_mask = label(alpha_channel)

        # Analyze properties of labeled regions
        regions = regionprops(labeled_mask)

        # Placeholder for categorized cracks
        vertical_cracks = []
        horizontal_cracks = []
        diagonal_cracks = []

        # Classify based on orientation and aspect ratio
        for props in regions:
            y0, x0, y1, x1 = props.bbox
            region_height = y1 - y0
            region_width = x1 - x0
            aspect_ratio = region_width / float(region_height)

            if aspect_ratio > 2:
                horizontal_cracks.extend(props.coords)
            elif aspect_ratio < 0.5:
                vertical_cracks.extend(props.coords)
            else:
                # Diagonal classification can be refined as needed
                orientation = props.orientation
                if -np.pi / 4 <= orientation <= np.pi / 4:
                    horizontal_cracks.extend(props.coords)
                else:
                    diagonal_cracks.extend(props.coords)

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Image shape needed for mask creation
        image_shape = alpha_channel.shape

        # Save masks for each type of crack
        cls._save_crack_mask(
            vertical_cracks, f"{output_folder}/vertical_crack_mask.png", image_shape
        )
        cls._save_crack_mask(
            horizontal_cracks, f"{output_folder}/horizontal_crack_mask.png", image_shape
        )
        cls._save_crack_mask(
            diagonal_cracks, f"{output_folder}/diagonal_crack_mask.png", image_shape
        )

    @staticmethod
    def _save_crack_mask(coords_list, mask_path, image_shape):
        # Create an empty image with transparent background
        crack_mask = Image.new("RGBA", (image_shape[1], image_shape[0]), (0, 0, 0, 0))
        draw = ImageDraw.Draw(crack_mask)

        # Draw each pixel for the classified cracks
        for coord in coords_list:
            draw.point((coord[1], coord[0]), fill=(255, 0, 0, 255))  # (x, y)

        # Save the mask
        crack_mask.save(mask_path)
