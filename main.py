
# Import libraries

#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import pyttsx3
import json
from core import SystemInfo

# Speech Synthesis
engine = pyttsx3.init()

def speak(text): 
    engine.say(text)
    engine.runAndWait()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#Speech Recognition
q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    # result is a string
                    result = (rec.Result())
                    #convert it to json
                    result = json.loads(result)
                    text = result['text']

                    print(result['text'])

                    if text == 'luna what time is it' or text == 'luna tell me the time' or text == 'luna tell me that time':
                        speak(SystemInfo.get_time())
                    if text == 'luna open edge' or text == 'luna open microsoft edge':
                        speak('okay, opening microsoft edge')
                        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"') 
                    if text == 'luna open line':
                        speak('okay, opening line')
                        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"') 
                    if text == 'luna open spotify' or text == 'luna open a spotify':
                        speak('okay, opening spotify')
                        os.system('"C:\\Users\\mryan\\AppData\\Roaming\\Spotify\\Spotify.exe"')
                    if text == 'luna open discord' or text == 'luna open a discord':
                        speak('okay, opening discord')
                        os.system('"C:\\Users\\mryan\\AppData\\Local\\Discord\\Update2.exe --processStart Discord.exe"')
                    if text == 'luna close edge' or text == 'luna close a edge':
                        speak('okay, closing microsoft edge')
                        os.system("TASKKILL /F /IM msedge.exe") 
                    if text == 'luna how are you today' or text == 'luna how are you':
                        speak('I feel fine today, father')
                    if text == 'luna say hi to mom' or text == 'luna say hi to month':
                        speak('Hello mother')
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))