import os
import stat
import subprocess

TTS_file = os.path.expanduser("~/.tts")

if not os.path.exists(TTS_file):
    os.mkfifo(TTS_file)

subprocess.Popen(
    f'while true; do cat "{TTS_file}"; done | termux-tts-speak',
    shell=True
)

def take_snapshot():
    subprocess.run(['cp', 'curr_snap.jpeg', 'prev_snap.jpeg'])
    subprocess.run(['termux-camera-photo', '-c', '0', 'curr_snap.jpeg'])

def read_description(desc:str):
    with open(TTS_file, 'w') as f:
        f.write(desc + '\n')

read_description("Setting up speech engine.")