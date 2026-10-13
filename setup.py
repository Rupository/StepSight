import os
import time
import subprocess
import urllib.request

TTS_file = os.path.expanduser("~/.tts")

def initialize():
    subprocess.run(['pkill', '-f', 'termux-tts-speak'], capture_output=True)
    subprocess.run(['pkill', '-f', 'cat ~/.tts'], capture_output=True)
    time.sleep(0.5)

    if os.path.exists(TTS_file):
        os.remove(TTS_file)
    os.mkfifo(TTS_file)

    subprocess.Popen(
        f'while true; do cat "{TTS_file}"; done | termux-tts-speak',
        shell=True
    )

    subprocess.run(['pkill', '-f', 'llama serve'])
    time.sleep(1)

    subprocess.Popen(
        f'llama serve -m SmolVLM-256M-Instruct-q4_0.gguf --mmproj SmolVLM-256M-Instruct-q8_0.mmproj --threads 4 --image-max-tokens 1024 --port 9931',
        shell=True
    )
    while True:
        try:
            if urllib.request.urlopen(f'http://127.0.0.1:9931/health', timeout=1).status == 200:
                break
        except Exception:
            time.sleep(1)

    read_description("Setup Complete.")

def take_snapshot():
    subprocess.run(['cp', 'curr_snap.jpeg', 'prev_snap.jpeg'])
    subprocess.run(['termux-camera-photo', '-c', '0', 'curr_snap.jpeg'])
    print()
    print("Took snapshot.")

def read_description(desc:str):
    with open(TTS_file, 'w') as f:
        f.write(desc + '\n')
    print()
    print(desc)