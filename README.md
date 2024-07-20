## Installation
Open a terminal of your choice and create a virtual env as follows
```
python -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/env/Scripts/activate
pip install -r requirements.txt
```

## Training
train_dreambooth_stable_diffusion_XL.ipynb including fine tuning the stable 
diffusion XL model and inference process

train_dreambooth_lora_sdxl.py is the pretrained stable diffusion XL for the lora model

sd_dreambooth.ipynb is the training file for Stable Diffusion model, only for the midterm report

## Metrics
We use CLIP score and FID score to evaluate the model's performance.

CLIP.py calcuate the CLIP screo

FID.py calculate the FID score

## Data
The Home Depot datasets are not open to public

Public resources screw dataset:
https://gtvault-my.sharepoint.com/:f:/g/personal/jma416_gatech_edu/EoDiXB-YdJxLl1RCWVhTSB0Bm3yvXvKQwrNvL38R8bAAsg?e=3McPaN

Public resources kitchen cabinet dataset directory:
Data_kitchen_cabinet/Final Dataset

