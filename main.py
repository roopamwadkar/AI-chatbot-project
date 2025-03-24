import speech_recognition as sr
import webbrowser
import pyttsx3
import google.generativeai as genai
import musiclibrary

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice and rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 150)

# API key configuration
genai.configure(api_key="___________") 
model = genai.GenerativeModel("gemini-1.5-pro-latest")


# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# AI function
def ai_process(query):
    try:
        response = model.generate_content(query)
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm sorry, I couldn't process that request."

# Command processing function
def processCommand(command):
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open spotify" in command:
        speak("Playing music")
        webbrowser.open("https://www.spotify.com")
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        try:
            link = musiclibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        except KeyError:
            speak("I couldn't find that song. Let me search on YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
    else:
        #  speak("Let me think...")
         response = ai_process(command)
         speak(response)

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source)
                wake_word = recognizer.recognize_google(audio).lower()

                if wake_word == "jarvis":
                    speak("Hey! How can I help you?")
                    print("Jarvis is active...")

                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Didn't catch that. Listening again...")
        except Exception as e:
            print(f"Error: {e}")
            speak("I'm sorry, I didn't get that.")
