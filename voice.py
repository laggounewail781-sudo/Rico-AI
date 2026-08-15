import speech_recognition as sr


# =========================================================
# Rico AI - Voice Recognition
# =========================================================

recognizer = sr.Recognizer()

# تحسين التعرف على الكلام
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


def listen():
    """
    يستمع من الميكروفون ويحول الكلام إلى نص.
    """

    try:

        with sr.Microphone() as source:

            print("🎤 Rico يسمعك...")

            # معايرة الضجيج المحيط
            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=15
            )

        print("🧠 Rico يحاول يفهمك...")

        text = recognizer.recognize_google(
            audio,
            language="ar-DZ"
        )

        text = text.strip()

        if text:

            print("👤 أنت:", text)

        return text


    except sr.WaitTimeoutError:

        print("⏳ Rico ما سمع حتى كلام.")

        return ""


    except sr.UnknownValueError:

        print("❓ Rico ما فهمش الكلام.")

        return ""


    except sr.RequestError as error:

        print("❌ خدمة التعرف على الصوت غير متاحة:")
        print(error)

        return ""


    except OSError as error:

        print("❌ مشكل في الميكروفون:")
        print(error)

        return ""


    except Exception as error:

        print("❌ خطأ في الصوت:")
        print(error)

        return ""


# =========================================================
# اختبار مستقل
# =========================================================

if __name__ == "__main__":

    print("=" * 45)
    print("🎤 Rico AI - اختبار الميكروفون")
    print("=" * 45)

    while True:

        print("\nاضغط Enter واهدر مع Rico.")

        command = input(
            "أو اكتب exit للخروج: "
        ).strip()

        if command.lower() == "exit":

            print("🤖 انتهى الاختبار.")

            break

        text = listen()

        if text:

            print("🤖 النص الذي فهمه Rico:", text)

        else:

            print("🤖 ما قدرتش نفهم الكلام.")
