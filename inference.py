import openai
import numpy as np
from sewar.full_ref import mse
from PIL import Image
from datauri import DataURI

client = openai.OpenAI(base_url="http://localhost:9931/v1", api_key="no-key-required")


def get_desc():
    curr_snap_uri = str(DataURI.from_file('curr_snap.jpeg'))

    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "image_url", "image_url": { "url": curr_snap_uri } },
                    {"type": "text", "text": "Describe the current environment as captured in 3-4 sentences for a visually impaired person."},
                ]
            }
        ],
    )

    output = completion.choices[0].message.content
    return(output)

#get_desc()