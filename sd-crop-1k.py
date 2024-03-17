"""
The script crops an image to pieces of 1024x1024px (with overlap) for training with Stable Diffusion XL.
"""

from PIL import Image
import os
import math

def calculate_crops_and_overlap(image_size, crop_size=1024):
    """
    Calculate the number of crops needed and the necessary overlap for each dimension of the image.
    Ensures full coverage of the image with a combination of overlaps and crop counts.
    """
    total_crops = math.ceil(image_size / crop_size)
    if total_crops == 1 or image_size % crop_size == 0:
        overlap_per_crop = 0
    else:
        extra_space = crop_size * total_crops - image_size
        overlap_per_crop = math.ceil(extra_space / (total_crops - 1))
    return total_crops, overlap_per_crop

def resize_image_if_needed(image, short_side_min=1024, short_side_max=1100):
    """
    Resizes the image so that its shortest side is 1024 pixels if it was originally between 1024 and 1100 pixels.
    Preserves the aspect ratio of the image.
    """
    width, height = image.size
    short_side = min(width, height)
    if short_side < short_side_max:
        ratio = short_side_min / short_side
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return image

def convert_to_rgb(image):
    """
    Converts an RGBA image to RGB by discarding the alpha channel.
    This is necessary because certain image saving formats do not support transparency.
    """
    if image.mode == 'RGBA':
        return image.convert('RGB')
    return image

def crop_image(input_path, output_dir, crop_size=1024):
    """
    Crops the given image into 1024x1024 segments, calculating necessary overlaps for full coverage.
    Resizes images and converts them to RGB when necessary. Saves the crops in the specified output directory.
    Pads the last crop with black if it doesn't fit perfectly.
    """
    img = Image.open(input_path)
    img = resize_image_if_needed(img)
    img = convert_to_rgb(img)
    width, height = img.size
    
    total_crops_w, overlap_w = calculate_crops_and_overlap(width, crop_size)
    total_crops_h, overlap_h = calculate_crops_and_overlap(height, crop_size)

    for i in range(total_crops_w):
        for j in range(total_crops_h):
            left = max(0, i * crop_size - i * overlap_w)
            upper = max(0, j * crop_size - j * overlap_h)
            right = min(width, left + crop_size)
            lower = min(height, upper + crop_size)

            if right - left < crop_size or lower - upper < crop_size: 
                crop_img = Image.new("RGB", (crop_size, crop_size), (0, 0, 0))
                original_crop = img.crop((left, upper, right, lower))
                crop_img.paste(original_crop, (0, 0))
            else:
                crop_img = img.crop((left, upper, right, lower))

            crop_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}_crop_{i}_{j}.png")
            crop_img.save(crop_path)

def process_directory(input_dir, output_dir):
    """
    Processes all images in the given input directory, applying cropping and saving the results in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    for image_name in os.listdir(input_dir):
        image_path = os.path.join(input_dir, image_name)
        if os.path.isfile(image_path):
            crop_image(image_path, output_dir)

# Adjust these directory paths as needed
input_dir = 'input_images_crop'
output_dir = 'output_crop'

process_directory(input_dir, output_dir)
