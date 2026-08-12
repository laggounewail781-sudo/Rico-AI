from difflib import get_close_matches

OPEN_WORDS = [

    "افتح",
    "افتحلي",
    "افتح لي",

    "شغل",
    "شغللي",
    "شغل لي",

    "ابدأ",

    "نحب نفتح",

    "اريد فتح",
    "أريد فتح",

    "من فضلك افتح",

]

def smart_match(word, choices):

    result = get_close_matches(

        word,

        choices,

        n=1,

        cutoff=0.55

    )

    if result:

        return result[0]

    return None


def clean_text(text):

    text = text.lower().strip()

    for word in OPEN_WORDS:

        text = text.replace(word, "")

    return text.strip()


def is_open_command(text):

    text = text.lower()

    for word in OPEN_WORDS:

        if word in text:

            return True

    return False