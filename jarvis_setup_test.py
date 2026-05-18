import speech_recognition as sr
import pyttsx3

# === STEP 1: List Available Microphones ===
print("🎙️ Available Microphones:")
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {mic}")

# === STEP 2: Test Microphone Input ===
mic_index = 1  # 🔁 Change this index based on the above list

print("\n🎤 Microphone Test:")
recognizer = sr.Recognizer()

try:
    with sr.Microphone(device_index=mic_index) as source:
        print("👉 Please say something into the mic...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        print("✅ Audio captured!")

    try:
        query = recognizer.recognize_google(audio)
        print("🧠 You said:", query)
    except sr.UnknownValueError:
        print("❌ Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print("❌ Failed to access microphone:", e)

# === STEP 3: Test Text-to-Speech ===
print("\n🔊 Testing JARVIS Voice...")
try:
    engine = pyttsx3.init()
    engine.say("Hello! I am Jarvis, your Python voice assistant.")
    engine.runAndWait()
    print("✅ Voice played successfully.")
except Exception as e:
    print("❌ Text-to-speech engine failed:", e)
