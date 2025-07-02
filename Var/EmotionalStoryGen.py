# Wholesome AI Caption Generator - Full Code

import gradio as gr
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from PIL import Image
import torch

# Load BLIP model for image captioning
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load GPT-2 model for rewriting captions into wholesome stories
text_gen = pipeline("text-generation", model="gpt2-large")

def generate_wholesome_caption(image):
    # Step 1: Generate base caption from the uploaded image
    inputs = caption_processor(image, return_tensors="pt")
    out = caption_model.generate(**inputs)
    base_caption = caption_processor.decode(out[0], skip_special_tokens=True)

    # Step 2: Rewrite it into a wholesome story
    prompt = (
        f"Generate a deeply emotional, tear-jerking caption for a picture of a {base_caption}:"
    )
    result = text_gen(prompt, max_length=100, do_sample=True, temperature=0.95)[0]['generated_text']

    return result.strip()

# Create Gradio interface
iface = gr.Interface(
    fn=generate_wholesome_caption,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Wholesome AI Caption Generator 🌸",
    description="Upload an image and let AI write an emotional story about it!"
)

# Launch the web app
iface.launch()