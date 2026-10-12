import openai
from datauri import DataURI

client = openai.OpenAI(base_url="http://localhost:8080/v1", api_key="no-key-required")


def get_desc():
    prev_snap = str(DataURI.from_file('prev_snap.jpeg'))
    curr_snap = str(DataURI.from_file('curr_snap.jpeg'))

    completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": "This is the previous environment:" },
                    { "type": "image_url", "image_url": { "url": prev_snap } },
                    { "type": "text", "text": "This is the current environment:" },
                    { "type": "image_url", "image_url": { "url": curr_snap } },
                    {"type": "text", "text": "Describe the current environment in one sentence. If the current environment"
                    " is similar to the previous environment, DO NOT describe the current environment."},
                ]
            }
        ],
    )

    print()
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

#get_desc()