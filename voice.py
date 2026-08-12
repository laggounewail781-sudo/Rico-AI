import re
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 400
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5


def is_valid_text(text):
    text = text.strip()
    if not text:
        return False
    if len(text) < 2:
        return False

    arabic_letters = re.findall(r"[ء-ي]", text)
    if len(arabic_letters) < 2:
        return False

    cleaned = re.sub(r"[^ء-ي\s]", "", text)
    if not cleaned or len(cleaned) < 2:
        return False

    return True


def listen():
    with sr.Microphone() as source:
        print("🎤 تكلم...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        audio = recognizer.listen(source, phrase_time_limit=6)

    try:
        text = recognizer.recognize_google(audio, language="ar-DZ")
        text = text.lower().strip()

        if not is_valid_text(text):
            print("❌ كانت هناك ضوضاء أو نص غير صالح.")
            return ""

        print("👤 أنت:", text)
        return text

    except sr.UnknownValueError:
        print("❌ لم أفهم كلامك.")
        return ""

    except sr.RequestError:
        print("❌ لا يوجد اتصال بالإنترنت.")
        return ""