## Prerequisites

To use the OpenAI API, you need to:

1. Create an account at [OpenAI](https://openai.com/).
2. Set up billing and add credits to obtain your API key.

## Setting Up the OpenAI API Key

Once you have your API key, set it as an environment variable:

1. Open your terminal. Located directory Dalle.
2. Export your OpenAI API key using the following command:
```
export OPENAI_API_KEY="your_api_key_here"
```
Replace your_api_key_here with your actual API key.

## Generating Images

To generate images:
Ensure you have Python installed on your system.
Run the following command:
```
python dalle_api.py
```
This script generates images based on input text prompts using DALL-E.

### Additional Information

dalle_api.py: Generates images from text prompts.

img2img.py: Can edit images based on text prompts and input images. However, it's not recommended for icon editing in 
this project due to suboptimal results.