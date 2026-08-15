import streamlit as st
from datetime import datetime
import urllib.request

from ai_chat import ask_ai


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Rico AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = []

if "chat_name" not in st.session_state:
    st.session_state.chat_name = "محادثة جديدة"


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 75% 25%,
            rgba(20,120,255,.08),
            transparent 35%
        ),
        #050b12;
    color: white;
}

.block-container {
    max-width: 1450px;
    padding-top: 28px !important;
    padding-bottom: 30px !important;
}

section[data-testid="stSidebar"] {
    background: #071019;
    border-right: 1px solid #1b2a36;
}

.rico-card {
    background: #08121c;
    border: 1px solid #203746;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    min-height: 570px;
}

.rico-face {
    width: 210px;
    height: 210px;
    margin: 35px auto 20px auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle,
            #172b3b 0%,
            #08121c 65%,
            #050b12 100%
        );

    border: 2px solid #159cff;

    box-shadow:
        0 0 15px rgba(21,156,255,.7),
        0 0 45px rgba(21,156,255,.25);

    font-size: 95px;
}

.status {
    background: #09291c;
    border: 1px solid #12643f;
    border-radius: 10px;
    padding: 10px;
    margin-top: 15px;
}

.info-box {
    background: #0a151f;
    border: 1px solid #203746;
    border-radius: 10px;
    padding: 10px;
    margin: 8px 0;
    text-align: right;
}

.wave {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    height: 35px;
    margin: 15px;
}

.wave span {
    width: 4px;
    border-radius: 5px;
    background: #159cff;
}

.wave span:nth-child(1) {height:10px;}
.wave span:nth-child(2) {height:22px;}
.wave span:nth-child(3) {height:32px;}
.wave span:nth-child(4) {height:18px;}
.wave span:nth-child(5) {height:27px;}
.wave span:nth-child(6) {height:12px;}

.title {
    font-size: 34px;
    font-weight: bold;
}

.subtitle {
    color: #7f909e;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TIME / DATE
# =========================================================

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%d/%m/%Y")


# =========================================================
# WEATHER
# =========================================================

weather_text = "غير متوفر"

try:

    weather_url = "https://wttr.in/Algeria?format=%C+%t"

    weather_text = urllib.request.urlopen(
        weather_url,
        timeout=5
    ).read().decode("utf-8")

except Exception:

    weather_text = "🌤️ غير متوفر حالياً"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "# 🤖 RICO AI"
    )

    st.caption(
        "مساعدك الذكي الشخصي"
    )

    st.divider()

    st.markdown("### 🕐 الوقت")

    st.info(current_time)

    st.markdown("### 📅 التاريخ")

    st.info(current_date)

    st.markdown("### 🌤️ الطقس")

    st.info(weather_text)

    st.divider()

    st.markdown("### 💬 المحادثات")

    if st.session_state.saved_chats:

        for index, chat in enumerate(
            st.session_state.saved_chats
        ):

            if st.button(
                f"💬 محادثة {index + 1}",
                key=f"chat_{index}",
                use_container_width=True
            ):

                st.session_state.messages = chat.copy()
                st.rerun()

    else:

        st.caption(
            "لا توجد محادثات محفوظة."
        )

    st.divider()

    if st.button(
        "➕ محادثة جديدة",
        use_container_width=True
    ):

        if st.session_state.messages:

            st.session_state.saved_chats.append(
                st.session_state.messages.copy()
            )

        st.session_state.messages = []

        st.rerun()

    if st.button(
        "🗑️ مسح المحادثة الحالية",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🤖 Rico AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">مساعدك الذكي — كتابة وصوت وذاكرة محادثة</div>',
    unsafe_allow_html=True
)


# =========================================================
# MAIN COLUMNS
# =========================================================

chat_column, rico_column = st.columns(
    [3, 1],
    gap="large"
)


# =========================================================
# CHAT
# =========================================================

with chat_column:

    st.subheader("💬 المحادثة")

    if not st.session_state.messages:

        st.markdown(
            """
            <div style="
                height:420px;
                display:flex;
                justify-content:center;
                align-items:center;
                color:#657684;
                font-size:18px;
            ">
                👋 مرحباً! ابدأ الكلام مع ريكو
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                with st.chat_message("user"):
                    st.write(message["content"])

            else:

                with st.chat_message("assistant"):
                    st.write(message["content"])


    # =====================================================
    # TEXT INPUT
    # =====================================================

    question = st.chat_input(
        "⌨️ اكتب رسالتك لريكو..."
    )


    if question:

        question = question.strip()

        if question:

            # رسالة المستخدم
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            # تاريخ المحادثة بدون السؤال الحالي
            history = st.session_state.messages[:-1]

            # Rico
            answer = ask_ai(
                question,
                history
            )

            # جواب Rico
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.rerun()


# =========================================================
# RICO
# =========================================================

with rico_column:

    st.markdown(
        """
        <div class="rico-card">

            <div style="
                text-align:right;
                font-size:21px;
                font-weight:bold;
            ">
                🤖 ريكو
            </div>

            <div class="rico-face">
                🤖
            </div>

            <h2>Rico</h2>

            <p style="color:#8291a0;">
                مساعدك الذكي
            </p>

            <div class="wave">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="status">
                🟢 النظام يعمل
            </div>

            <div class="info-box">
                🧠 الذكاء الاصطناعي: متصل
            </div>

            <div class="info-box">
                💬 الكتابة: جاهزة
            </div>

            <div class="info-box">
                🎤 الصوت: جاهز على الجهاز
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SAVE CURRENT CHAT
# =========================================================

if st.session_state.messages:

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 حفظ المحادثة",
            use_container_width=True
        ):

            st.session_state.saved_chats.append(
                st.session_state.messages.copy()
            )

            st.success(
                "✅ تم حفظ المحادثة"
            )

    with col2:

        if st.button(
            "🆕 حفظ وبدء محادثة جديدة",
            use_container_width=True
        ):

            st.session_state.saved_chats.append(
                st.session_state.messages.copy()
            )

            st.session_state.messages = []

            st.rerun()
