import speech_recognition
import pyaudio

recognizer = speech_recognition.Recognizer()
with speech_recognition.Microphone() as source:
    print("What song would you like to sing? ")
    audio = recognizer.listen(source)
words = recognizer.recognize_google(audio)

if 'pump up the jam' in words.lower():
    print("Playing Pump Up the Jam")
elif 'doctor worm' in words.lower():
    print("Playing Doctor Worm")