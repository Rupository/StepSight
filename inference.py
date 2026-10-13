import openai
import numpy as np
from sewar.full_ref import ssim
from PIL import Image
from datauri import DataURI

client = openai.OpenAI(base_url="http://localhost:9931/v1", api_key="no-key-required")


def get_desc():
    curr_snap_uri = str(DataURI.from_file('curr_snap.jpeg'))
    curr_snap = np.asarray(Image.open("curr_snap.jpeg"))
    prev_snap = np.asarray(Image.open("prev_snap.jpeg"))

    if ssim(curr_snap, prev_snap)[0] < 0.85:

        completion = client.chat.completions.create(
            model="local-model",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "image_url", "image_url": { "url": curr_snap_uri } },
                        {"type": "text", "text": "Describe the current environment in one sentence."},
                    ]
                }
            ],
        )

        output = completion.choices[0].message.content

    else:
        output = "No changes detected."

    print(output)
    return(output)

#get_desc()