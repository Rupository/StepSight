from transformers import AutoProcessor, AutoModelForImageTextToText
from transformers.image_utils import load_image
import torch

DEVICE = "cpu"

model_name = "HuggingFaceTB/SmolVLM-256M-Instruct"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForImageTextToText.from_pretrained(model_name,
                                                dtype=torch.float32,
                                                #low_cpu_mem_usage=True,
                                                _attn_implementation="eager").to(DEVICE)



def get_desc():
    prev_snap = load_image("prev_snap.jpeg")
    curr_snap = load_image("curr_snap.jpeg")

    print('Snapshots loaded')

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "This image shows the previous environment the user was in."},
                {"type": "image"},
                {"type": "text", "text": "This image shows the current environment the user is in."},
                {"type": "image"},
                {"type": "text", "text": "Describe the current environment in one sentence. "
                "If the current environment is similar to the previous environment, DO NOT describe the current environment."},
            ] 
        },
    ]

    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[prev_snap, curr_snap], return_tensors="pt")
    inputs = inputs.to(DEVICE)

    print("Inputs passed")

    generated_ids = model.generate(**inputs, max_new_tokens=64)
    generated_texts = processor.batch_decode(
        generated_ids,
        #skip_special_tokens=True,
    )

    
    delimeter = '<end_of_utterance>\nAssistant:'
    full_output = str(generated_texts[0]).partition(delimeter)[2]

    output = full_output[:len(full_output) - len('<end_of_utterance>')]

    print()
    print(output)
    return output

#get_desc()