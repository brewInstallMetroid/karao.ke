import speech_recognition

recognizer = speech_recognition.Recognizer()
recognizer.operation_timeout = 10

print("Yo! What's good?")

try:
    with speech_recognition.Microphone() as source:
        print("Setting up the mic. Keep it down for a sec...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            choice = input("\nHit Enter if you're too Legit, or hit Q then Enter to Quit: ")

            if choice.lower().strip() == "q":
                print("Catch you later!")
                break

            try:
                print("What song are we singing?")
                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=8
                )

                print("Bet. Let me see what I got...")
                words = recognizer.recognize_google(audio)
                print("You said:", words)

                while True:
                    confirmation = input("Is that right? (Y/N): ").strip().lower()
                    if confirmation in ("y", "yes", "n", "no"):
                        break  
                    
                    print("Just Y or N works. Let's try again.")

                if confirmation in ("n", "no"):
                    print("My bad. Let's try again.") 
                    continue

                if "pump up the jam" in words.lower():
                    print("Nice choice! Here's: Pump Up the Jam")
                elif "doctor worm" in words.lower():
                    print("Nice choice! Here's: Doctor Worm")
                else:
                    print("I don't have that one.")
                    print("Want to give Pump Up the Jam or Doctor Worm a try?")

            except speech_recognition.WaitTimeoutError:
                print("Couldn't hear you. Say it again.")

            except speech_recognition.UnknownValueError:
                print("That's on me. What'd you say?")

            except speech_recognition.RequestError as error:
                print("I wasn't able to connect. Looks like:", error)

except OSError as error:
    print("Couldn't use the mic:", error)