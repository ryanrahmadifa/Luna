
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
import webbrowser
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

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 16000, device=args.device, dtype='int16',
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

                    # Basic conversations
                    
                    if text == 'luna what time is it' or text == 'luna tell me the time' or text == 'luna tell me that time':
                        speak(SystemInfo.get_time())
                    if text == 'thank you luna' or text == 'good job luna' or text == 'thanks luna':
                        speak('youre welcome')
                    if text == 'good morning luna' or text == 'morning luna':
                        speak('morning ryan')

                    # Running applications

                    if text == 'luna open edge' or text == 'luna open microsoft edge':
                        speak('okay, opening microsoft edge')
                        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"') 
                    if text == 'luna open line':
                        speak('okay, opening line')
                        os.system('"C:\\Users\\mryan\\AppData\\Local\LINE\\bin\\current\\LINE.exe"') 
                    if text == 'luna open spotify' or text == 'luna open a spotify':
                        speak('okay, opening spot a fy')
                        os.system('"C:\\Users\\mryan\\AppData\\Roaming\\Spotify\\Spotify.exe"')
                    if text == 'luna open discord' or text == 'luna open a discord':
                        speak('okay, opening discord')
                        os.system('"C:\\Users\\mryan\\AppData\\Local\\Discord\\Update2.exe --processStart Discord.exe"')
                    if text == 'luna open teams' or text == 'luna open a teams':
                        speak('okay, opening microsoft teams')
                        os.system('"C:\\Users\\mryan\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart "Teams.exe""')
                    if text == 'luna open one drive' or text == 'luna open want drive' or text == 'who do not open one drive':
                        speak('okay, opening microsoft one drive')
                        os.system('"C:\Program Files (x86)\Microsoft OneDrive\OneDrive.exe"')
                    if text == 'luna open play list ' or text == 'luna open playlist':
                        speak('okay, opening spotify')
                        webbrowser.open_new('https://open.spotify.com/playlist/0Cn8526CF48hDmLUF2rfvZ')

                    # Open websites as a new tab

                    if text == 'luna open google':
                        speak('okay, opening google')
                        webbrowser.open_new('http://www.google.com')
                    if text == 'luna open here too' or text == 'luna open you tube' or text == 'luna open you too':
                        speak('okay, opening you tube')
                        webbrowser.open_new('http://www.youtube.com')
                    if text == 'luna open i do next' or text == 'luna open and do next' or text == 'luna open a do next':
                        speak('okay, opening and do next')
                        webbrowser.open_new('https://edunex.itb.ac.id')
                    if text == 'luna open see x' or text == 'luna open sea acts' or text == 'luna open sea x' or text == 'luna open sea eggs' or text == 'luna oh can see x' or text == 'who do not open sea x':
                        speak('okay, opening see x')
                        webbrowser.open_new('https://akademik.itb.ac.id')
                    if text == 'luna open trading view' or text == 'luna open trade and view':
                        speak('okay, opening trading view')
                        webbrowser.open_new('https://www.tradingview.com/chart/')
                    if text == 'luna open email' or text == 'luna open de mayo':
                        speak('okay, opening gee mail')
                        webbrowser.open_new('https://mail.google.com/mail/u/1/#inbox')
                    if text == 'luna open twitch':
                        speak('okay, opening twitch')
                        webbrowser.open_new('https://twitch.tv/')
                    if text == 'luna openly january' or text == 'luna open dictionary' or text == 'when i opened dictionary':
                        speak('okay, opening dictionary')
                        webbrowser.open_new('https://www.merriam-webster.com/')
                    if text == 'luna open can be be' or text == 'who now open can be be':
                        speak('okay, opening dictionary')
                        webbrowser.open_new('https://kbbi.web.id/')

                    # Closing applications

                    if text == 'luna close teams' or text == 'luna close a teams':
                        speak('okay, closing microsoft teams')
                        os.system("TASKKILL /F /IM Teams.exe") 
                    if text == 'luna close discord' or text == 'luna close a discord':
                        speak('okay, closing discord')
                        os.system("TASKKILL /F /IM Discord.exe") 
                    if text == 'luna close line' or text == 'luna clothes line':
                        speak('okay, closing line')
                        os.system("TASKKILL /F /IM LINE.exe") 
                    if text == 'luna close edge' or text == 'luna close a edge':
                        speak('okay, closing microsoft edge')
                        os.system("TASKKILL /F /IM msedge.exe") 
                    if text == 'luna go to sleep' or text == 'luna go sleep':
                        speak('okay, laptop will be going to sleep mode')
                        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    if text == 'luna shut down' or text == 'luna go shut down':
                        speak('okay, shutting down the laptop')
                        os.system('shutdown -s -t 0')
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))