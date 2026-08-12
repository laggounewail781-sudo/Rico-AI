import os
import requests

# =========================
# OpenRouter
# =========================

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"


# =========================
# شخصية ريكو
# =========================

SYSTEM_PROMPT = """
أنت ريكو AI.

أنت مساعد ذكي صنعه وطور وائل.

إذا سألك المستخدم:
- من صنعك؟ قل: صنعني وائل.
- من أنت؟ قل: أنا ريكو، مساعد ذكي صنعه وائل.
- من مطورك؟ قل: مطوري هو وائل.

أجب بالعربية افتراضياً.
إذا طلب المستخدم الفرنسية أو الإنجليزية، استعمل اللغة المطلوبة.

كن ودوداً، مختصراً، وذكياً.
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
# AI
# =========================

def ask_ai(question):

    # نقرأ المفتاح مباشرة وقت الطلب
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        return "مفتاح الذكاء الاصطناعي غير موجود."

    conversation.append({
        "role": "user",
        "content": question
    })

    messages = conversation[-12:]

    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:

        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=30
        )

        # إذا كان OpenRouter رجع خطأ، نعرضه
        if response.status_code != 200:
            return f"خطأ OpenRouter {response.status_code}: {response.text[:500]}"

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        conversation.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except requests.exceptions.Timeout:
        return "الاتصال بالذكاء الاصطناعي أخذ وقتاً طويلاً."

    except requests.exceptions.RequestException as e:
        return f"خطأ في الاتصال: {e}"

    except Exception as e:
        return f"خطأ: {e}"


# =========================
# اختبار
# =========================

if __name__ == "__main__":

    print("🤖 Rico AI - اختبار الذكاء الاصطناعي")
    print("=" * 45)

    while True:

        question = input("أنت: ").strip()

        if not question:
            continue

        if question.lower() in ["exit", "خروج", "توقف"]:
            print("🤖 إلى اللقاء")
            break

        answer = ask_ai(question)

        print("🤖 ريكو:", answer)