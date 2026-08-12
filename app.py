import streamlit as st
from datetime import datetime

from assistant import process_command


# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="Rico AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# الذاكرة
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "مساعد عام"

if "character" not in st.session_state:
    st.session_state.character = "🤖"

if "status" not in st.session_state:
    st.session_state.status = "جاهز"


# =========================================================
# الشخصيات
# =========================================================

CHARACTERS = {
    "مساعد عام": "🤖",
    "طبيب": "👨‍⚕️",
    "معلم": "👨‍🏫",
    "مبرمج": "👨‍💻",
    "Gamer": "🎮",
    "باحث": "🔎",
}


# =========================================================
# تحديد شخصية ريكو
# =========================================================

def detect_mode(text):

    text = text.lower()

    if any(x in text for x in [
        "مرض", "دواء", "طبيب", "صحة",
        "اعراض", "أعراض", "علاج"
    ]):
        return "طبيب"

    if any(x in text for x in [
        "درس", "دراسة", "رياضيات",
        "فيزياء", "كيمياء", "واجب",
        "تمرين", "اشرح", "شرح"
    ]):
        return "معلم"

    if any(x in text for x in [
        "برمجة", "كود", "بايثون",
        "python", "programming"
    ]):
        return "مبرمج"

    if any(x in text for x in [
        "لعبة", "العاب", "ألعاب",
        "ماينكرافت", "minecraft",
        "fifa", "لعب"
    ]):
        return "Gamer"

    if any(x in text for x in [
        "ابحث", "بحث", "جوجل",
        "google", "يوتيوب", "youtube"
    ]):
        return "باحث"

    return "مساعد عام"


# =========================================================
# معالجة الرسالة
# =========================================================

def send_message(text):

    if not text:
        return

    text = text.strip()

    if not text:
        return

    # تغيير شخصية ريكو
    mode = detect_mode(text)

    st.session_state.mode = mode
    st.session_state.character = CHARACTERS[mode]

    # المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": text
    })

    # حالة ريكو
    st.session_state.status = "يفكر..."

    # معالجة الأمر / الذكاء الاصطناعي
    answer = process_command(text)

    if not answer:
        answer = "ما قدرتش نفهم الطلب."

    # جواب ريكو
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.session_state.status = "جاهز"


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
    background: #070c12 !important;
}

.stApp {
    background:
        radial-gradient(
            circle at 75% 40%,
            rgba(0,140,255,.09),
            transparent 32%
        ),
        #070c12;

    color: white;
}

.block-container {
    max-width: 1280px;
    padding-top: 18px;
    padding-bottom: 60px;
}


/* =========================
   Sidebar
========================= */

section[data-testid="stSidebar"] {
    background: #080f17;
    border-right: 1px solid #1c2a37;
}

.logo {
    text-align: center;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 20px;
}

.side-line {
    height: 1px;
    background: #1d2935;
    margin: 16px 0;
}

.side-title {
    color: #728193;
    text-align: center;
    font-size: 10px;
    margin-bottom: 8px;
}

.side-current {
    background: #102b45;
    border: 1px solid #1d527c;
    border-radius: 9px;
    padding: 10px;
    text-align: center;
    font-size: 11px;
    margin-bottom: 8px;
}

.stButton > button {
    width: 100%;
    border-radius: 9px;
    background: #0e1823;
    border: 1px solid #263746;
    color: #dce6ef;
}

.stButton > button:hover {
    background: #122437;
    border-color: #149cff;
}


/* =========================
   Header
========================= */

.welcome {
    font-size: 29px;
    font-weight: 800;
}

.subtitle {
    color: #718091;
    font-size: 11px;
    margin-top: 3px;
}


/* =========================
   Cards
========================= */

.top-card {
    background: #0c151f;
    border: 1px solid #223344;
    border-radius: 11px;
    padding: 9px;
    text-align: center;
}

.clock {
    color: #168cff;
    font-size: 18px;
    font-weight: 800;
}

.tiny {
    color: #718092;
    font-size: 9px;
}


/* =========================
   Status
========================= */

.status {
    background: #0d2b20;
    border: 1px solid #15583b;
    border-radius: 10px;
    padding: 10px;
    margin-top: 15px;
    font-size: 11px;
}


/* =========================
   Rico
========================= */

.rico-box {
    background: #09121b;
    border: 1px solid #1d2c3b;
    border-radius: 15px;
    padding: 15px;
}

.rico-header {
    font-size: 13px;
    font-weight: 800;
}

.robot-area {
    display: flex;
    justify-content: center;
    margin: 25px 0 15px;
}

.robot {
    width: 190px;
    height: 190px;
    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 80px;

    background:
        radial-gradient(
            circle,
            #122a40,
            #08141f 60%,
            #040b11
        );

    border: 2px solid #139cff;

    box-shadow:
        0 0 18px rgba(19,156,255,.8),
        0 0 45px rgba(19,156,255,.3);

    animation: glow 2.5s infinite;
}

@keyframes glow {

    0%,100% {
        box-shadow:
            0 0 15px rgba(19,156,255,.6),
            0 0 35px rgba(19,156,255,.25);
    }

    50% {
        box-shadow:
            0 0 30px rgba(19,156,255,1),
            0 0 60px rgba(19,156,255,.4);
    }
}

.rico-name {
    text-align: center;
    font-size: 19px;
    font-weight: 800;
}

.rico-mode {
    text-align: center;
    color: #718092;
    font-size: 10px;
    margin-top: 4px;
}


/* =========================
   Sound waves
========================= */

.waves {
    height: 35px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 3px;
}

.waves span {
    width: 3px;
    background: #139cff;
    border-radius: 10px;
    animation: wave .9s infinite ease-in-out;
}

.waves span:nth-child(1) {
    height: 8px;
}

.waves span:nth-child(2) {
    height: 15px;
    animation-delay: .1s;
}

.waves span:nth-child(3) {
    height: 24px;
    animation-delay: .2s;
}

.waves span:nth-child(4) {
    height: 31px;
    animation-delay: .3s;
}

.waves span:nth-child(5) {
    height: 20px;
    animation-delay: .4s;
}

.waves span:nth-child(6) {
    height: 12px;
    animation-delay: .5s;
}

@keyframes wave {

    0%,100% {
        transform: scaleY(.45);
        opacity: .45;
    }

    50% {
        transform: scaleY(1);
        opacity: 1;
    }
}


/* =========================
   Empty Chat
========================= */

.empty {
    height: 330px;

    display: flex;
    justify-content: center;
    align-items: center;

    color: #465566;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="logo">🤖 RICO AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-line"></div>',
        unsafe_allow_html=True
    )

    if st.button("💬 المحادثة"):
        st.session_state.mode = "مساعد عام"
        st.session_state.character = "🤖"
        st.rerun()

    if st.button("🎓 الدراسة"):
        st.session_state.mode = "معلم"
        st.session_state.character = "👨‍🏫"
        st.rerun()

    if st.button("💻 البرمجة"):
        st.session_state.mode = "مبرمج"
        st.session_state.character = "👨‍💻"
        st.rerun()

    if st.button("🎮 الألعاب"):
        st.session_state.mode = "Gamer"
        st.session_state.character = "🎮"
        st.rerun()

    if st.button("🔎 البحث"):
        st.session_state.mode = "باحث"
        st.session_state.character = "🔎"
        st.rerun()

    if st.button("👨‍⚕️ الطب"):
        st.session_state.mode = "طبيب"
        st.session_state.character = "👨‍⚕️"
        st.rerun()

    st.markdown(
        '<div class="side-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-title">الوضع الحالي</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="side-current">
            {st.session_state.character}
            {st.session_state.mode}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🗑️ مسح المحادثة"):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# Main columns
# =========================================================

left, right = st.columns(
    [2.7, 1],
    gap="large"
)


# =========================================================
# LEFT
# =========================================================

with left:

    c1, c2, c3 = st.columns([4, 1, 1])

    with c1:

        st.markdown(
            """
            <div class="welcome">
                مرحبا 👋 أنا ريكو
            </div>

            <div class="subtitle">
                مساعدك الذكي الشخصي
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        now = datetime.now().strftime("%H:%M")

        st.markdown(
            f"""
            <div class="top-card">
                <div class="clock">{now}</div>
                <div class="tiny">الوقت</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="top-card">
                <div style="font-size:18px;">🟢</div>
                <div class="tiny">Online</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        f"""
        <div class="status">
            ⚡ ريكو: <b>{st.session_state.status}</b>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "### 💬 المحادثة"
    )


    if not st.session_state.messages:

        st.markdown(
            """
            <div class="empty">
                👋 ابدأ محادثتك مع ريكو
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                with st.chat_message(
                    "user",
                    avatar="👤"
                ):
                    st.write(message["content"])

            else:

                with st.chat_message(
                    "assistant",
                    avatar="🤖"
                ):
                    st.write(message["content"])


# =========================================================
# RIGHT
# =========================================================

with right:

    st.markdown(
        '<div class="rico-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="rico-header">🤖 ريكو</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<hr style="border-color:#263440;">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="robot-area">

            <div class="robot">
                {st.session_state.character}
            </div>

        </div>

        <div class="rico-name">
            ريكو
        </div>

        <div class="rico-mode">
            {st.session_state.mode}
        </div>

        <div class="waves">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:#0b141d;
            border:1px solid #1d2c39;
            border-radius:9px;
            padding:10px;
            margin-top:15px;
            font-size:9px;
            color:#8291a0;
            line-height:1.8;
        ">
            🧠 الذكاء الاصطناعي: متصل<br>
            🌐 وضع الويب: جاهز<br>
            🟢 النظام: يعمل
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# Input
# =========================================================

user_input = st.chat_input(
    "اكتب رسالتك لريكو..."
)


if user_input:

    send_message(user_input)

    st.rerun()