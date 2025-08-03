import io
from gtts import gTTS
import streamlit as st
from groq import Groq

# API Key
api_key = st.secrets["api_key"]
client = Groq(api_key=api_key)

# UI Setup
st.set_page_config(page_title="Chandana Caty's AI Assistant", layout="centered")
st.title("Chandana Caty's AI Assistant 🤖💬")
st.write("Ask me anything, and I’ll reply as your personal assistant with a voice!")

# Input
user_text = st.text_input("Enter your message:")

if user_text:
    with st.spinner("Thinking..."):
        try:
            # LLM call with personality
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Chandana Caty's helpful AI assistant. Always respond in a friendly and professional tone. Keep answers clear and supportive, like a personal companion who can talk and listen."
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            )
            bot_text = response.choices[0].message.content

            # Display text
            st.subheader("Assistant Says:")
            st.write(bot_text)

            # Text to Speech
            tts = gTTS(bot_text, lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            # Play response
            st.subheader("Listen to the Response:")
            st.audio(audio_fp.read(), format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.write("---")
st.caption("✨ Powered by Groq LLM and gTTS | Your Assistant – Chandana Caty")
