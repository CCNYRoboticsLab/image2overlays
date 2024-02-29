import unittest
import subprocess
import json
import os
from copy_geo_exiftool import process_single_image

class TestImageProcessing(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Backup the original mask image
        cls.test_raw_image_path = 'TestImages/raw/S1078749.JPG'
        cls.test_mask_image_path = 'TestImages/S1078749.JPG'
        cls.backup_mask_image_path = f"{cls.test_mask_image_path}_original"
        if not os.path.exists(cls.backup_mask_image_path):
            os.rename(cls.test_mask_image_path, cls.backup_mask_image_path)
    
    def get_geolocation_with_exiftool(self, image_path):
        # Run exiftool and parse latitude, longitude, and altitude
        command = ["exiftool", "-json", "-GPSLatitude", "-GPSLongitude", "-GPSAltitude", image_path]
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = process.stdout
        data = json.loads(output)[0]
        return data.get('GPSLatitude'), data.get('GPSLongitude'), data.get('GPSAltitude')
    
    def test_process_single_image(self):
        # Call the function with the test paths
        process_single_image(self.test_raw_image_path, self.test_mask_image_path)
        
        # Get the geolocation data from the mask image after processing
        lat, lon, alt = self.get_geolocation_with_exiftool(self.test_mask_image_path)
        
        # Assert that the geolocation data is not None (indicating that it's been written)
        self.assertIsNotNone(lat, "Latitude was not written to the mask image")
        self.assertIsNotNone(lon, "Longitude was not written to the mask image")
        self.assertIsNotNone(alt, "Altitude was not written to the mask image")
        
        # Additional assertions can be added to compare with expected values
        # For example:
        # self.assertEqual(lat, expected_lat)
        # self.assertEqual(lon, expected_lon)
        # self.assertEqual(alt, expected_alt)

    @classmethod
    def tearDownClass(cls):
        # Rename the processed mask image for inspection instead of deleting
        if os.path.exists(cls.test_mask_image_path):
            processed_mask_image_path = cls.test_mask_image_path.replace('.JPG', '_processed.JPG')
            os.rename(cls.test_mask_image_path, processed_mask_image_path)
            print(f"Processed image available at: {processed_mask_image_path}")

        # Restore the original state of the mask image from the backup
        if os.path.exists(cls.backup_mask_image_path):
            os.rename(cls.backup_mask_image_path, cls.test_mask_image_path)

if __name__ == '__main__':
    unittest.main()
