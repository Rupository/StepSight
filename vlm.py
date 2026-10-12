from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

with open("vlm_prompt.md", "r") as file:
    vlm_prompt = file.read()

processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-500M-Instruct")
model = AutoModelForVision2Seq.from_pretrained("HuggingFaceTB/SmolVLM-500M-Instruct",
                                                torch_dtype=torch.bfloat16,
                                                _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager").to(DEVICE)

messages = [
    {
        "role": "system", 
        "content": vlm_prompt
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "This is the previous image"},
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"},
            {"type": "text", "text": "This is the current image."},
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/0052a70beed5bf71b92610a43a52df6d286cd5f3/diffusers/rabbit.jpg"},
        ] 
    },
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device, dtype=torch.bfloat16)

generated_ids = model.generate(**inputs, do_sample=False, max_new_tokens=64)
generated_texts = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)

print(generated_texts[0])
