import subprocess
import os
import winsound
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PIPER_EXE = os.path.join(BASE_DIR, "piper", "piper.exe")
VOICE_MODEL = os.path.join(BASE_DIR, "voices", "miro_ar.onnx")
VOICE_CONFIG = os.path.join(BASE_DIR, "voices", "miro_ar.piper.json")

def speak(text):
    print("🤖", text)

    try:
        # تشغيل Piper وإرسال النص له
        process = subprocess.run(
            [
                PIPER_EXE,
                "--model", VOICE_MODEL,
                "--config", VOICE_CONFIG
            ],
            input=text + "\n",
            text=True,
            encoding="utf-8",
            capture_output=True
        )

        if process.returncode != 0:
            print("❌ خطأ Piper:")
            print(process.stderr)
            return

        # Piper ينشئ ملف WAV تلقائيا في مجلد المشروع
        output_lines = process.stdout.strip().splitlines()

        wav_file = None

        for line in output_lines:
            if line.lower().endswith(".wav"):
                wav_file = line.strip()

        if not wav_file:
            print("❌ ما لقيتش ملف الصوت.")
            return

        # تشغيل الصوت
        winsound.PlaySound(
            wav_file,
            winsound.SND_FILENAME
        )

        # حذف الملف بعد التشغيل
        try:
            os.remove(wav_file)
        except:
            pass

    except Exception as e:
        print("❌ خطأ الصوت:", e)