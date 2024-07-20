import os
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"

# load the model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


root_dir = "Data_Screw/home depot data/home depot_screw_short_prompt/CLIP"


clip_scores = []

# Iterate through each file in the root directory
for file in os.listdir(root_dir):
    file_path = os.path.join(root_dir, file)

    if file.endswith('.txt'):
       
        with open(file_path, "r") as text_file:
            text_prompt = text_file.read().strip()

      
        image_file_path = file_path.replace('.txt', '.png')

        if os.path.exists(image_file_path):
            print(f"Processing {image_file_path} with prompt from {file_path}")

            image = Image.open(image_file_path)
            inputs = processor(text=[text_prompt], images=image, return_tensors="pt", padding=True)
            
            inputs = {k: v.to(device) for k, v in inputs.items()}

  
            with torch.no_grad():
                outputs = model(**inputs)
            
            image_embeddings = outputs.image_embeds
            text_embeddings = outputs.text_embeds

            # calculate the cosine similarity between the image and text embeddings
            cosine_sim = torch.nn.functional.cosine_similarity(image_embeddings, text_embeddings)
            clip_score = cosine_sim.item()


            clip_scores.append(clip_score)

            print(f"CLIP Score for {image_file_path}: {clip_score}")
        else:
            print(f"Image file not found for text prompt: {file_path}")
    else:
        print(f"Skipping non-text file: {file_path}")

# calculate the average CLIP score
if clip_scores:
    average_clip_score = sum(clip_scores) / len(clip_scores)
    print(f"Average CLIP Score: {average_clip_score}")

    with open("CLIP_screw.txt", 'a') as f:
        f.write(f'\nAverage public data long prompt CLIP Score: {average_clip_score}\n')
else:
    print("No CLIP scores calculated.")
