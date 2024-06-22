# Image Duplicate Detection and Removal
This script detects duplicate images within a specified directory using image hashing techniques and removes them from the filesystem.

## Description
The Image Duplicate Detection and Removal script leverages image hashing algorithms (phash, dhash, whash, average_hash) to compute unique hashes for each image. It then compares these hashes to identify duplicate images based on a configurable threshold. Detected duplicates are subsequently removed from the specified directory.

## Features
- Efficiently identifies duplicate images using multiprocessing for parallel processing.

- Utilizes image hashing algorithms to generate unique identifiers for images.

- Removes detected duplicate images from the filesystem.


## Installation
Clone the repository to your local machine:

```bash
git clone https://github.com/Abdallah2A/Image-Duplicate-Detection-and-Removal.git
```

## Install the required dependencies:
```bash
pip install Pillow imagehash
```

## How to Use
- Update the dataset_path variable in the script to point to your target directory containing images.

- Adjust the _threshold value in are_images_identical function as per your requirement to control the sensitivity of duplicate detection.

## Run the script:

```bash
python image_duplicate_removal.py
```

Monitor the script's output to track the progress of image hashing, duplicate detection, and removal.

The script will print the total execution time upon completion.

## Requirements
- Python 3.x

- Pillow

- imagehash

- multiprocessing
