import speech_recognition

recognizer = speech_recognition.Recognizer()
recognizer.operation_timeout = 10

print("Yo! What's good?")

try:
    with speech_recognition.Microphone() as source:
        print("Setting up the mic. Keep it down for a sec...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            choice = input("\nHit Enter if you're too Legit, or hit Q to Quit: ")

            if choice.lower().strip() == "q":
                print("Catch you later!")
                break

            try:
                print("What track do you want me to spin for you?")
                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=8
                )

                print("Bet. Let me see what I got...")
                words = recognizer.recognize_google(audio)
                print("You said:", words)

                if "pump up the jam" in words.lower():
                    print("Nice choice! Here's: Pump Up the Jam")
                elif "doctor worm" in words.lower():
                    print("Nice choice! Here's: Doctor Worm")
                else:
                    print("I don't have that one.")
                    print("See how Pump Up the Jam or Doctor Worm works for you.")

            except speech_recognition.WaitTimeoutError:
                print("Couldn't hear you. Say it again.")

            except speech_recognition.UnknownValueError:
                print("That's on me. What'd you say?")

            except speech_recognition.RequestError as error:
                print("I wasn't able to connect. Looks like:", error)

except OSError as error:
    print("Couldn't use the mic:", error)