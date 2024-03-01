#!/home/roboticslab/Developer/image2overlays/.conda/bin/python
import os
import subprocess
import json

def get_geolocation_with_exiftool(image_path):
    command = ["exiftool", "-json", "-GPSLatitude", "-GPSLongitude", "-GPSAltitude", image_path]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = process.stdout

    try:
        data = json.loads(output)[0]
        return data.get('GPSLatitude'), data.get('GPSLongitude'), data.get('GPSAltitude')
    except json.JSONDecodeError:
        return None, None, None

def write_geolocation_with_exiftool(dest_image, latitude, longitude, altitude):
    command = [
        "exiftool",
        "-overwrite_original",  # Modify in-place
        f"-GPSLatitude={latitude}",
        f"-GPSLongitude={longitude}",
        f"-GPSAltitude={altitude}",
        dest_image
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def process_single_image(raw_image_path, mask_image_path):
    lat, lon, alt = get_geolocation_with_exiftool(raw_image_path)

    if lat and lon and alt:
        write_geolocation_with_exiftool(mask_image_path, lat, lon, alt)
        print(f"Geolocation information copied from {raw_image_path} to {mask_image_path}.")
    else:
        print("No geolocation information found in the source image.")
