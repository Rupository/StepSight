import os
import stat
import subprocess

TTS_file = os.path.expanduser("~/.tts")

if not os.path.exists(TTS_file):
    os.mkfifo(TTS_file)
elif not stat.S_ISFIFO(os.stat(TTS_file).st_mode):
    raise RuntimeError(f"{TTS_file} exists but is not a FIFO")

subprocess.Popen(
    f'while true; do cat "{TTS_file}"; done | termux-tts-speak',
    shell=True
)

def take_snapshot():
    subprocess.run(['cp', '/StepSight/curr_snap.jpeg', '/StepSight/prev_snap.jpeg'])
    subprocess.run(['termux-camera-photo', '-c', '0', '/StepSight/curr_snap.jpeg'])

def read_description(desc:str):
    with open(TTS_file, 'w') as f:
        f.write(desc + '\n')

read_description("Setting up speech engine.")