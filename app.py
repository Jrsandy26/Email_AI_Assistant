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

st.set_page_config(page_title="Email AI Assistant", layout="centered")

st.title("📧 AI Email Manager")
st.caption("Powered by Qwen 2.5 Coder on NVIDIA NIM")

# Create the three features in tabs
tab1, tab2, tab3 = st.tabs(["New Email", "Smart Reply", "Grammar Fix"])

def call_ai(system_prompt, user_prompt):
    """Helper function to stream response from NVIDIA"""
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

# --- FEATURE 1: WRITER ---
with tab1:
    points = st.text_area("What should the email say?", placeholder="Points: Meeting request, project update...")
    if st.button("Generate"):
        result_placeholder = st.empty()
        full_text = ""
        for chunk in call_ai("You are a professional email writer.", points):
            content = chunk.choices[0].delta.content
            if content:
                full_text += content
                result_placeholder.markdown(full_text)

# --- FEATURE 2: REPLY ---
with tab2:
    received = st.text_area("Paste received email:")
    intent = st.text_input("Your intent (e.g., 'Yes, I'll be there')")
    if st.button("Draft Reply"):
        result_placeholder = st.empty()
        full_text = ""
        prompt = f"Original Email: {received}\nIntent: {intent}"
        for chunk in call_ai("Draft a professional reply to this email based on the intent.", prompt):
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
        for chunk in call_ai("Fix all grammar and spelling. Make it sound professional.", raw_text):
            content = chunk.choices[0].delta.content
            if content:
                full_text += content
                result_placeholder.markdown(full_text)