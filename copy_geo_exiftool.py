#!/home/roboticslab/Developer/image2overlays/.conda/bin/python
import os
import subprocess
import json

def get_geolocation_with_exiftool(image_path):
    command = ["exiftool", "-json", "-GPSLatitude", "-GPSLongitude", "-GPSAltitude", "-GPSLatitudeRef", "-GPSLongitudeRef", image_path]  # Added reference tags
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = process.stdout

    try:
        data = json.loads(output)[0]
        return (
            data.get('GPSLatitude'), 
            data.get('GPSLongitude'), 
            data.get('GPSAltitude'),
            data.get('GPSLatitudeRef'),   # Extract references
            data.get('GPSLongitudeRef')
        )
    except json.JSONDecodeError:
        return None, None, None, None, None  # Return None for all values if there's an error

def write_geolocation_with_exiftool(dest_image, latitude, longitude, altitude, GPSLatitudeRef, GPSLongitudeRef):
    command = [
        "exiftool",
        "-overwrite_original",  
        f"-GPSLatitude={latitude}",
        f"-GPSLongitude={longitude}",
        f"-GPSAltitude={altitude}",
        f"-GPSLatitudeRef={GPSLatitudeRef}",  # Added
        f"-GPSLongitudeRef={GPSLongitudeRef}",  # Added
        dest_image
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def process_single_image(raw_image_path, mask_image_path):
    lat, lon, alt, lat_ref, lon_ref = get_geolocation_with_exiftool(raw_image_path)  # Get references

    if lat and lon and alt:
        write_geolocation_with_exiftool(mask_image_path, lat, lon, alt, lat_ref, lon_ref)  # Pass references
        print(f"Geolocation information copied from {raw_image_path} to {mask_image_path}.")
    else:
        print("No geolocation information found in the source image.")
