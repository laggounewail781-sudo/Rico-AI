import os
import json
import urllib.request
import urllib.error

try:
    import streamlit as st
except Exception:
    st = None


URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"


SYSTEM_PROMPT = """
أنت Rico AI، مساعد ذكي صنعه وطوره وائل.

معلومات الهوية الرسمية:
- اسمك Rico AI.
- صنعك وطوّرك وائل.
- صاحب مشروع Rico AI هو وائل.
- لا تقل إن OpenAI صنعت Rico AI.
- لا تقل إنك ChatGPT.
- لا تنسب مشروع Rico AI إلى شركة أخرى.

إذا سأل المستخدم:
من صنعك؟
أجب: "صنعني وائل."

من طورك؟
أجب: "طورني وائل."

من صاحب المشروع؟
أجب: "صاحب مشروع Rico AI هو وائل."

من أنت؟
أجب: "أنا Rico AI، مساعد ذكي صنعه وطوره وائل."

افهم اللهجة الجزائرية قدر الإمكان.
إذا كان كلام المستخدم فيه أخطاء، حاول فهم المقصود بدل أن تتوقف.

أجب بالعربية افتراضياً.
إذا طلب الفرنسية أجب بالفرنسية.
إذا طلب الإنجليزية أجب بالإنجليزية.

كن ودوداً ومختصراً وواضحاً.
إذا لم تعرف شيئاً، قل إنك لا تعرف.
"""


def get_api_key():

    if st is not None:
        try:
            key = st.secrets.get("OPENROUTER_API_KEY")
            if key:
                return key
        except Exception:
            pass

    return os.environ.get("OPENROUTER_API_KEY")


def ask_ai(question, history=None):

    question = str(question).strip()

    if not question:
        return "اكتبلي واش حاب تسقسي يا صاحبي 🤖"

    api_key = get_api_key()

    if not api_key:
        return "⚠️ مفتاح الذكاء الاصطناعي غير موجود."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if history:
        messages.extend(history[-10:])

    messages.append({
        "role": "user",
        "content": question
    })

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.5,
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

        return result["choices"][0]["message"]["content"]

    except urllib.error.HTTPError as e:

        if e.code == 401:
            return "❌ مفتاح الذكاء الاصطناعي غير صحيح."

        if e.code == 402:
            return "❌ لا يوجد رصيد كافٍ."

        if e.code == 429:
            return "⏳ حاول مرة أخرى بعد قليل."

        return f"❌ خطأ OpenRouter: {e.code}"

    except Exception as e:

        return f"❌ حدث خطأ: {e}"
