import os
import webbrowser
from urllib.parse import quote
from difflib import get_close_matches

from data import OPEN_WORDS, CLOSE_WORDS


def smart_match(word, choices):
    result = get_close_matches(
        word,
        choices,
        n=1,
        cutoff=0.45
    )

    return result[0] if result else None


def clean_text(text):
    text = text.lower().strip()

    for word in OPEN_WORDS:
        text = text.replace(word, "")

    for word in CLOSE_WORDS:
        text = text.replace(word, "")

    return text.strip()


def is_open_command(text):
    return any(word in text.lower() for word in OPEN_WORDS)


def is_close_command(text):
    return any(word in text.lower() for word in CLOSE_WORDS)


def open_program(name, programs):
    if name in programs:
        try:
            os.system(programs[name])
            return True
        except Exception as e:
            print("خطأ فتح البرنامج:", e)
            return False

    return False


def open_site(name, sites):
    if name in sites:
        try:
            webbrowser.open(sites[name])
            return True
        except Exception as e:
            print("خطأ فتح الموقع:", e)
            return False

    return False


def google_search(text):
    try:
        url = "https://www.google.com/search?q=" + quote(text)
        webbrowser.open(url)
        return True
    except Exception as e:
        print("خطأ Google:", e)
        return False


def youtube_search(text):
    try:
        url = "https://www.youtube.com/results?search_query=" + quote(text)
        webbrowser.open(url)
        return True
    except Exception as e:
        print("خطأ YouTube:", e)
        return False


def close_program(name):

    tasks = {
        "كروم": "chrome.exe",
        "الحاسبة": "CalculatorApp.exe",
        "المفكرة": "notepad.exe",
        "الرسام": "mspaint.exe",
    }

    if name in tasks:
        os.system(f'taskkill /f /im {tasks[name]}')
        return True

    return False