import openai
from PIL import Image
from datauri import DataURI
from ssim import compute_ssim

client = openai.OpenAI(base_url="http://localhost:9931/v1", api_key="no-key-required")


def get_desc():
    curr_snap_uri = str(DataURI.from_file('curr_snap.jpeg'))
    curr_snap_img = Image.open('curr_snap.jpeg')
    prev_snap_img = Image.open('prev_snap.jpeg')

    ssim_score = compute_ssim(curr_snap_img, prev_snap_img)

    if ssim_score < 0.5:

        completion = client.chat.completions.create(
            model="local-model",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "image_url", "image_url": { "url": curr_snap_uri } },
                        {"type": "text", "text": "In one short sentence, describe the environment captured in the image."},
                    ]
                }
            ],
            temperature = 0,
        )

        output = completion.choices[0].message.content

    else:
        output = "No changes observed."

    return(output)