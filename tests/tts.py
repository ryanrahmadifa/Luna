import pyttsx3
engine = pyttsx3.init()

engine.say("Hello")
engine.runAndWait()

voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)