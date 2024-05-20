import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import measure
from skimage.measure import label, regionprops
from PIL import Image, ImageDraw
import os


class CrackClassifier:

    @classmethod
    def classify_and_save_cracks(cls, red_mask_image_path, output_folder):
        red_mask = Image.open(red_mask_image_path)
        red_mask_np = np.array(red_mask)
        alpha_channel = red_mask_np[:, :, 3]
        labeled_mask = label(alpha_channel)

        straight_line_threshold = 5  

        # Create output folders if they don't exist
        straight_folder = os.path.join(output_folder, "straight_cracks")
        other_folder = os.path.join(output_folder, "other_cracks")
        os.makedirs(straight_folder, exist_ok=True)
        os.makedirs(other_folder, exist_ok=True)

        # Visualize (Optional)
        fig, ax = plt.subplots()
        ax.imshow(alpha_channel, cmap=plt.cm.gray)

        # Iterate over each region (crack)
        for i, region in enumerate(regionprops(labeled_mask)):
            y0, x0, y1, x1 = region.bbox
            region_height = y1 - y0
            region_width = x1 - x0
            aspect_ratio = region_width / float(region_height)

            # Determine crack type and save
            crack_type = "straight" if aspect_ratio >= straight_line_threshold or aspect_ratio <= 1/straight_line_threshold else "other"
            output_path = os.path.join(straight_folder if crack_type == "straight" else other_folder, f"crack_{i}.png")

            # Crop and save the crack region
            crack_image = Image.fromarray(alpha_channel[y0:y1, x0:x1])  
            crack_image.save(output_path)

            # Visualize (Optional)
            rect = patches.Rectangle((x0, y0), region_width, region_height, linewidth=1, edgecolor='red' if crack_type == "straight" else 'green', facecolor='none')
            ax.add_patch(rect)

        # Save overall image with bounding boxes (Optional)
        plt.savefig(f"{output_folder}/all_cracks_with_bounding_boxes.png")
        plt.close(fig)  # Close the plot to free up memory

# Example Usage:
# crack_classifier = CrackClassifier()
# red_mask_image_path = "path/to/your/red_mask.png" 
# output_folder = "crack_results"
# crack_classifier.classify_and_save_cracks(red_mask_image_path, output_folder)
