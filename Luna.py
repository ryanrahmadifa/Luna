
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
import schedule
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
                    if text == 'luna clear' or text == 'luna clean' or text == 'luna refresh':
                        speak('clearing memory')
                        os.system('cls')

                    # Running applications

                    if text == 'luna open edge' or text == 'luna open microsoft edge':
                        os.system('"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"') 
                        speak('opening microsoft edge')
                    if text == 'luna open line':
                        os.system('"C:\\Users\\mryan\\AppData\\Local\LINE\\bin\\current\\LINE.exe"')
                        speak('opening line') 
                    if text == 'luna open spotify' or text == 'luna open a spotify':
                        os.system('"C:\\Users\\mryan\\AppData\\Roaming\\Spotify\\Spotify.exe"')
                        speak('opening spot a fy')
                    if text == 'luna open discord' or text == 'luna open a discord':
                        os.system('"C:\\Users\\mryan\\AppData\\Local\\Discord\\Update2.exe --processStart Discord.exe"')
                        speak('opening discord')
                    if text == 'luna open teams' or text == 'luna open a teams':
                        os.system('"C:\\Users\\mryan\\AppData\\Local\\Microsoft\\Teams\\Update.exe --processStart "Teams.exe""')
                        speak('opening microsoft teams')
                    if text == 'luna open one drive' or text == 'luna open want drive' or text == 'who do not open one drive':
                        os.system('"C:\Program Files (x86)\Microsoft OneDrive\OneDrive.exe"')
                        speak('opening microsoft one drive')
                    if text == "luna open what's up" or text == "when i open what's up" or text == "when i opened what's app":
                        os.system('"C:\\Users\\mryan\\AppData\\Local\\WhatsApp\\WhatsApp.exe"')
                        speak('opening whats app')
                    if text == 'luna open notepad' or text == 'luna open not bad':
                        os.system('"%windir%\\system32\\notepad.exe"')
                        speak('opening note pad')

                    # Open websites as a new tab

                    if text == 'luna open google':
                        webbrowser.open_new('http://www.google.com')
                        speak('opening google')
                    if text == 'luna open here too' or text == 'luna open you tube' or text == 'luna open you too':
                        webbrowser.open_new('http://www.youtube.com')
                        speak('opening you tube')
                    if text == 'luna open i do next' or text == 'luna open and do next' or text == 'luna open a do next':
                        webbrowser.open_new('https://edunex.itb.ac.id')
                        speak('opening and do next')
                    if text == 'luna open see x' or text == 'luna open sea acts' or text == 'luna open sea x' or text == 'luna open sea eggs' or text == 'luna oh can see x' or text == 'luna open six':
                        webbrowser.open_new('https://akademik.itb.ac.id/app/K/mahasiswa:16721425+2021-1/kelas/jadwal/mahasiswa')
                        speak('opening see x')
                    if text == 'luna open trading view' or text == 'luna open trade and view':
                        webbrowser.open_new('https://www.tradingview.com/chart/')
                        speak('opening trading view')
                    if text == 'luna open email' or text == 'luna open de mayo':
                        webbrowser.open_new('https://mail.google.com/mail/u/1/#inbox')
                        speak('opening gee mail')
                    if text == 'luna open twitch':
                        webbrowser.open_new('https://twitch.tv/')
                        speak('opening twitch')
                    if text == 'luna openly january' or text == 'luna open dictionary' or text == 'when i opened dictionary':
                        webbrowser.open_new('https://www.merriam-webster.com/')
                        speak('opening dictionary')
                    if text == 'luna open can be be' or text == 'who now open can be be':
                        webbrowser.open_new('https://kbbi.web.id/')
                        speak('opening dictionary')
                    if text == 'luna open instagram':
                        webbrowser.open_new('https://www.instagram.com/')
                        speak('opening instagram')
                    if text == 'luna open market' or text == 'luna open online shop':
                        webbrowser.open_new('https://www.tokopedia.com/')
                        speak('opening online shop')
                    if text == 'luna open link and' or text == 'luna open link in' or text == 'luna open linked in' or text == 'luna open linked then' or text == 'luna open link then' or text == 'luna open linked him':
                        webbrowser.open_new('https://www.linkedin.com/in/ryan-rahmadifa-b04486219/')
                        speak('opening linked in')
                    if text == 'luna open calculator' or text == 'luna open well from' or text == 'luna open wolfram' or text == 'luna open while from':
                        webbrowser.open_new('https://www.wolframalpha.com/')
                        speak('opening wolf ram alpha')
                    if text == 'luna open rep playlist' or text == 'luna open rap playlist':
                        webbrowser.open_new('https://open.spotify.com/playlist/01QJEaau6MD8AZBx8Gq0ZN/')
                        speak('opening spot a fy')
                    if text == 'luna open lo fi playlist' or text == 'luna open a lofi playlist':
                        webbrowser.open_new('https://open.spotify.com/playlist/62avPAI9LV5bRRAaMUPgAF/')
                        speak('opening spot a fy')
                    if text == 'luna open life playlist' or text == 'luna open soundtrack playlist':
                        webbrowser.open_new('https://open.spotify.com/playlist/2qFazgtuYfWyjb3rRIU1tU/')
                        speak('opening spot a fy')
                    if text == 'luna open enemy playlist' or text == 'luna open annie may playlist':
                        webbrowser.open_new('https://open.spotify.com/playlist/0Cn8526CF48hDmLUF2rfvZ/')
                        speak('opening spot a fy')

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
                    if text == "luna close what's up" or text == "luna close what's app":
                        speak('okay, closing whats app')
                        os.system("TASKKILL /F /IM WhatsApp.exe") 
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