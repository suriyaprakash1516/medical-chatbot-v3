"""
MediAssist - Multilingual Medical Support Chatbot
GUVI | HCL Final Project
Author: [Your Name]
Description: A multilingual medical support chatbot using OpenAI GPT and Streamlit.
"""
import streamlit as st
from utils.translator import detect_and_translate, translate_response
from utils.medical_engine import get_medical_response
from utils.session import init_session, save_message, get_chat_history
from utils.helpers import is_emergency, is_non_medical, format_disclaimer

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediAssist – Multilingual Medical Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fb; }
    .header-box {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
        border-radius: 14px;
        padding: 24px 32px;
        color: white;
        margin-bottom: 20px;
    }
    .header-box h1 { font-size: 2rem; margin: 0; font-weight: 700; }
    .header-box p  { margin: 6px 0 0; opacity: 0.88; font-size: 0.95rem; }
    .user-bubble {
        background: #1a73e8;
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(26,115,232,0.18);
    }
    .bot-bubble {
        background: white;
        color: #1a1a2e;
        padding: 14px 20px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 85%;
        font-size: 0.93rem;
        border: 1px solid #e3e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .emergency-box {
        background: #fff3f3;
        border: 2px solid #e53935;
        border-radius: 12px;
        padding: 14px 20px;
        color: #b71c1c;
        font-weight: 600;
        margin: 8px 0;
    }
    .restrict-box {
        background: #f3f4ff;
        border: 2px solid #5c6bc0;
        border-radius: 12px;
        padding: 14px 20px;
        color: #283593;
        font-weight: 600;
        margin: 8px 0;
    }
    .disclaimer-box {
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        font-size: 0.82rem;
        color: #5d4037;
        margin-top: 10px;
    }
    .lang-badge {
        display: inline-block;
        background: #e8f5e9;
        color: #2e7d32;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .sidebar-section {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        border: 1px solid #e3e8f0;
    }
    .sidebar-section h4 { color: #1a73e8; margin: 0 0 10px; font-size: 0.9rem; }
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #c5cae9 !important;
        font-size: 0.95rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 28px;
        font-size: 0.95rem;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }
    div[data-testid="stHorizontalBlock"] { gap: 10px; }
</style>
""", unsafe_allow_html=True)

# ─── Session Initialization ───────────────────────────────────────────────────
init_session()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    st.markdown('<div class="sidebar-section"><h4>🌐 Language</h4>', unsafe_allow_html=True)
    language_mode = st.selectbox(
        "Input language",
        ["Auto-detect", "English", "Tamil (தமிழ்)", "Hindi (हिंदी)",
         "French", "Spanish", "Arabic", "Telugu", "Kannada", "Malayalam"],
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><h4>🩺 Quick Symptom Templates</h4>', unsafe_allow_html=True)
    quick_prompts = {
        "🤒 Fever & Headache": "I have a fever and headache for the past 2 days.",
        "🤧 Cold & Cough": "I have a runny nose, sore throat, and mild cough.",
        "🫀 Chest Pain": "I feel chest pain and shortness of breath.",
        "🤢 Stomach Issues": "I have stomach pain, nausea, and loose stools.",
        "💊 Appointment Help": "How do I book a doctor appointment?",
    }
    for label, prompt in quick_prompts.items():
        if st.button(label, key=f"quick_{label}"):
            st.session_state["prefill_input"] = prompt
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section"><h4>🗑️ Session</h4>', unsafe_allow_html=True)
    if st.button("Clear Chat History"):
        st.session_state["messages"] = []
        st.session_state["prefill_input"] = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-section">
    <h4>📋 About MediAssist</h4>
    <p style="font-size:0.82rem;color:#555;">
    MediAssist provides multilingual medical <b>guidance</b>, not diagnosis.
    Always consult a qualified healthcare professional for medical decisions.
    <br><br>
    🔖 GUVI | HCL Final Project<br>
    🧠 Powered by llama3-70b-8192<br>
    🌐 Supports 10+ languages
    </p>
    </div>
    """, unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🏥 MediAssist — Multilingual Medical Chatbot</h1>
    <p>AI-powered health guidance in your language · Safe · Accurate · 24/7</p>
</div>
""", unsafe_allow_html=True)

# ─── Chat History Display ─────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    history = get_chat_history()
    if not history:
        st.markdown("""
        <div class="bot-bubble">
            👋 Welcome to <b>MediAssist</b>! I'm your multilingual medical support assistant.<br><br>
            You can describe your symptoms in <b>any language</b> — I'll understand and respond
            in the same language.<br><br>
            💡 <i>Try the quick templates in the sidebar, or type your query below.</i>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in history:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>',
                            unsafe_allow_html=True)
            else:
                if msg.get("emergency"):
                    st.markdown(f'<div class="emergency-box">🚨 {msg["content"]}</div>',
                                unsafe_allow_html=True)
                elif msg.get("restricted"):
                    st.markdown(f'<div class="restrict-box">🚫 {msg["content"]}</div>',
                                unsafe_allow_html=True)
                else:
                    lang_badge = f'<span class="lang-badge">🌐 {msg.get("detected_lang", "English")}</span><br>' \
                                 if msg.get("detected_lang") else ""
                    st.markdown(
                        f'<div class="bot-bubble">{lang_badge}🤖 {msg["content"]}</div>',
                        unsafe_allow_html=True
                    )

# ─── Input Section ────────────────────────────────────────────────────────────
st.markdown("---")
prefill = st.session_state.get("prefill_input", "")

user_input = st.text_area(
    "💬 Describe your symptoms or ask a health question (any language):",
    value=prefill,
    height=100,
    placeholder="e.g. I have a headache and fever for 2 days... / எனக்கு தலைவலி இருக்கிறது... / मुझे बुखार है...",
    key="user_text_area"
)

col1, col2 = st.columns([3, 1])
with col1:
    send_clicked = st.button("🚀 Send Message", use_container_width=True)
with col2:
    st.markdown("<br>", unsafe_allow_html=True)

# ─── Process Message ──────────────────────────────────────────────────────────
if send_clicked and user_input.strip():
    st.session_state["prefill_input"] = ""
    user_text = user_input.strip()

    # Save user message
    save_message("user", user_text)

    # ── Non-medical check (fast path — no API needed) ──
    if is_non_medical(user_text):
        restrict_msg = (
            "🏥 I'm <b>MediAssist</b>, a medical support chatbot. "
            "I can only help with health and medical questions.<br><br>"
            "Please ask me about <b>symptoms, medicines, diseases, or health concerns</b>. "
            "I'm not able to answer general knowledge, sports, politics, or other non-medical topics."
        )
        save_message("assistant", restrict_msg, restricted=True)
        st.rerun()

    # ── Emergency check (fast path — no API needed) ──
    if is_emergency(user_text):
        emergency_msg = (
            "🚨 <b>EMERGENCY DETECTED</b> — Your symptoms suggest a potentially serious condition. "
            "Please <b>call emergency services immediately</b>:<br>"
            "🇮🇳 India: <b>108</b> &nbsp;|&nbsp; 🌍 International: <b>911 / 999 / 112</b><br>"
            "Go to the nearest hospital Emergency Room <b>right now</b>. Do not delay."
        )
        save_message("assistant", emergency_msg, emergency=True)
        st.rerun()

    # Language detection & translation
    with st.spinner("🌐 Detecting language & translating..."):
        translated_input, detected_lang, source_lang_code = detect_and_translate(user_text)

    # Medical response generation
    with st.spinner("🩺 Generating medical guidance..."):
        english_response = get_medical_response(
            user_query=translated_input,
            chat_history=get_chat_history(),
        )

    # Translate response back if needed
    with st.spinner("🔄 Translating response..."):
        final_response = translate_response(
            english_response, target_lang=source_lang_code
        )

    # Save bot response
    save_message(
        "assistant",
        final_response,
        detected_lang=detected_lang if source_lang_code != "en" else None
    )

    st.rerun()