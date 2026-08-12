from datetime import datetime

from brain import smart_match, clean_text, is_open_command
from data import PROGRAMS, SITES
from functions import (
    open_program,
    open_site,
    google_search,
    youtube_search
)
from ai_chat import ask_ai


def process_command(text):

    text = text.lower().strip()

    # =========================
    # التحية
    # =========================

    if "مرحبا" in text or "السلام عليكم" in text:
        return "مرحبا وائل"

    elif "كيف حالك" in text:
        return "أنا بخير الحمد لله"

    elif "اسمك" in text:
        return "اسمي ريكو"

    # =========================
    # الوقت والتاريخ
    # =========================

    elif "الوقت" in text or "الساعة" in text:
        return datetime.now().strftime("%H:%M")

    elif "التاريخ" in text:
        return datetime.now().strftime("%d/%m/%Y")

    # =========================
    # البحث في جوجل
    # =========================

    elif "ابحث في جوجل عن" in text:

        search = text.replace(
            "ابحث في جوجل عن",
            ""
        ).strip()

        if search:
            google_search(search)
            return "جاري البحث في جوجل"

        return "ماذا تريد أن أبحث عنه؟"

    # =========================
    # البحث في يوتيوب
    # =========================

    elif "ابحث في يوتيوب عن" in text:

        search = text.replace(
            "ابحث في يوتيوب عن",
            ""
        ).strip()

        if search:
            youtube_search(search)
            return "جاري البحث في يوتيوب"

        return "ماذا تريد أن أبحث عنه في يوتيوب؟"

    # =========================
    # فتح البرامج والمواقع
    # =========================

    elif is_open_command(text):

        command = clean_text(text)

        # برنامج
        app = smart_match(
            command,
            PROGRAMS.keys()
        )

        if app:
            if open_program(app, PROGRAMS):
                return f"جاري فتح {app}"

        # موقع
        site = smart_match(
            command,
            SITES.keys()
        )

        if site:
            if open_site(site, SITES):
                return f"جاري فتح {site}"

        # إذا لم يجد برنامج أو موقع
        google_search(command)

        return f"لم أجد {command}، سأبحث عنه في جوجل"

    # =========================
    # الذكاء الاصطناعي
    # =========================

    else:
        return ask_ai(text)