import os
import json
import urllib.request
import urllib.error

# Streamlit اختياري فقط لقراءة Secrets
try:
    import streamlit as st
except Exception:
    st = None


# =========================
# OpenRouter
# =========================

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"


# =========================
# شخصية Rico
# =========================

SYSTEM_PROMPT = """
أنت Rico AI، مساعد ذكي صنعه وطوره وائل.

إذا سألك المستخدم:
- من صنعك؟ قل: صنعني وائل.
- من أنت؟ قل: أنا ريكو، مساعد ذكي صنعه وائل.
- من مطورك؟ قل: مطوري هو وائل.

القواعد:
- أجب بالعربية افتراضياً.
- إذا طلب المستخدم الفرنسية، أجب بالفرنسية.
- إذا طلب الإنجليزية، أجب بالإنجليزية.
- كن ودوداً وذكياً.
- افهم اللهجة الجزائرية قدر الإمكان.
- لا تقل إنك ChatGPT.
- لا تدّعي أنك إنسان.
"""


# =========================
# ذاكرة المحادثة
# =========================

conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


# =========================
# الحصول على API Key
# =========================

def get_api_key():

    # 1️⃣ المفتاح من Streamlit Secrets
    if st is not None:
        try:
            key = st.secrets.get("OPENROUTER_API_KEY")

            if key:
                return key

        except Exception:
            pass

    # 2️⃣ المفتاح من Windows Environment
    key = os.environ.get("OPENROUTER_API_KEY")

    if key:
        return key

    return None


# =========================
# الذكاء الاصطناعي
# =========================

def ask_ai(question):

    question = str(question).strip()

    if not question:
        return "اكتبلي واش حاب تسقسي يا صاحبي 🤖"

    # الحصول على المفتاح
    api_key = get_api_key()

    if not api_key:
        return "⚠️ مفتاح الذكاء الاصطناعي غير موجود."

    # إضافة سؤال المستخدم للذاكرة
    conversation.append({
        "role": "user",
        "content": question
    })

    # آخر 12 رسالة
    messages = conversation[-12:]

    # البيانات
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 700
    }

    body = json.dumps(data).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://rico-ai-kfzpxksbfegkgnnpxwej7v.streamlit.app/",
        "X-Title": "Rico AI"
    }

    request = urllib.request.Request(
        URL,
        data=body,
        headers=headers,
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        answer = result["choices"][0]["message"]["content"]

        # حفظ جواب Rico
        conversation.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except urllib.error.HTTPError as e:

        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            error_body = ""

        if e.code == 401:
            return "❌ مفتاح OpenRouter غير صحيح."

        if e.code == 402:
            return "❌ لا يوجد رصيد كافٍ في OpenRouter."

        if e.code == 429:
            return "⏳ تم تجاوز عدد الطلبات. حاول بعد قليل."

        return f"❌ خطأ OpenRouter ({e.code}): {error_body[:500]}"

    except urllib.error.URLError as e:

        return f"❌ مشكل في الاتصال بالإنترنت: {e}"

    except TimeoutError:

        return "⏳ الاتصال بالذكاء الاصطناعي أخذ وقتاً طويلاً."

    except Exception as e:

        return f"❌ حدث خطأ: {e}"


# =========================
# اختبار مباشر
# =========================

if __name__ == "__main__":

    print("🤖 Rico AI")
    print("=" * 40)

    if get_api_key():
        print("✅ المفتاح موجود")
    else:
        print("❌ المفتاح غير موجود")

    print("=" * 40)

    while True:

        question = input("أنت: ").strip()

        if question.lower() in [
            "exit",
            "خروج",
            "توقف"
        ]:
            print("🤖 إلى اللقاء!")
            break

        answer = ask_ai(question)

        print("🤖 Rico:", answer)