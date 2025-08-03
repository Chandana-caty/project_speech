import io
from gtts import gTTS
import streamlit as st
from groq import Groq

# Get API key securely
api_key = st.secrets["api_key"]
client = Groq(api_key=api_key)

# UI setup
st.set_page_config(page_title="Text-to-Speech LLM Bot", layout="centered")
st.title("Text-to-Speech LLM Bot")
st.write("Type a message below to talk with the LLM and hear its voice response!")

# Text input instead of microphone
user_text = st.text_input("Enter your message:")

if user_text:
    with st.spinner("Thinking..."):
        try:
            # Query the LLM
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": user_text}]
            )
            bot_text = response.choices[0].message.content

            # Show response
            st.subheader("LLM Response:")
            st.write(bot_text)

            # Convert to speech
            tts = gTTS(bot_text, lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            # Play audio
            st.subheader("Listen to the Response:")
            st.audio(audio_fp.read(), format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.write("---")
st.caption("Powered by Groq LLM and gTTS.")

