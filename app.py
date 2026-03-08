import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

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
# GLOBAL UI STYLES
# -----------------------------
st.markdown("""
<style>

/* -------- GALAXY BACKGROUND -------- */

.stApp{
background-image:
radial-gradient(rgba(128,128,128,0.2) 1px, transparent 1px),
radial-gradient(rgba(128,128,128,0.2) 1px, transparent 1px);

background-size:50px 50px;
background-position:0 0,25px 25px;
}
/* ===== Animated Generate Button ===== */

.stButton > button {

display:flex;
justify-content:center;
align-items:center;
gap:10px;

width:15em;
height:3.2em;

border-radius:3em;

background:#1C1A1C;

border:none;

font-weight:600;

color:#AAAAAA;

transition:all 450ms ease-in-out;

}

.stButton > button:hover {

background:linear-gradient(0deg,#A47CF3,#683FEA);

box-shadow:
inset 0px 1px 0px rgba(255,255,255,0.4),
inset 0px -4px 0px rgba(0,0,0,0.2),
0px 0px 0px 4px rgba(255,255,255,0.2),
0px 0px 120px #9917FF;

transform:translateY(-2px);

color:white;

}

/* -------- HERO GRADIENT TITLE -------- */

.hero{
padding:60px;
text-align:center;
border-radius:20px;
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
margin-bottom:40px;
}

.hero-title{
font-size:52px;
font-weight:800;

background:linear-gradient(
90deg,
#6e8cff,
#23c55e,
#4d6dff,
#7bdc8d
);

background-size:300%;
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

animation:heroGradient 8s linear infinite;
}

@keyframes heroGradient{
0%{background-position:0%}
100%{background-position:300%}
}

.hero-sub{
color:#dbe7ff;
font-size:20px;
}

/* -------- NAVIGATION -------- */

.stRadio [role="radiogroup"]{

display:flex !important;
flex-direction:row !important;
gap:0 !important;

border-radius:20px;
box-shadow:0 15px 10px rgba(0,0,0,0.25);

width:fit-content;
margin:auto;

border:1px solid rgba(128,128,128,0.2);
}

.stRadio input{
opacity:0;
position:absolute;
}

.stRadio label{

padding:14px 25px !important;

cursor:pointer;

background:linear-gradient(
to bottom,
var(--secondary-background-color),
var(--background-color)
) !important;

transition:0.35s;

font-weight:bold;
color:var(--text-color) !important;

border:none !important;
}

.stRadio label:hover{

box-shadow:
0 0 8px rgba(46,204,113,0.6) inset,
0 6px 18px rgba(39,174,96,0.4),
0 0 18px rgba(22,128,76,0.4) inset;
}

.stRadio div[data-checked="true"] label{

background:linear-gradient(
150deg,
#eafaf1,
#7bdc8d
) !important;

color:#1a934c !important;

box-shadow:
0 0 6px #2ecc71 inset,
0 5px 15px rgba(46,204,113,0.5),
0 0 20px rgba(22,128,76,0.6) inset;

transform:translateY(-1px);
}

/* -------- FEATURE CARD (SQUARE) -------- */

.landing-card{

position:relative;

/* square size */
width:75%;
aspect-ratio:1/1;

padding:28px;

border-radius:24px;

background:var(--secondary-background-color);

border:1px solid rgba(255,255,255,0.08);

overflow:hidden;

display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;

transition:0.4s;

}

/* glow orb */

.landing-card::after{

content:"";

position:absolute;

bottom:-30%;
right:-30%;

width:120px;
height:120px;

background:#23c55e;

filter:blur(70px);

border-radius:50%;

}

/* expanding glow */

.landing-card::before{

content:"";

position:absolute;

bottom:-160%;
left:50%;

transform:translate(-50%,-50%);

width:0;
height:0;

background:#23c55e;

filter:blur(70px);

border-radius:50%;

transition:width 1s,height 1s;

}

.landing-card:hover::before{

bottom:-230%;

width:1000px;
height:1000px;

filter:blur(1px);

}

/* hover lift */

.landing-card:hover{

transform:translateY(-8px);

}
/* -------- PROMPT GLOW -------- */

@keyframes cosmicPulse{

0%{
border-color:#4d6dff;
box-shadow:0 0 6px rgba(77,109,255,0.4);
}

50%{
border-color:#6e8cff;
box-shadow:0 0 18px rgba(110,140,255,0.7);
}

100%{
border-color:#4d6dff;
box-shadow:0 0 6px rgba(77,109,255,0.4);
}
}

[data-testid="stChatInput"]{

border:2px solid #4d6dff !important;

border-radius:12px !important;

animation:cosmicPulse 3s infinite ease-in-out;

padding:6px !important;
}

/* -------- CHAT BORDER -------- */

.chat-box{
border-radius:20px;
padding:15px;

background:
linear-gradient(var(--background-color),var(--background-color)) padding-box,
linear-gradient(135deg,#4d6dff,#23c55e,#6e8cff) border-box;

border:3px solid transparent;
}

/* -------- ICON ANIMATION -------- */

@keyframes userPulse{
0%,100%{transform:scale(1);opacity:0.8;}
50%{transform:scale(1.1);opacity:1;color:#007AFF;}
}

.user-icon{
display:inline-block;
animation:userPulse 2s infinite ease-in-out;
margin-right:6px;
}

@keyframes aiGlow{
0%,100%{text-shadow:0 0 5px #4d6dff;}
50%{text-shadow:0 0 15px #6e8cff;}
}

.ai-icon{
display:inline-block;
animation:aiGlow 3s infinite ease-in-out;
margin-right:6px;
}

/* -------- CURSOR -------- */

.typing-cursor{
animation:blink 1s infinite;
}

@keyframes blink{
0%{opacity:1;}
50%{opacity:0;}
100%{opacity:1;}
}

.signature{
text-align:center;
font-size:12px;
opacity:0.6;
margin-top:6px;
}

/* -------- CHAT BUBBLES -------- */

[data-testid="stChatMessage"]{

background:var(--secondary-background-color);

border:1px solid rgba(128,128,128,0.2);

border-radius:16px;

padding:12px;

margin-bottom:8px;

}

/* hide default avatars */

[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"]{

display:none;

}


</style>
""", unsafe_allow_html=True)

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
nav = st.radio(
"",
["🏠 Home","💬 Star Chat","📩 Cosmic Reply","✨ Nebula Polish"],
horizontal=True
)

# -----------------------------
# AI Call
# -----------------------------
def call_ai(system_prompt, user_prompt):

    try:

        return client.chat.completions.create(
            model="qwen/qwen2.5-coder-7b-instruct",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_prompt}
            ],
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

    st.markdown("""
    <div class="hero">
    <div class="hero-title">Email Wonderland</div>
    <div class="hero-sub">
    AI-powered email writing assistant
    </div>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="landing-card">
        <h3>💬 Star Chat</h3>
        Generate professional emails instantly using AI prompts.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="landing-card">
        <h3>📩 Cosmic Reply</h3>
        Paste received emails and generate AI replies.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="landing-card">
        <h3>✨ Nebula Polish</h3>
        Improve grammar, clarity, and tone of drafts.
        </div>
        """, unsafe_allow_html=True)

# =============================
# STAR CHAT
# =============================

elif nav == "💬 Star Chat":

    from datetime import datetime

    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    if "chat" not in st.session_state:
        st.session_state.chat = []

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

                # GPT-like copy button
                st.code(msg["content"], language="text")

            if msg.get("time"):
                st.caption(msg["time"])

    prompt = st.chat_input("Write an email...")

    if prompt:

        st.session_state.chat.append({
            "role": "user",
            "content": prompt,
            "time": datetime.now().strftime("%H:%M")
        })

        with st.chat_message("assistant"):

            placeholder = st.empty()
            text = ""

            for chunk in call_ai(f"Write a {tone} email", prompt):

                content = chunk.choices[0].delta.content if chunk.choices else None

                if content:
                    text += content
                    placeholder.markdown(
                        f"{text}<span class='typing-cursor'>|</span>",
                        unsafe_allow_html=True
                    )

            placeholder.markdown(text)

        st.session_state.chat.append({
            "role": "assistant",
            "content": text,
            "time": datetime.now().strftime("%H:%M")
        })

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

        for chunk in call_ai(
            f"Write a {tone} reply",
            f"Email:{received}\nIntent:{intent}"
        ):

            content = chunk.choices[0].delta.content if chunk.choices else None

            if content:
                text += content
                placeholder.markdown(text)

        st.session_state.reply_result = text

    if st.session_state.reply_result:

        st.code(st.session_state.reply_result)
           
# =============================
# NEBULA POLISH
# =============================

elif nav == "✨ Nebula Polish":

    draft = st.text_area("Email Draft", height=300)

    if "polish_result" not in st.session_state:
        st.session_state.polish_result = ""

    generate = st.button("✨ Improve Email")

    if generate and draft:

        placeholder = st.empty()
        text = ""

        for chunk in call_ai("Improve grammar and clarity", draft):

            content = chunk.choices[0].delta.content if chunk.choices else None

            if content:
                text += content
                placeholder.markdown(text)

        st.session_state.polish_result = text

    if st.session_state.polish_result:

        st.code(st.session_state.polish_result)

