import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import measure
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
        red_mask_np = np.array(red_mask)
        alpha_channel = red_mask_np[:, :, 3] 

        # Label connected components
        labeled_mask = label(alpha_channel)

        # Lists to hold coordinates for bounding boxes
        straight_line_cracks = []
        other_cracks = []

        # Classify and draw bounding boxes
        fig, ax = plt.subplots()
        ax.imshow(alpha_channel, cmap=plt.cm.gray)

        for region in measure.regionprops(labeled_mask):
            y0, x0, y1, x1 = region.bbox
            region_height = y1 - y0
            region_width = x1 - x0
            aspect_ratio = region_width / float(region_height)

            straight_line_threshold = 5 

            # Create bounding box patch
            rect = patches.Rectangle((x0, y0), region_width, region_height, 
                                    linewidth=1, edgecolor='none', facecolor='none')
            ax.add_patch(rect)

            if aspect_ratio >= straight_line_threshold or aspect_ratio <= 1/straight_line_threshold:
                straight_line_cracks.extend(region.coords)
                rect.set_edgecolor('red')
            else:
                other_cracks.extend(region.coords)
                rect.set_edgecolor('green')


            # Get the original image name from the path
    # image_name = os.path.basename(red_mask_image_path)

    # # Save the image with bounding boxes, including the original image name
    # plt.savefig(f"{output_folder}/cracks_with_bounding_boxes_{image_name}")  # Corrected line
    # plt.close(fig)

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Image shape needed for mask creation
        image_shape = alpha_channel.shape
        
        # Save the image with bounding boxes
        plt.savefig(f"{output_folder}/cracks_with_bounding_boxes.png")
        plt.close(fig)  # Close the plot to free up memory
        

        # Save masks for each type of crack
        cls._save_crack_mask(
            straight_line_cracks, f"{output_folder}/straight_line_crack_mask.png", image_shape
        )
        cls._save_crack_mask(
            other_cracks, f"{output_folder}/other_crack_mask.png", image_shape
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
