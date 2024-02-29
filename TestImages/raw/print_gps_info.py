#!/home/roboticslab/Developer/image2overlays/.conda/bin/python
from PIL import Image
import piexif

# Load the image from file path
jpg_image_path = '/home/roboticslab/Developer/image2overlays/TestImages/raw/S1078749.JPG'

# Open the image using PIL
jpg_image = Image.open(jpg_image_path)

# Extract EXIF data
exif_data = piexif.load(jpg_image.info['exif'])

# GPS information is in the 'GPSInfo' field of the EXIF data
gps_info = exif_data.get('GPSInfo')

# Define a helper function to convert GPS coordinates to a human-readable format
def convert_to_degrees(value):
    """Convert GPS coordinates stored in the EXIF to degrees"""
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

# Check if GPSInfo tag is present
if gps_info:
    # Extract latitude and longitude in EXIF's specific format
    latitude = gps_info.get(2)
    longitude = gps_info.get(4)
    
    # Convert latitude and longitude to degrees if they are present
    if latitude and longitude:
        lat_degrees = convert_to_degrees(latitude)
        long_degrees = convert_to_degrees(longitude)
        
        # Determine the sign based on the reference value
        lat_ref = gps_info.get(1)
        long_ref = gps_info.get(3)
        
        if lat_ref == 'S':
            lat_degrees = -lat_degrees
        if long_ref == 'W':
            long_degrees = -long_degrees
        
        # Print out the geolocation information
        geolocation = {
            'Latitude': lat_degrees,
            'Longitude': long_degrees
        }
else:
    geolocation = "No geolocation information found."

print(geolocation)
