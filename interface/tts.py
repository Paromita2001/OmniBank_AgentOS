import pyttsx3
import threading


def speak_text(text: str):
    """
    Speak text using offline TTS.
    Runs in background thread so Streamlit doesn't freeze.
    """
    def run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=run).start()