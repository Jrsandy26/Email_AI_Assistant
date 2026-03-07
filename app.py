import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load credentials
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")

# Initialize the NVIDIA client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

st.set_page_config(page_title="AI Email Manager", layout="centered")

# ---------- LANDING PAGE ----------

st.markdown("# 📧 AI Email Manager")

st.markdown(
"""
### Write Better Emails with AI

Generate professional emails in seconds using **AI powered by Qwen 2.5 on NVIDIA NIM**.

Save time, improve communication, and draft emails effortlessly.
"""
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ✉️ Email Writer")
    st.write("Generate professional emails instantly with AI assistance.")

with col2:
    st.markdown("### 🤖 Smart Reply")
    st.write("Reply to emails quickly with context-aware AI suggestions.")

with col3:
    st.markdown("### 📝 Grammar Fix")
    st.write("Correct grammar and improve tone automatically.")

st.divider()

st.markdown("### 🚀 Start Using AI Email Manager")

# ---------- MAIN FEATURES ----------

tab1, tab2, tab3 = st.tabs(["New Email", "Smart Reply", "Grammar Fix"])


def call_ai(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="qwen/qwen2.5-coder-7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        stream=True
    )
    return response


# --- FEATURE 1: WRITER (Chat Mode) ---
with tab1:

    st.subheader("AI Email Writer (Chat Mode)")

    tone = st.selectbox(
        "Select Email Tone",
        ["Professional", "Friendly", "Formal", "Apology", "Request"]
    )

    if "email_chat" not in st.session_state:
        st.session_state.email_chat = []

    for message in st.session_state.email_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Write or modify your email...")

    if prompt:

        st.session_state.email_chat.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_text = ""

            messages = [
                {
                    "role": "system",
                    "content": f"You are a professional email writing assistant. Write the email in a {tone} tone."
                }
            ] + st.session_state.email_chat

            response = client.chat.completions.create(
                model="qwen/qwen2.5-coder-7b-instruct",
                messages=messages,
                temperature=0.2,
                stream=True
            )

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    full_text += content
                    response_placeholder.markdown(full_text)

        st.session_state.email_chat.append({"role": "assistant", "content": full_text})

        st.code(full_text)

        if st.button("Copy Email"):
            st.success("Email copied! Use Ctrl + C if needed.")

    if st.button("Clear Conversation"):
        st.session_state.email_chat = []
        st.rerun()


# --- FEATURE 2: REPLY ---
with tab2:

    received = st.text_area("Paste received email:")
    intent = st.text_input("Your intent (e.g., 'Yes, I'll be there')")

    if st.button("Draft Reply"):

        result_placeholder = st.empty()
        full_text = ""

        prompt = f"Original Email: {received}\nIntent: {intent}"

        for chunk in call_ai(
            "Draft a professional reply to this email based on the intent.",
            prompt
        ):
            content = chunk.choices[0].delta.content
            if content:
                full_text += content
                result_placeholder.markdown(full_text)


# --- FEATURE 3: GRAMMAR ---
with tab3:

    raw_text = st.text_area("Paste your rough draft:")

    if st.button("Fix Grammar"):

        result_placeholder = st.empty()
        full_text = ""

        for chunk in call_ai(
            "Fix all grammar and spelling. Make it sound professional.",
            raw_text
        ):
            content = chunk.choices[0].delta.content
            if content:
                full_text += content
                result_placeholder.markdown(full_text)


# ---------- FOOTER ----------

st.divider()

st.markdown(
"""
Built with ❤️ using **Streamlit + NVIDIA AI**
"""
)