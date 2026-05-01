import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Channel Coach",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
# 🎬 Channel Coach
### Your AI assistant for YouTube & TikTok growth

Create better titles, descriptions, comment replies, and content ideas faster.
""")

st.divider()

# Sidebar
st.sidebar.title("⚙️ Creator Settings")

niche = st.sidebar.text_input("Channel niche", "Gaming")
platform = st.sidebar.selectbox("Platform", ["YouTube", "TikTok", "Both"])
tone = st.sidebar.selectbox(
    "Tone",
    ["Casual", "Professional", "Funny", "Bold", "Friendly"]
)

if st.sidebar.button("💾 Save My Channel"):
    st.session_state.saved_niche = niche
    st.session_state.saved_platform = platform
    st.session_state.saved_tone = tone
    st.sidebar.success("Channel settings saved!")

st.sidebar.divider()
st.sidebar.caption("Built by Nikki | Channel Coach v1")

# Intro card
st.info(
    f"Currently helping with **{st.session_state.get('saved_niche', niche)}** content "
    f"for **{st.session_state.get('saved_platform', platform)}** in a "
    f"**{st.session_state.get('saved_tone', tone)}** tone."
)

# Buttons
st.subheader("🚀 Quick Tools")

col1, col2 = st.columns(2)

user_input = None

with col1:
    if st.button("🎬 Generate Titles", use_container_width=True):
        user_input = "Give me 5 strong video title ideas."

    if st.button("💬 Reply to Comment", use_container_width=True):
        user_input = "Help me write a friendly reply to this comment: "

with col2:
    if st.button("📝 Write Description", use_container_width=True):
        user_input = "Write a YouTube description with hashtags."

    if st.button("⚡ Shorts Ideas", use_container_width=True):
        user_input = "Give me 5 short-form video ideas."

st.divider()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_input = st.chat_input("Ask Channel Coach anything...")

if chat_input:
    user_input = chat_input

# Run chatbot
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    full_prompt = f"""
You are Channel Coach, a helpful AI content strategist for creators.

Creator profile:
Niche: {st.session_state.get("saved_niche", niche)}
Platform: {st.session_state.get("saved_platform", platform)}
Tone: {st.session_state.get("saved_tone", tone)}

Give practical, specific, creator-friendly advice.
Avoid being too generic.
When helpful, provide examples.

User request: {user_input}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=full_prompt
    )

    reply = response.output_text
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat
st.subheader("💬 Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])