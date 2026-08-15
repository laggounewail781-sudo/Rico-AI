import streamlit as st
from datetime import datetime
import urllib.request

from ai_chat import ask_ai


st.set_page_config(
    page_title="Rico AI",
    page_icon="🤖",
    layout="wide"
)


# =========================
# MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = []


# =========================
# STYLE - NO HTML
# =========================

st.markdown("""
<style>
.stApp {
    background: #050b12;
}

.block-container {
    max-width: 1400px;
    padding-top: 25px;
}

section[data-testid="stSidebar"] {
    background: #071019;
}

.rico-box {
    background: #08121c;
    border: 1px solid #203746;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.rico-face {
    font-size: 100px;
    padding: 35px;
}

.info-box {
    background: #0a151f;
    border: 1px solid #203746;
    border-radius: 10px;
    padding: 10px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)


# =========================
# TIME / DATE
# =========================

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%d/%m/%Y")


# =========================
# WEATHER
# =========================

try:
    weather = urllib.request.urlopen(
        "https://wttr.in/Algeria?format=%C+%t",
        timeout=5
    ).read().decode("utf-8")
except Exception:
    weather = "غير متوفر حالياً"


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🤖 RICO AI")

    st.divider()

    st.subheader("🕐 الوقت")
    st.info(current_time)

    st.subheader("📅 التاريخ")
    st.info(current_date)

    st.subheader("🌤️ الطقس")
    st.info(weather)

    st.divider()

    if st.button(
        "➕ محادثة جديدة",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    if st.button(
        "🗑️ مسح المحادثة",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# =========================
# HEADER
# =========================

st.title("🤖 Rico AI")

st.caption(
    "مساعدك الذكي — الكتابة متاحة الآن"
)


# =========================
# COLUMNS
# =========================

chat_col, rico_col = st.columns(
    [3, 1],
    gap="large"
)


# =========================
# CHAT
# =========================

with chat_col:

    st.subheader("💬 المحادثة")

    if not st.session_state.messages:

        st.info(
            "👋 مرحباً! أنا Rico. اكتبلي أي سؤال."
        )

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message("user"):
                st.write(message["content"])

        else:

            with st.chat_message("assistant"):
                st.write(message["content"])


# =========================
# RICO
# =========================

with rico_col:

    st.markdown(
        """
        <div class="rico-box">
            <div class="rico-face">🤖</div>
            <h2>Rico</h2>
            <p>مساعدك الذكي</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("🟢 Rico يعمل")

    st.info("🧠 الذكاء الاصطناعي متصل")

    st.info("⌨️ الكتابة جاهزة")


# =========================
# INPUT
# =========================

question = st.chat_input(
    "اكتب رسالتك لريكو..."
)


# =========================
# AI
# =========================

if question:

    question = question.strip()

    if question:

        history = st.session_state.messages.copy()

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.spinner("🤖 Rico يفكر..."):

            answer = ask_ai(
                question,
                history
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": str(answer)
        })

        st.rerun()


# =========================
# SAVE CHAT
# =========================

if st.session_state.messages:

    st.divider()

    if st.button(
        "💾 حفظ المحادثة",
        use_container_width=True
    ):

        st.session_state.saved_chats.append(
            st.session_state.messages.copy()
        )

        st.success("✅ تم حفظ المحادثة")
