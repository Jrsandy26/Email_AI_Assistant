import streamlit as st
import os
import uuid
from database import get_user_id, create_conversation, save_message, load_messages
from openai import OpenAI
from dotenv import load_dotenv

# -----------------------------
#  Session id
# -----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
user_id = get_user_id(st.session_state.session_id)
# -----------------------------
# Conversation Session
# -----------------------------
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation(user_id)
# -----------------------------
# Load CSS File
# -----------------------------
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/style.css")

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    st.error("NVIDIA_API_KEY not found in .env file")
    st.stop()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Email Wonderland",
    page_icon="✨",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🌌 Cosmic Panel")

    tone = st.selectbox(
        "Email Tone",
        ["Professional","Friendly","Formal","Technical"]
    )

    if st.button("Reset Chat"):
        st.session_state.chat = []

    st.divider()

    st.subheader("System Status")
    st.write("AI Model: Qwen 2.5")
    st.write("Inference: NVIDIA AI")
    st.success("System Online")

# -----------------------------
# Title
# -----------------------------
st.title("Email Wonderland")

# -----------------------------
# Navigation
# -----------------------------
nav_options = ["🏠 Home","💬 Star Chat","📩 Cosmic Reply","✨ Nebula Polish"]

# Initialize state
if "nav" not in st.session_state:
    st.session_state.nav = nav_options[0]

# Callback when radio changes
def update_nav():
    st.session_state.nav = st.session_state.nav_radio

# Radio navigation
st.radio(
    "Navigation",
    nav_options,
    horizontal=True,
    label_visibility="collapsed",
    key="nav_radio",
    index=nav_options.index(st.session_state.nav),
    on_change=update_nav
)

nav = st.session_state.nav
# -----------------------------
# AI Call
# -----------------------------
def call_ai(messages):

    try:

        return client.chat.completions.create(
            model="qwen/qwen2.5-coder-7b-instruct",
            messages=messages,   # full conversation history
            temperature=0.2,
            stream=True
        )

    except Exception as e:
        st.error(f"AI Error: {e}")
        return []

# =============================
# HOME
# =============================

if nav == "🏠 Home":

    # Hero Section
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Email Wonderland</div>
        <div class="hero-sub">
        AI-powered email assistant that helps you write, reply, and refine emails instantly.
        Designed for professionals, students, and teams who want faster communication.
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("## 🚀 Powerful AI Email Tools")

    col1, col2, col3 = st.columns(3)

    # Star Chat
    with col1:
        st.markdown("""
        <div class="landing-card">
        <h3>💬 Star Chat</h3>
        <p>
        Describe the email you want to write and the AI will generate a complete,
        structured message in seconds.
        </p>

        <ul>
        <li>Professional formatting</li>
        <li>Smart tone adjustment</li>
        <li>Instant email drafts</li>
        <li>Context-aware writing</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Cosmic Reply
    with col2:
        st.markdown("""
        <div class="landing-card">
        <h3>📩 Cosmic Reply</h3>
        <p>
        Paste an incoming email and describe your response intent.
        The AI will generate a clear, professional reply instantly.
        </p>

        <ul>
        <li>Smart email understanding</li>
        <li>Quick response generation</li>
        <li>Custom reply tone</li>
        <li>Time-saving automation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Nebula Polish
    with col3:
        st.markdown("""
        <div class="landing-card">
        <h3>✨ Nebula Polish</h3>
        <p>
        Improve your existing emails with AI-powered grammar correction
        and clarity enhancement.
        </p>

        <ul>
        <li>Grammar correction</li>
        <li>Professional tone improvement</li>
        <li>Clearer sentence structure</li>
        <li>Readable email formatting</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


    st.divider()

# How It Works
    st.markdown("""
<div class="section-heading">
⚙️ How Email Wonderland Works
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
    <div class="how-card">
    <h3>✍️ Describe Your Email</h3>
    <p>
    Enter a prompt, paste an email, or provide a rough draft.
    The system understands your request and prepares it for AI processing.
    </p>
    </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
    <div class="how-card">
    <h3>🧠 AI Processes Request</h3>
    <p>
    The AI model analyzes tone, context, structure, and intent
    to generate a clear and professional email response.
    </p>
    </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
    <div class="how-card">
    <h3>🚀 Instant Results</h3>
    <p>
    Get a ready-to-send email within seconds,
    helping you communicate faster and more effectively.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

# Who it's for
    st.markdown("""
    <div class="who-heading">
    👥 Who Is This For?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="who-container">

    <div class="who-card">

    <div class="who-title">
    Email Wonderland is perfect for
    </div>

    <div class="who-desc">
    AI-powered assistant designed for anyone who writes emails frequently.
    </div>

    <ul class="who-list">

    <li>
    <span class="who-check">✓</span>
    Professionals writing daily business emails
    </li>

    <li>
    <span class="who-check">✓</span>
    Students contacting professors or recruiters
    </li>

    <li>
    <span class="who-check">✓</span>
    Customer support teams handling large email volumes
    </li>

    <li>
    <span class="who-check">✓</span>
    HR teams responding to candidates
    </li>

    <li>
    <span class="who-check">✓</span>
    Freelancers managing client communication
    </li>
    </ul>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    
# CTA Section
    st.markdown("""
<div class="cta-section">

<div class="cta-title">
Start Writing Smarter Emails
</div>

<div class="cta-sub">
Generate professional emails instantly using AI-powered automation.
Save time, improve communication, and boost productivity.
</div>

<div class="cta-btn-streamlit">
""", unsafe_allow_html=True)

    if st.button("Start Writing Emails →"):
        st.session_state.nav = "💬 Star Chat"
        st.rerun()

    st.markdown("""
</div>

</div>
""", unsafe_allow_html=True)

# Footer
    st.markdown("""
<div class="footer">

<div class="footer-title">
Email Wonderland™
</div>

<p class="footer-desc">
AI-powered email assistant that helps users generate, reply,
and refine emails instantly using intelligent automation.
</p>

<div class="social-container">

<a href="https://github.com/Jrsandy26" target="_blank">

<div class="social-card">

<div class="social-bg"></div>

<div class="social-center">
GitHub
</div>

<div class="social-box social-box1">

<svg viewBox="0 0 24 24">
<path d="M12 .5C5.73.5.5 5.73.5 12a11.5 11.5 0 008 10.94c.59.1.8-.26.8-.57v-2.1c-3.25.71-3.93-1.56-3.93-1.56-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.7.08-.7 1.16.08 1.78 1.2 1.78 1.2 1.03 1.76 2.7 1.25 3.36.95.1-.75.4-1.25.73-1.54-2.6-.3-5.33-1.3-5.33-5.77 0-1.27.45-2.3 1.2-3.12-.12-.3-.52-1.5.11-3.13 0 0 .97-.31 3.18 1.19a10.9 10.9 0 015.8 0c2.21-1.5 3.18-1.19 3.18-1.19.63 1.63.23 2.83.11 3.13.75.82 1.2 1.85 1.2 3.12 0 4.48-2.73 5.47-5.33 5.77.41.35.78 1.05.78 2.12v3.14c0 .31.21.67.81.56A11.5 11.5 0 0023.5 12C23.5 5.73 18.27.5 12 .5z"/>
</svg>

</div>

</div>
</a>
<a href="https://www.linkedin.com/in/sandeepsai26" target="_blank">

<div class="social-card">

<div class="social-bg"></div>

<div class="social-center">
LinkedIn
</div>

<div class="social-box social-box2">

<svg viewBox="0 0 448 512">
<path d="M100.28 448H7.4V148.9h92.88zM53.79 108.1C24.09 108.1 0 83.5 0 53.8A53.79 53.79 0 0153.79 0C83.5 0 108.1 24.09 108.1 53.8s-24.6 54.3-54.31 54.3zM447.9 448h-92.4V302.4c0-34.7-.7-79.3-48.3-79.3-48.3 0-55.7 37.7-55.7 76.7V448h-92.4V148.9h88.7v40.8h1.3c12.4-23.6 42.6-48.3 87.7-48.3 93.8 0 111.1 61.8 111.1 142.3V448z"/>
</svg>

</div>

</div>

</a>

</div>

<br>

<div class="footer-bottom">
© 2026 Email Wonderland™ • Built with Streamlit & NVIDIA AI
</div>

</div>
""", unsafe_allow_html=True)
    
# =============================
# STAR CHAT
# =============================

elif nav == "💬 Star Chat":

    from datetime import datetime

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    if "chat" not in st.session_state:

        messages = load_messages(st.session_state.conversation_id)
        
        st.session_state.chat = [
            {"role": role, "content": content}
            for role, content in messages
        ]

    # Show chat history
    for i, msg in enumerate(st.session_state.chat):

        with st.chat_message(msg["role"]):

            if msg["role"] == "user":

                st.markdown(
                    f"<span class='user-icon'>👤</span> {msg['content']}",
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"<span class='ai-icon'>🤖</span> {msg['content']}",
                    unsafe_allow_html=True
                )

                st.code(msg["content"], language="text")

            if msg.get("time"):
                st.caption(msg["time"])


    prompt = st.chat_input("Write an email...")

    if prompt:

        # Save user message
        st.session_state.chat.append({
            "role": "user",
            "content": prompt,
            "time": datetime.now().strftime("%H:%M")
        })
        
        save_message(
        st.session_state.conversation_id,
        "user",
        prompt
     )

        # -----------------------------
        # Build conversation context
        # -----------------------------

        messages = [
            {
                "role": "system",
                "content": f"""
                You are an AI email assistant.

                Your tasks:
                • Write emails
                • Modify emails
                • Shorten emails
                • Change tone

                Current tone: {tone}
                """
            }
        ]

        # include last 10 messages for context
        history = st.session_state.chat[-10:]

        for msg in history:

            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # -----------------------------
        # Generate AI response
        # -----------------------------

        with st.chat_message("assistant"):

            placeholder = st.empty()
            text = ""

            for chunk in call_ai(messages):

                content = chunk.choices[0].delta.content if chunk.choices else None

                if content:

                    text += content

                    placeholder.markdown(
                        f"{text}<span class='typing-cursor'>|</span>",
                        unsafe_allow_html=True
                    )

            placeholder.markdown(text)

        # Save AI response
        st.session_state.chat.append({
            "role": "assistant",
            "content": text,
            "time": datetime.now().strftime("%H:%M")
        })
        save_message(
            st.session_state.conversation_id,
            "assistant",
            text
        )
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =============================
# COSMIC REPLY
# =============================

elif nav == "📩 Cosmic Reply":

    col1, col2 = st.columns(2)

    with col1:
        received = st.text_area("Received Email", height=250)

    with col2:
        intent = st.text_area("Reply Intent", height=250)

    if "reply_result" not in st.session_state:
        st.session_state.reply_result = ""
        
    if st.button("Generate Reply") and received:

        placeholder = st.empty()
        text = ""

        messages = [
            {
                "role": "system",
                "content": f"""
    You are an AI email assistant.

    Your job is to write a reply email based ONLY on:
    1. The received email
    2. The reply intent given by the user

    Rules:
    - Do NOT invent names, hotels, bookings, or information.
    - Only respond based on the provided email.
    - Follow the requested tone: {tone}
    - Keep the reply professional and relevant.
    """
            },
            {
                "role": "user",
                "content": f"""
    Received Email:
    {received}

    Reply Intent:
    {intent}

    Write the reply email.
    """
            }
        ]

        for chunk in call_ai(messages):

            content = chunk.choices[0].delta.content if chunk.choices else None

            if content:
                text += content
                placeholder.markdown(text)

        st.session_state.reply_result = text

        save_message(
            st.session_state.conversation_id,
            "assistant",
            text
        )

    if st.session_state.reply_result:
        st.code(st.session_state.reply_result)
# =============================
# NEBULA POLISH
# =============================
elif nav == "✨ Nebula Polish":

    draft = st.text_area("Email Draft", height=300)

    if "polish_result" not in st.session_state:
        st.session_state.polish_result = ""

    generate = st.button("✨ Check Grammar")

    if generate and draft:

        # Save user draft
        save_message(
            st.session_state.conversation_id,
            "user",
            f"Polish this email:\n{draft}"
        )

        placeholder = st.empty()
        text = ""

        messages = [
    {
        "role": "system",
        "content": f"""
        You are a grammar correction assistant.

        Your job is ONLY to correct grammar, spelling, and punctuation errors in the email.

        Rules:
        - Do NOT rewrite the email completely
        - Do NOT change meaning
        - Do NOT add new information
        - Only fix grammar and sentence errors
        - Keep the same tone and structure
        """
    },
    {
        "role": "user",
        "content": draft
    }
]
        for chunk in call_ai(messages):

            content = chunk.choices[0].delta.content if chunk.choices else None

            if content:
                text += content
                placeholder.markdown(text)

        st.session_state.polish_result = text

        # Save AI response
        save_message(
            st.session_state.conversation_id,
            "assistant",
            text
        )

    if st.session_state.polish_result:
        st.code(st.session_state.polish_result)