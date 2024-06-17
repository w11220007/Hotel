from PIL import Image
import os

def resize_image(image_path, output_path, width):
    with Image.open(image_path) as img:
        height = int(img.height * (width / img.width))
        img = img.resize((width, height), resample=Image.LANCZOS)
        img.save(output_path)

current_directory = os.getcwd()

for filename in os.listdir(current_directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        input_path = os.path.join(current_directory, filename)
        output_path = os.path.join(current_directory, f"resized_{filename}")
        resize_image(input_path, output_path, 320)