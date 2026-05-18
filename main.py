import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
from duckduckgo_search import DDGS
import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

import speech_recognition as sr
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(i, name)


# === Text-to-Speech ===

def speak(text):
    print("JARVIS:", text)
    speaker.Speak(text)


# === Greeting ===
def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good Morning!"
    elif hour < 18:
        greet = "Good Afternoon!"
    else:
        greet = "Good Evening!"
    speak(f"{greet} I am JARVIS. Say or type 'hey jarvis' to wake me up.")

# === Wake Word Listening ===
def wait_for_wake_word():
    recognizer = sr.Recognizer()
    mic_index = 1  # Replace with your correct microphone index

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("🎤 Say 'hey jarvis'...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            query = recognizer.recognize_google(audio).lower()
            print("Heard:", query)
            if "hey jarvis" in query:
                speak("Yes, I'm listening.")
                return True
    except:
        pass

    typed = input("⌨️ Type 'hey jarvis' or 'exit': ").lower()
    if typed == "hey jarvis":
        speak("Yes, I'm listening.")
        return True
    elif typed == "exit":
        speak("Goodbye.")
        exit()
    return False

# === Take Voice or Text Command ===
def take_command():
    recognizer = sr.Recognizer()
    mic_index = 1

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            query = recognizer.recognize_google(audio).lower()
            print("YOU:", query)
            return query
    except:
        speak("I didn't catch that. Please type your command.")
        return input("⌨️ Type: ").lower()

# === DuckDuckGo Top Result ===
def search_google_top_result(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=1)
            for r in results:
                title = r['title']
                body = r['body']
                url = r['href']

                print("\n🔎 Top Result:")
                print("📌", title)
                print("📝", body)
                print("🌐", url)

                speak(f"Top result is: {title}")
                if body:
                    speak("Here's a brief summary:")
                    speak(body[:300])
                else:
                    speak("No readable summary available.")
                speak("Opening the result in your browser.")
                webbrowser.open(url)
                return
        speak("Sorry, I couldn't find anything useful.")
    except Exception as e:
        speak("There was a problem searching.")
        print("Error:", e)

# === Open Files or Apps ===
def open_file_or_app(query):
    try:
        if "notepad" in query:
            os.system("notepad")
            speak("Opening Notepad.")
        elif "calculator" in query:
            os.system("start calc")
            speak("Opening Calculator.")
        elif "command prompt" in query or "cmd" in query:
            os.system("start cmd")
            speak("Opening Command Prompt.")
        elif "chrome" in query:
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if os.path.exists(chrome_path):
                os.startfile(chrome_path)
                speak("Opening Chrome.")
            else:
                speak("Chrome is not found in the usual location.")
        elif "d drive" in query:
            os.startfile("D:\\")
            speak("Opening D drive.")
        elif "c drive" in query:
            os.startfile("C:\\")
            speak("Opening C drive.")
        else:
            path = query.lower().replace("open", "").strip().strip('"')
            if os.path.exists(path):
                os.startfile(path)
                speak(f"Opening {path}")
            else:
                speak("Sorry, I couldn't find that file or folder.")
                print("Path not found:", path)
    except Exception as e:
        speak("Something went wrong while trying to open.")
        print("Error:", e)

# === Handle Commands ===
def handle_command(query):
    if "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "wikipedia" in query:
        speak("What should I search on Wikipedia?")
        topic = take_command()
        try:
            summary = wikipedia.summary(topic, sentences=3)
            print("📚 Wikipedia Summary:\n", summary)
            speak(f"According to Wikipedia, here is a summary about {topic}.")
            speak(summary[:300])
        except Exception as e:
            speak("Sorry, I couldn't find anything on that topic.")
            print("Wikipedia error:", e)

    elif "search" in query or "google" in query:
        speak("What should I search?")
        search_query = take_command()
        search_google_top_result(search_query)

    elif "open" in query:
        open_file_or_app(query)

    elif "exit" in query or "bye" in query:
        speak("Goodbye.")
        exit()

    else:
        speak("Sorry, I didn't understand that.")

# === Main Program ===
if __name__ == "__main__":
    wish_user()
    while True:
        if wait_for_wake_word():
            user_query = take_command()
            handle_command(user_query)
