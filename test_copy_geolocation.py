import unittest
import tempfile
import os
import shutil
from PIL import Image
import piexif
from copy_geolocation import (
    main,
)  # Assume your script is refactored to have a main function


class TestGeolocationCopying(unittest.TestCase):
    def setUp(self):
        # Create temporary directories
        self.raw_dir = tempfile.mkdtemp()
        self.mask_dir = tempfile.mkdtemp()

        # Create a dummy raw image with EXIF geolocation data
        raw_image_path = os.path.join(self.raw_dir, "raw_image.jpg")
        mask_image_path = os.path.join(self.mask_dir, "mask_image.jpg")

        # Dummy image creation
        Image.new("RGB", (100, 100)).save(raw_image_path)
        Image.new("RGB", (100, 100)).save(mask_image_path)

        # Add dummy EXIF data to raw image
        # Add dummy EXIF data to raw image
        exif_dict = {
            "GPS": {
                piexif.GPSIFD.GPSLatitudeRef: "N",
                piexif.GPSIFD.GPSLatitude: ((10, 1), (0, 1), (0, 1)),
                piexif.GPSIFD.GPSLongitudeRef: "E",
                piexif.GPSIFD.GPSLongitude: ((20, 1), (0, 1), (0, 1)),
            }
        }

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, raw_image_path)

    def test_geolocation_copy(self):
        # Run the script
        main(self.raw_dir, self.mask_dir)

        # Verify EXIF data is copied to mask image
        mask_image_path = os.path.join(self.mask_dir, "mask_image.jpg")
        exif_data = piexif.load(mask_image_path)

        self.assertIn("GPS", exif_data)
        self.assertEqual(exif_data["GPS"][piexif.GPSIFD.GPSLatitudeRef], b"N")
        self.assertEqual(
            exif_data["GPS"][piexif.GPSIFD.GPSLatitude], ((10, 1), (0, 1), (0, 1))
        )
        self.assertEqual(exif_data["GPS"][piexif.GPSIFD.GPSLongitudeRef], b"E")
        self.assertEqual(
            exif_data["GPS"][piexif.GPSIFD.GPSLongitude], ((20, 1), (0, 1), (0, 1))
        )

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.raw_dir)
        shutil.rmtree(self.mask_dir)


if __name__ == "__main__":
    unittest.main()
