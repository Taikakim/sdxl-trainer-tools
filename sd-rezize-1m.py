from PIL import Image

import os

import math



def resize_and_pad(image_path, output_dir, target_area=1048576, divisor=64):

    # Ensure the output directory exists

    os.makedirs(output_dir, exist_ok=True)

    # Load the image

    img = Image.open(image_path)

    original_width, original_height = img.size

    original_area = original_width * original_height

    

    # Calculate the resize ratio to reach the target area, while keeping aspect ratio

    resize_ratio = math.sqrt(target_area / original_area)

    new_width = round(original_width * resize_ratio)

    new_height = round(original_height * resize_ratio)

    

    # Adjust width and height to be divisible by the divisor (64 in this case)

    new_width += (divisor - new_width % divisor) % divisor

    new_height += (divisor - new_height % divisor) % divisor

    

    # Ensure the final area does not exceed the target area significantly by reducing dimensions if necessary

    while new_width * new_height > target_area:

        new_width -= divisor

        new_height -= divisor



    # Resize the image

    resized_image = img.resize((new_width, new_height), Image.LANCZOS)

    

    # Finally, create an output image with the adjusted size and pad it if necessary

    output_img = Image.new("RGB", (new_width, new_height), (0, 0, 0))
    output_img.paste(resized_image, (0, 0))



    # Save the processed image

    #filename = os.path.basename(image_path) # keep original filename 
    
    filename = os.path.splitext(os.path.basename(image_path))[0] + '.jpeg'

    output_path = os.path.join(output_dir, filename)

    # output_img.save(output_path) # save in original format
    output_img.save(output_path, 'JPEG', optimize=True, quality=95)



# Example usage

# Assuming we have a directory 'input_images' with images to be processed

input_dir = 'input_images'

output_dir = 'output'



for image_name in os.listdir(input_dir):

    image_path = os.path.join(input_dir, image_name)

    if os.path.isfile(image_path):

        resize_and_pad(image_path, output_dir)
