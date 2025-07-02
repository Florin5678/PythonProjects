import torch # Runs the model
from transformers import BlipProcessor, BlipForConditionalGeneration # Image captioning model
from PIL import Image # To open images in Python

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption_image(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(**inputs)

    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption

def main():
    while True:
        print("\n🖼️ Image Caption Generator")
        img_path = input("Local image path: ").strip()

        if img_path.lower() == "exit":
            print("Goodbye! 👋")
            break

        try:
            caption = caption_image(img_path).capitalize()
            print(f"\nDescription: {caption}")
        except Exception as e:
            print(f"⚠️ Error: {e}\nPlease check the image path and try again.")


if __name__ == "__main__":
    main()