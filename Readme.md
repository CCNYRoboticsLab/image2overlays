# Image2Overlays

This project provides a set of scripts for processing images of concrete surfaces to identify and overlay damage types such as cracks, stains, and spalls.

## Requirements

* Python 3.6 or higher
* Conda environment named "visualinspection113" with the following packages installed:
    * numpy
    * opencv-python
    * scikit-image
    * laspy

## Usage

1. Clone the repository.

```bash
git clone https://github.com/roboticslab/image2overlays.git


2. Create a conda environment with the required packages.

3. Open "config.ini" and change image_path to the folder that you want to process.

4. Open "main.py" and adjust the comments and True or False values according to the needs.

5. You can also run an individual script like `python cracksegmentation.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/)