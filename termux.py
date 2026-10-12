import os
import subprocess

TTS_file = "~/.tts"

if not os.path.exists(TTS_file):
  os.mkfifo(path=TTS_file)
subprocess.run(['while true; do cat ~/.tts; done | termux-tts-speak', 'echo "Setting up speech engine." > /.tts'], shell=True)

def take_snapshot():
  subprocess.run(['cp /StepSight/curr_snap.jpeg /StepSight/prev_snap.jpeg', f'termux-camera-photo -c 0 /StepSight/curr_snap.jpeg'], shell=True)

def read_description(desc:str):
  subprocess.run([f'echo {desc} > ~/.tts'], shell=True)
