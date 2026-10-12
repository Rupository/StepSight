import os
import time
import subprocess

TTS_file = os.path.expanduser("~/.tts")

def initialize():
    if not os.path.exists(TTS_file):
        os.mkfifo(TTS_file)

    subprocess.Popen(
        f'while true; do cat "{TTS_file}"; done | termux-tts-speak',
        shell=True
    )

    subprocess.Popen(
        f'llama serve -hf ggml-org/SmolVLM-256M-Instruct-GGUF --threads 4 --port 9931',
        shell=True
    )
    time.sleep(30)

    read_description("Setup Complete.")

def take_snapshot():
    subprocess.run(['cp', 'curr_snap.jpeg', 'prev_snap.jpeg'])
    subprocess.run(['termux-camera-photo', '-c', '0', 'curr_snap.jpeg'])
    print()
    print("Took snapshot.")

def read_description(desc:str):
    with open(TTS_file, 'w') as f:
        f.write(desc + '\n')
    print
    print(desc)