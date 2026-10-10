from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2"
).to("cuda")
