import streamlit as st
from app.chatbot import get_response, build_messages
from app.database import db

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background: radial-gradient(circle at top left, #10254F 0%, #0B1A38 45%, #060E20 100%);
    color:white;
}

/* -------- Top Header (Deploy / icons area) -------- */
header[data-testid="stHeader"]{
    background:rgba(6,14,32,0.9);
    backdrop-filter: blur(6px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

header[data-testid="stHeader"] div,
header[data-testid="stHeader"] span{
    background-color:transparent !important;
}

header[data-testid="stHeader"] *{
    color:white !important;
    fill:white !important;
}

header[data-testid="stHeader"] button,
header[data-testid="stHeader"] [role="button"],
header[data-testid="stHeader"] [data-baseweb="button"],
div[data-testid="stToolbar"] button,
div[data-testid="stToolbarActions"] button,
div[data-testid="stStatusWidget"]{
    background:#0F1E42 !important;
    border:1px solid rgba(59,130,246,0.35) !important;
    border-radius:8px !important;
    box-shadow:none !important;
}

header[data-testid="stHeader"] button svg,
header[data-testid="stHeader"] [role="button"] svg,
div[data-testid="stToolbar"] svg,
div[data-testid="stToolbarActions"] svg,
div[data-testid="stStatusWidget"] svg{
    fill:#93C5FD !important;
    color:#93C5FD !important;
}

#MainMenu svg{
    fill:white !important;
}

.stDeployButton button{
    background:linear-gradient(135deg,#3B82F6,#2563EB) !important;
    color:white !important;
    border-radius:8px !important;
    border:none !important;
}

/* -------- Sidebar -------- */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0A1633,#081027);
    border-right:1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] *{
    color:white;
}

section[data-testid="stSidebar"] h1{
    font-size:26px;
    letter-spacing:0.5px;
}

section[data-testid="stSidebar"] h3{
    color:#93C5FD;
    font-weight:600;
    letter-spacing:0.3px;
}

section[data-testid="stSidebar"] hr{
    border-color:rgba(255,255,255,0.1);
}

section[data-testid="stSidebar"] .stMarkdown p{
    background:rgba(255,255,255,0.04);
    padding:8px 12px;
    border-radius:10px;
    margin-bottom:6px;
    font-size:14px;
    border:1px solid rgba(255,255,255,0.05);
}

/* -------- Titles -------- */
h1{
    color:white;
    font-weight:700;
    background: linear-gradient(90deg,#FFFFFF,#93C5FD);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.stCaption, [data-testid="stCaptionContainer"]{
    color:#9CA3AF !important;
}

/* -------- Chat Messages (base bubble look) -------- */
div[data-testid="stChatMessage"]{
    background:rgba(22,36,71,0.85);
    backdrop-filter: blur(4px);
    padding:14px 18px;
    border-radius:16px;
    margin-bottom:14px;
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0 4px 14px rgba(0,0,0,0.25);
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li,
div[data-testid="stChatMessage"] span,
div[data-testid="stChatMessage"] strong,
div[data-testid="stChatMessage"] b,
div[data-testid="stChatMessage"] h1,
div[data-testid="stChatMessage"] h2,
div[data-testid="stChatMessage"] h3,
div[data-testid="stChatMessage"] h4,
div[data-testid="stChatMessage"] h5,
div[data-testid="stChatMessage"] h6,
div[data-testid="stChatMessage"] a{
    color:white !important;
    -webkit-text-fill-color:white !important;
}

div[data-testid="stChatMessage"] h1,
div[data-testid="stChatMessage"] h2,
div[data-testid="stChatMessage"] h3{
    color:#93C5FD !important;
    -webkit-text-fill-color:#93C5FD !important;
    font-weight:700;
}

div[data-testid="stChatMessage"] img,
div[data-testid="stChatMessage"] svg{
    border-radius:50%;
}

/* -------- Tables inside chat messages -------- */
div[data-testid="stChatMessage"] table{
    width:100%;
    border-collapse:collapse;
    margin:10px 0;
}

div[data-testid="stChatMessage"] th,
div[data-testid="stChatMessage"] td{
    color:white !important;
    -webkit-text-fill-color:white !important;
    padding:8px 14px;
    border:1px solid rgba(255,255,255,0.12);
}

div[data-testid="stChatMessage"] thead th{
    color:#93C5FD !important;
    -webkit-text-fill-color:#93C5FD !important;
    background:rgba(59,130,246,0.12) !important;
    font-weight:700;
}

div[data-testid="stChatMessage"] tbody tr:nth-child(odd) td{
    background:rgba(255,255,255,0.03);
}

/* -------- AI (assistant) replies ONLY: white text, green code -------- */
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) li,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) strong,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) b,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) td,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) th{
    color:#FFFFFF !important;
    -webkit-text-fill-color:#FFFFFF !important;
}

div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) code,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) pre,
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) pre code{
    color:#4ADE80 !important;
    -webkit-text-fill-color:#4ADE80 !important;
    background:rgba(74,222,128,0.08) !important;
    border:1px solid rgba(74,222,128,0.25);
    border-radius:8px;
}

div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) code{
    padding:2px 6px;
}

div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) pre{
    padding:12px 14px;
    overflow-x:auto;
}

/* -------- Code block copy button + tooltip (was invisible/white-on-white) -------- */
div[data-testid="stCodeBlock"]{
    position:relative;
}

div[data-testid="stCodeBlock"] button,
button[data-testid="stCodeCopyButton"],
button[title="Copy to clipboard"]{
    background:rgba(15,30,66,0.9) !important;
    border:1px solid rgba(74,222,128,0.4) !important;
    border-radius:8px !important;
    opacity:1 !important;
}

div[data-testid="stCodeBlock"] button svg,
button[data-testid="stCodeCopyButton"] svg,
button[title="Copy to clipboard"] svg{
    fill:#4ADE80 !important;
    color:#4ADE80 !important;
}

div[data-testid="stCodeBlock"] [role="tooltip"],
div[data-baseweb="tooltip"]{
    background:#0F1E42 !important;
    color:white !important;
    border:1px solid rgba(74,222,128,0.3) !important;
    border-radius:8px !important;
}

/* -------- Bottom input area (kills the white wrapper) -------- */
div[data-testid="stBottom"],
div[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer,
div[data-testid="stChatInput"] > div{
    background:transparent !important;
}

div[data-testid="stBottom"] > div{
    background:linear-gradient(180deg, rgba(6,14,32,0) 0%, rgba(6,14,32,0.95) 40%) !important;
}

div[data-testid="stChatInput"]{
    background:#0F1E42;
    border-radius:16px;
    border:1px solid rgba(59,130,246,0.4);
    box-shadow:0 0 20px rgba(59,130,246,0.15);
}

div[data-testid="stChatInput"] textarea{
    color:white !important;
    background:transparent !important;
    caret-color:#3B82F6 !important;
    font-size:15px !important;
}

div[data-testid="stChatInput"] textarea::placeholder{
    color:#6B7A99 !important;
}

div[data-testid="stChatInput"] button{
    background:linear-gradient(135deg,#3B82F6,#2563EB) !important;
    border-radius:12px !important;
}

div[data-testid="stChatInput"] button svg{
    fill:white !important;
}

/* -------- Buttons -------- */
.stButton>button{
    width:100%;
    border-radius:12px;
    background:linear-gradient(135deg,#3B82F6,#2563EB);
    color:white;
    border:none;
    font-weight:600;
    padding:10px 0;
    transition: all 0.2s ease-in-out;
    box-shadow:0 4px 12px rgba(59,130,246,0.3);
}

.stButton>button:hover{
    background:linear-gradient(135deg,#2563EB,#1D4ED8);
    transform: translateY(-1px);
    box-shadow:0 6px 16px rgba(37,99,235,0.4);
}

/* -------- Scrollbar -------- */
::-webkit-scrollbar{
    width:8px;
}
::-webkit-scrollbar-track{
    background:transparent;
}
::-webkit-scrollbar-thumb{
    background:rgba(59,130,246,0.4);
    border-radius:10px;
}

/* -------- Footer Credit -------- */
.footer-credit{
    position:fixed;
    bottom:10px;
    right:18px;
    color:#93C5FD;
    font-size:13px;
    font-weight:500;
    letter-spacing:0.3px;
    background:rgba(15,30,66,0.6);
    padding:5px 14px;
    border-radius:20px;
    border:1px solid rgba(59,130,246,0.3);
    z-index:9999;
    backdrop-filter: blur(6px);
}

</style>

<div class="footer-credit">✨ Crafted by Nagothula Dhanush</div>

<script>
// Fallback fix for the persistent white square in the header toolbar.
// CSS selectors haven't caught it across several attempts, so we
// watch the DOM directly and force-restyle it the moment it appears.
(function () {
    function restyleHeaderSquare() {
        const header = window.parent.document.querySelector('header[data-testid="stHeader"]');
        if (!header) return;

        const all = header.querySelectorAll('*');
        all.forEach(el => {
            const style = window.parent.getComputedStyle(el);
            if (style.backgroundColor === 'rgb(255, 255, 255)' ||
                style.backgroundColor === 'rgba(255, 255, 255, 1)') {
                el.style.setProperty('background-color', '#0F1E42', 'important');
                el.style.setProperty('border', '1px solid rgba(59,130,246,0.35)', 'important');
                el.style.setProperty('border-radius', '8px', 'important');
            }
        });
    }

    const observer = new MutationObserver(restyleHeaderSquare);
    const target = window.parent.document.querySelector('header[data-testid="stHeader"]') || window.parent.document.body;
    observer.observe(target, { childList: true, subtree: true, attributes: true });

    restyleHeaderSquare();
    setInterval(restyleHeaderSquare, 1000);
})();
</script>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🤖 AI Assistant")

st.sidebar.markdown("---")

st.sidebar.subheader("💬 Chat History")

history = db.get_messages()

if history:

    for role, message in history[-15:]:

        if role == "user":
            st.sidebar.write("🧑 " + message[:35])

        else:
            st.sidebar.write("🤖 " + message[:35])

else:

    st.sidebar.write("No history yet.")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear History"):

    db.clear_history()

    st.session_state.messages = []

    st.rerun()

# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 AI Assistant")

st.caption("Powered by Google Gemini")

# -----------------------------
# Load Messages
# -----------------------------
if "messages" not in st.session_state:

    st.session_state.messages = []

    for role, message in db.get_messages():

        st.session_state.messages.append(
            {
                "role": role,
                "content": message
            }
        )

# -----------------------------
# Display Messages
# -----------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    db.save_message("user", prompt)

    with st.chat_message("user"):

        st.markdown(prompt)

    contents = build_messages(st.session_state.messages)

    response = get_response(contents)

    with st.chat_message("assistant"):

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    db.save_message("assistant", response)