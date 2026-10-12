from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers.image_utils import load_image
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

with open("vlm_prompt.md", "r") as file:
    vlm_prompt = file.read()

processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-500M-Instruct")
model = AutoModelForImageTextToText.from_pretrained("HuggingFaceTB/SmolVLM-500M-Instruct",
                                                torch_dtype=torch.bfloat16,
                                                _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager").to(DEVICE)


image1 = load_image("https://huggingface.co/spaces/HuggingFaceTB/SmolVLM/resolve/main/example_images/rococo.jpg")
image2 = load_image("https://huggingface.co/spaces/HuggingFaceTB/SmolVLM/resolve/main/example_images/rococo_1.jpg")

messages = [
    {
        "role": "system", 
        "content": vlm_prompt
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "The Previous Image:"},
            {"type": "image"},
            {"type": "text", "text": "The Current Image:"},
            {"type": "image"},
        ] 
    },
]

prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[image1, image2], return_tensors="pt")
inputs = inputs.to(DEVICE)

generated_ids = model.generate(**inputs, max_new_tokens=500)
generated_texts = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)

print(generated_texts[0])
