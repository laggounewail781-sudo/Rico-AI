import streamlit as st
from datetime import datetime

# =========================================================
# Rico AI
# =========================================================

st.set_page_config(
    page_title="Rico AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# AI
# =========================================================

try:
    from assistant import process_command
except Exception:
    process_command = None


# =========================================================
# Session State
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Gamer"

if "character" not in st.session_state:
    st.session_state.character = "🤖"

if "online" not in st.session_state:
    st.session_state.online = True


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background: #050b12;
    color: white;
}

/* =========================
   MAIN CONTAINER
   ========================= */

.block-container {
    max-width: 1400px;
    padding-top: 35px !important;
    padding-bottom: 25px !important;
}

/* =========================
   SIDEBAR
   ========================= */

section[data-testid="stSidebar"] {
    background: #08111a;
    border-right: 1px solid #22313e;
}

section[data-testid="stSidebar"] > div {
    padding-top: 25px;
}

.sidebar-title {
    text-align: center;
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 25px;
}

.sidebar-line {
    height: 1px;
    background: #263541;
    margin: 20px 0;
}

.nav-item {
    background: #101b26;
    border: 1px solid #2a3b4a;
    border-radius: 10px;
    padding: 11px;
    margin: 9px 0;
    text-align: center;
    color: #e8edf2;
    font-size: 15px;
}

.nav-item:hover {
    border-color: #178cff;
    background: #122333;
}

/* =========================
   HEADER
   ========================= */

.rico-title {
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 5px;
}

.rico-subtitle {
    color: #8291a0;
    font-size: 13px;
    margin-bottom: 20px;
}

/* =========================
   STATUS
   ========================= */

.status-box {
    background: #083622;
    border: 1px solid #0c6d43;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 20px;
    color: #d7fff0;
}

/* =========================
   CHAT
   ========================= */

.chat-title {
    font-size: 25px;
    font-weight: bold;
    margin-bottom: 15px;
}

.chat-area {
    min-height: 430px;
    max-height: 430px;
    overflow-y: auto;
    padding: 10px;
    background: #071019;
    border-radius: 12px;
    border: 1px solid #182936;
}

.user-message {
    background: #123c66;
    border: 1px solid #1b6aa5;
    padding: 12px 15px;
    border-radius: 12px;
    margin: 10px 0 10px auto;
    max-width: 75%;
    text-align: right;
}

.ai-message {
    background: #121c26;
    border: 1px solid #243544;
    padding: 12px 15px;
    border-radius: 12px;
    margin: 10px auto 10px 0;
    max-width: 75%;
}

/* =========================
   RICO PANEL
   ========================= */

.rico-panel {
    background: #08111a;
    border: 1px solid #223542;
    border-radius: 15px;
    padding: 20px;
    min-height: 540px;
    text-align: center;
}

.rico-panel-title {
    font-size: 20px;
    font-weight: bold;
    text-align: right;
}

.robot-circle {
    width: 210px;
    height: 210px;
    border-radius: 50%;
    margin: 35px auto 25px auto;

    border: 2px solid #149cff;

    box-shadow:
        0 0 15px #149cff,
        0 0 35px rgba(20,156,255,0.35);

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle,
            #182938 0%,
            #071019 65%,
            #050b12 100%
        );
}

.robot-face {
    font-size: 105px;
}

.robot-name {
    font-size: 25px;
    font-weight: bold;
    margin-top: 10px;
}

.robot-mode {
    color: #8d9aa7;
    margin-top: 8px;
}

.wave {
    margin: 20px auto;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;
    height: 30px;
}

.wave span {
    display: block;
    width: 4px;
    background: #0c9cff;
    border-radius: 5px;
}

.wave span:nth-child(1) { height: 10px; }
.wave span:nth-child(2) { height: 20px; }
.wave span:nth-child(3) { height: 30px; }
.wave span:nth-child(4) { height: 18px; }
.wave span:nth-child(5) { height: 27px; }
.wave span:nth-child(6) { height: 12px; }

.system-info {
    background: #0b151e;
    border: 1px solid #20313e;
    border-radius: 10px;
    padding: 12px;
    text-align: right;
    color: #8999a8;
    font-size: 12px;
    line-height: 2;
}

/* =========================
   INPUT
   ========================= */

div[data-testid="stChatInput"] {
    margin-top: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🤖 RICO AI</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-line"></div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="nav-item">🏠 الرئيسية</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">💬 المحادثة</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🎓 الدراسة</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">💻 البرمجة</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🎮 الألعاب</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🔎 البحث</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-item">🧑‍🏫 العلم</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-line"></div>',
                unsafe_allow_html=True)

    st.caption("الوضع الحالي")

    st.success("🤖 مساعد ذكي")

    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns(
    [3.3, 1.25],
    gap="large"
)


# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.markdown(
        '<div class="rico-title">مرحبا 👋 أنا ريكو</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="rico-subtitle">مساعدك الذكي الشخصي</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status-box">⚡ الحالة: جاهز</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="chat-title">💬 المحادثة</div>',
        unsafe_allow_html=True
    )

    # -------------------------
    # Messages
    # -------------------------

    if not st.session_state.messages:

        st.markdown(
            """
            <div style="
                height:380px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#637383;
                font-size:14px;
            ">
                👋 ابدأ محادثتك مع ريكو
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for msg in st.session_state.messages:

            if msg["role"] == "user":

                st.markdown(
                    f"""
                    <div class="user-message">
                        👤 {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="ai-message">
                        🤖 {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# RIGHT SIDE - RICO
# =========================================================

with right:

    st.markdown(
        f"""
        <div class="rico-panel">

            <div class="rico-panel-title">
                🤖 ريكو
            </div>

            <div class="robot-circle">
                <div class="robot-face">
                    {st.session_state.character}
                </div>
            </div>

            <div class="robot-name">
                ريكو
            </div>

            <div class="robot-mode">
                الوضع: {st.session_state.mode}
            </div>

            <div class="wave">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>

            <div class="system-info">
                🧠 الذكاء الاصطناعي: متصل<br>
                🌐 وضع الويب: جاهز<br>
                🟢 النظام: يعمل
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "اكتب رسالتك لريكو..."
)


# =========================================================
# PROCESS MESSAGE
# =========================================================

if question:

    question = question.strip()

    if question:

        # إضافة رسالة المستخدم
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # -------------------------
        # Rico AI
        # -------------------------

        answer = None

        try:

            if process_command is not None:

                answer = process_command(question)

            else:

                answer = (
                    "⚠️ ما قدرتش نحمّل نظام ريكو."
                )

        except Exception as e:

            answer = f"❌ حدث خطأ: {e}"

        if answer is None:
            answer = "🤖 ريكو ما قدرش يجاوب حالياً."

        answer = str(answer)

        # إضافة الإجابة
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()
