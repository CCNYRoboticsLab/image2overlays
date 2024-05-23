from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import measure
from skimage.measure import label, regionprops
from PIL import Image, ImageDraw
import os
import requests

class CrackClassifier:

    @classmethod
    def classify_and_save_cracks(cls, raw_image_path, red_mask_image_path, output_folder, api_endpoint="http://localhost:18000/classify"):
        raw_image = Image.open(raw_image_path)
        red_mask = Image.open(red_mask_image_path)
        red_mask_np = np.array(red_mask)
        alpha_channel = red_mask_np[:, :, 3]
        labeled_mask = label(alpha_channel)

        # Create output folders if they don't exist
        straight_folder = os.path.join(output_folder, "straight_joints")  # Update folder name to match API
        other_folder = os.path.join(output_folder, "other_cracks")
        os.makedirs(straight_folder, exist_ok=True)
        os.makedirs(other_folder, exist_ok=True)
        
        # Create an empty mask for other_cracks
        other_cracks_mask = np.zeros_like(alpha_channel)

        # Visualize (Optional)
        fig, ax = plt.subplots()
        ax.imshow(alpha_channel, cmap=plt.cm.gray)

        # Iterate over each region (crack)
        for i, region in enumerate(regionprops(labeled_mask)):
            y0, x0, y1, x1 = region.bbox
            crack_image = Image.fromarray(alpha_channel[y0:y1, x0:x1])  

            # Classify using the API
            # Convert PIL Image to bytes before sending to API
            with BytesIO() as image_bytes:
                crack_image.save(image_bytes, format='PNG')  # Save as PNG to bytes buffer
                image_bytes.seek(0)  # Reset file pointer to the beginning

                # Classify using the API
                try:
                    files = {'image': ('crack.png', image_bytes.read(), 'image/png')}  # File name, bytes, content type
                    response = requests.post(api_endpoint, files=files)
                    response.raise_for_status()
                    classification = response.json()
                    crack_type = classification["class"]
                    confidence = classification["confidence"]
                except requests.exceptions.RequestException as e:
                    print(f"Error classifying crack_{i}: {e}")
                    continue  # Skip this crack if there's an API error

            # Save based on classification
            output_path = os.path.join(straight_folder if crack_type == "straight joints" else other_folder, f"crack_{i}.png")
            crack_image.save(output_path)

            # Visualize (Optional)
            rect = patches.Rectangle((x0, y0), x1-x0, y1-y0, linewidth=1, 
                                    edgecolor='red' if crack_type == "straight joints" else 'green', facecolor='none')
            ax.add_patch(rect)
            # Dynamic text color based on background
            background_region = alpha_channel[max(y0-10, 0):min(y1+10, alpha_channel.shape[0]), 
                                            max(x0-10, 0):min(x1+10, alpha_channel.shape[1])]
            avg_intensity = np.mean(background_region)
            text_color = 'white' if avg_intensity < 128 else 'black'  # Choose color based on average intensity
            ax.text(x0, y0 - 5, f"{confidence:.1f}", color=text_color, alpha=0.5)  # Set alpha for transparency (0 to 1)
            
            # print(f"Crack {i} classified as {crack_type} with confidence {confidence:.1f}")
            if crack_type == "other cracks":
                # print("Found other crack:", i)  # Print if an "other_cracks" is detected
                other_cracks_mask[y0:y1, x0:x1] = 255

        # Save overall image with bounding boxes (Optional)
        plt.savefig(f"{output_folder}/all_cracks_with_bounding_boxes.png")
        plt.close(fig) 
        
        # Create the filteredRaw image
        filtered_raw = Image.new("RGBA", raw_image.size)
        filtered_raw.paste(raw_image)
        filtered_raw.save(os.path.join(output_folder, "filtered_raw_image_only.png"))  # Raw image without mask
        
        red_mask.save(os.path.join(output_folder, "red_mask.png"))  # Save the red mask

        # Create and SAVE the filtered raw mask for debugging
        # print(np.unique(other_cracks_mask))  # Should print [0 255] if "other_cracks" exist
        filtered_raw_mask = Image.fromarray(other_cracks_mask)  # Don't need to scale here
        filtered_raw_mask.save(os.path.join(output_folder, "mask_filter.png")) 
        
                # Convert red_mask and other_cracks_mask to boolean (True for white, False for black)
        red_mask_bool = red_mask_np[:, :, 3] > 0
        other_cracks_mask_bool = other_cracks_mask > 0
        
        # Create filtered_mask using logical AND
        filtered_mask = np.zeros_like(red_mask_np, dtype=np.uint8)  # Empty RGBA image
        filtered_mask[other_cracks_mask_bool & red_mask_bool] = red_mask_np[other_cracks_mask_bool & red_mask_bool]

        # Save the filtered_mask as an image
        filtered_mask_img = Image.fromarray(filtered_mask)
        filtered_mask_img.save(os.path.join(output_folder, "filtered_mask.png"))
        

        # Paste the filtered raw mask onto the raw image
        filtered_raw.paste(filtered_mask_img, (0, 0), filtered_mask_img)  
        filtered_raw.save(os.path.join(output_folder, "filtered_overlay.png"))
        
        # Create solid_filtered_overlay
        solid_filtered_overlay = Image.new("RGBA", raw_image.size)
        solid_filtered_overlay.paste(raw_image)

        solid_mask = Image.new("RGBA", filtered_mask_img.size, (255, 0, 0, 255))  # Solid red color
        solid_filtered_overlay.paste(solid_mask, (0, 0), filtered_mask_img)  # Use filtered_mask_img as the mask
        
        solid_filtered_overlay.save(os.path.join(output_folder, "solid_filtered_overlay.png"))
        
        filtered_raw = Image.new("RGBA", raw_image.size)
        filtered_raw.paste(raw_image)

        # Paste the unfiltered raw mask onto the raw image
        filtered_raw.paste(red_mask, (0, 0), red_mask)  
        filtered_raw.save(os.path.join(output_folder, "unfiltered_overlay.png"))



# Example Usage: (Remember to replace with your actual paths)
# red_mask_image_path = "path/to/your/red_mask.png" 
# output_folder = "crack_results"
# crack_classifier = CrackClassifier()
# crack_classifier.classify_and_save_cracks(red_mask_image_path, output_folder)
