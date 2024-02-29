#!/home/roboticslab/Developer/image2overlays/.conda/bin/python
from copy_geo_exiftool import process_single_image

# Example usage of the process_single_image function
if __name__ == '__main__':
    raw_image_path = '/home/roboticslab/Developer/image2overlays/TestImages/raw/S1078749.JPG'
    mask_image_path = '/home/roboticslab/Developer/image2overlays/TestImages/S1078749.JPG'
    
    process_single_image(raw_image_path, mask_image_path)
