import os
import shutil
from PIL import Image
import imagehash


def get_image_hash(image_path):
    try:
        print(f"Processing image: {image_path}")
        image = Image.open(image_path)
        img_hash = imagehash.average_hash(image)
        print(f"Hash for {image_path}: {img_hash}")
        return img_hash
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def find_duplicates(image_folder, error_folder):
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
        print(f"Created error folder: {error_folder}")

    hashes = {}
    duplicates = []

    print(f"Scanning folder: {image_folder}")
    for root, dirs, files in os.walk(image_folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                img_hash = get_image_hash(file_path)
                if img_hash is None:
                    error_path = os.path.join(error_folder, os.path.basename(file_path))
                    shutil.move(file_path, error_path)
                    print(f"Moved {file_path} to error folder: {error_path}")
                else:
                    if img_hash in hashes:
                        duplicates.append(file_path)
                        print(f"Duplicate found: {file_path}")
                    else:
                        hashes[img_hash] = file_path

    return hashes.values(), duplicates


def save_unique_images(unique_images, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    for image_path in unique_images:
        shutil.copy(image_path, output_folder)
        print(f"Copied {image_path} to {output_folder}")


def main():
    input_folder = 'input'  # Change this to your input folder
    output_folder = 'output'  # Change this to your desired output folder
    error_folder = 'error'  # Change this to your error folder

    print("Starting duplicate image detection...")
    unique_images, duplicates = find_duplicates(input_folder, error_folder)

    print(f"Found {len(duplicates)} duplicates.")
    print(f"Saving {len(unique_images)} unique images to {output_folder}.")
    print(f"Moved images with errors to {error_folder}.")

    save_unique_images(unique_images, output_folder)
    print("Completed processing.")


if __name__ == '__main__':
    main()
