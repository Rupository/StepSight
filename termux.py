import os
import subprocess

TTS_file = "~/.tts"

def setup_TTS():
  if not os.path.exists(TTS_file):
    os.mkfifo(path=TTS_file)
  subprocess.run(['while true; do cat ~/.tts; done | termux-tts-speak', 'echo "Setting up speech engine." > /.tts'], shell=True)

def take_snapshot():
  pass

def read_description(desc:str):
  subprocess.run([f'echo {desc} > ~/.tts'], shell=True)
