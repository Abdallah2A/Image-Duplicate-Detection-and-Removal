import os
import imagehash
from PIL import Image
from multiprocessing import Pool, cpu_count, Manager
import time


def load_image(_image_path):
    try:
        _image = Image.open(_image_path)
        return _image
    except Exception as e:
        print(f"Error loading image at {_image_path}: {e}")
        return None


def calculate_hashes(_image_path):
    _image = load_image(_image_path)
    if _image is None:
        return None

    _phash = imagehash.phash(_image)
    _dhash = imagehash.dhash(_image)
    _whash = imagehash.whash(_image)
    _avhash = imagehash.average_hash(_image)

    return _image_path, [_phash, _dhash, _whash, _avhash]


def are_images_identical(_hash1, _hash2, _threshold=6):
    return abs(_hash1 - _hash2) <= _threshold


def check_duplicates(_image_data, _start, _end, _duplicated_list):
    for i in range(_start, _end):
        image1_path, hash1_values = _image_data[i]

        for j in range(i + 1, len(_image_data)):
            image2_path, hash2_values = _image_data[j]

            if any(are_images_identical(hash1_values[k], hash2_values[k]) for k in range(len(hash1_values))):
                _duplicated_list.append(image2_path)


def find_duplicates_in_range(_dataset_path):
    _dataset_path = _dataset_path.replace("\\", "/")
    _image_files = [os.path.join(_dataset_path, _image_name).replace("\\", "/") for _image_name in
                    os.listdir(_dataset_path) if os.path.isfile(os.path.join(_dataset_path, _image_name))]

    print("Starting calculate Images hashes")
    with Pool(processes=cpu_count()) as pool:
        _hash_results = pool.map(calculate_hashes, _image_files)

    _hash_results = [result for result in _hash_results if result is not None]

    print("Calculating Images hashes Finished")

    _manager = Manager()
    _duplicated_list = _manager.list()

    _chunk_size = len(_hash_results) // cpu_count() + 1
    _tasks = [(_hash_results, i * _chunk_size, min((i + 1) * _chunk_size, len(_hash_results)), _duplicated_list)
              for i in range(cpu_count())]

    print("Starting check for duplicated images")
    with Pool(processes=cpu_count()) as pool:
        pool.starmap(check_duplicates, _tasks)

    print("Checking for duplicated images finished")

    print("Starting removing duplicated images")
    for _image_path in _duplicated_list:
        if os.path.exists(_image_path):
            os.remove(_image_path)
            print(f"\r Image: {_image_path} removed", end="")

    print("\nRemoving duplicated images finished")


if __name__ == "__main__":
    old = time.time()
    dataset_path = "dataset/path"
    find_duplicates_in_range(dataset_path)
    new = time.time()

    print(f"Total time code take is: {new - old} sec")
