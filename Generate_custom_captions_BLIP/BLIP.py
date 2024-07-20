# Generate custom captions with BLIP
# Load BLIP to auto caption the images

import requests
from transformers import AutoProcessor, BlipForConditionalGeneration
import torch
import json
import glob
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

# load the processor and the captioning model
blip_processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base",torch_dtype=torch.float16).to(device)

# captioning utility
def caption_images(input_image):
    inputs = blip_processor(images=input_image, return_tensors="pt").to(device, torch.float16)
    pixel_values = inputs.pixel_values

    generated_ids = blip_model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = blip_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_caption

# Define the directory containing images
local_dir = "original data_screw/"

# Create a list of (path, PIL.Image) pairs
imgs_and_paths = [(path, Image.open(path)) for path in glob.glob(f"{local_dir}*.png")]

print(imgs_and_paths)

# Prefix for captions
caption_prefix = "a photo of TOK screw icon, "

# Specify the directory where the output file will be saved
output_dir = "original data_screw/"

# Create and write to the metadata.jsonl file
with open(f'{output_dir}metadata.jsonl', 'w') as outfile:
    for img in imgs_and_paths:
        caption = caption_prefix + caption_images(img[1]).split("\n")[0]
        entry = {"file_name": img[0].split("/")[-1], "prompt": caption}
        json.dump(entry, outfile)
        outfile.write('\n')

print(f'Metadata written to {output_dir}metadata.jsonl')