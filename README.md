# Fine-Tuning Stable Diffusion XL for Stylistic Icon Generation
This repository contains the dataset, code and documentation for fine-tuning the Stable Diffusion XL model to generate stylistic icons, comparing different caption sizes. Our work builds on the Stable Diffusion model, incorporating enhancements and specialized training procedures.

The related paper can be found [here](https://arxiv.org/abs/2407.08513).
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

## Citation
If you find our work useful in your research, please consider citing:

@misc{
    sultan2024finetuningstablediffusionxl,

    title={Fine-Tuning Stable Diffusion XL for Stylistic Icon Generation: A Comparison of Caption Size},
    
    author={Youssef Sultan and Jiangqin Ma and Yu-Ying Liao},
    
    year={2024},
    
    eprint={2407.08513},
    
    archivePrefix={arXiv},
    
    primaryClass={cs.CV},
    
    url={https://arxiv.org/abs/2407.08513}
}

