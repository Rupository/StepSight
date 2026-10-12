from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers.image_utils import load_image
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-256M-Instruct")
model = AutoModelForImageTextToText.from_pretrained("HuggingFaceTB/SmolVLM-256M-Instruct",
                                                dtype=torch.bfloat16,
                                                _attn_implementation="flash_attention_2" if DEVICE == "cuda" else "eager").to(DEVICE)



def get_desc():
    prev_snap = load_image("prev_snap.jpeg")
    curr_snap = load_image("curr_snap.jpeg")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "The Previous Image:"},
                {"type": "image"},
                {"type": "text", "text": "The Current Image:"},
                {"type": "image"},
                {"type": "text", "text": "Describe the surroundings in the current image to a visually impaired person, "
                "in at most two sentences. If the images do not differ in terms of the environment, entities and events "
                "taking place, print the string: 'null'"},
            ] 
        },
    ]

    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[prev_snap, curr_snap], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    generated_ids = model.generate(**inputs, max_new_tokens=500)
    generated_texts = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        skip_prompt = True,
    )

    print(generated_texts[0])

    return generated_texts[0]


get_desc()