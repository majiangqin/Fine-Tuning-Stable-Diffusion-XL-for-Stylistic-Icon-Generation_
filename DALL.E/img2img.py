from PIL import Image
import requests
from IPython.display import display, Image as IPImage
import os
from io import BytesIO
# API Key and headers configuration
OPENAI_API_KEY = "<your-key-value-here>"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}
def convert_image_format(image_path, output_format='RGBA'):
    """ Convert image to a specified format and overwrite the original image. """
    with Image.open(image_path) as img:
        rgba_image = img.convert(output_format)
        rgba_image.save(image_path)  # overwrite the original image


def resize_and_compress_image(input_path, output_path, target_size=(1024, 1024), max_size=4000000):
    """ Resize and compress an image while keeping its size below a maximum and ensuring specific dimensions. """
    with Image.open(input_path) as img:
        img = img.convert('RGBA')  # ensure the image is in RGBA format
        img.thumbnail(target_size, Image.LANCZOS)  # Resize the image
        img.save(output_path, 'PNG', optimize=True)

        while os.path.getsize(output_path) > max_size:
            img = Image.open(output_path)
            current_size = os.path.getsize(output_path)
            width, height = img.size
            factor = (max_size / current_size) ** 0.5  # Reduce dimensions by the square root of the ratio
            new_dimensions = (int(width * factor), int(height * factor))
            img = img.resize(new_dimensions, Image.LANCZOS)
            img.save(output_path, 'PNG', optimize=True)

        return output_path


def ensure_same_size(image_path, mask_path, output_image_path, output_mask_path):
    """ Ensure both image and mask are the same size and meet requirements. """
    with Image.open(image_path) as img, Image.open(mask_path) as mask:
        if img.size != mask.size:
            new_size = min(img.size, mask.size)
            img = img.resize(new_size, Image.LANCZOS)
            mask = mask.resize(new_size, Image.LANCZOS)
        img.save(output_image_path, 'PNG', optimize=True)
        mask.save(output_mask_path, 'PNG', optimize=True)


# Image and mask paths
original_image_path = "teks-self-drilling-screws-21340-e1_145.png"
mask_image_path = "hardware-fasteners-screws-562860-head-style-587571-truss-head-4295189302-v1.png"
processed_image_path = "processed_image.png"
processed_mask_path = "processed_mask.png"

# Process images
convert_image_format(original_image_path)
convert_image_format(mask_image_path)
resize_and_compress_image(original_image_path, processed_image_path)
resize_and_compress_image(mask_image_path, processed_mask_path)
ensure_same_size(processed_image_path, processed_mask_path, processed_image_path, processed_mask_path)

# API data and file configuration
data = {
    "prompt": "icon of External Hex Flange Hex-Head Self-Drilling Screws with a plain white background.",
    "n": 1,
    "size": "512x512"
}
files = {
    "image": open(processed_image_path, "rb"),
    "mask": open(processed_mask_path, "rb")
}

# Send request to OpenAI API
response = requests.post(
    "https://api.openai.com/v1/images/edits",
    headers=headers,
    files=files,
    data=data
)

# Handle the response from the API
if response.status_code == 200:
    image_data = response.json()['data'][0]
    image_url = image_data['url']


    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        # Load image from the response
        img = Image.open(BytesIO(image_response.content))

        img.show()


        img.save("output_image.png")
        print("Image has been saved to 'output_image.png'.")

    else:
        print("Failed to download the image from the URL provided.")
else:
    print("Failed to generate image:", response.text)