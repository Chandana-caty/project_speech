import os
import io
import base64
from gtts import gTTS
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr
load_dotenv(override=True)

api_key = st.secrets["api_key"]
# Initialize the LLM client
client = Groq(api_key=api_key)

# Streamlit app configuration
st.set_page_config(page_title="Speech-to-Speech LLM Bot", layout="centered")

# Title and description
st.title("Speech-to-Speech LLM Bot")
st.write("Speak into your microphone to interact with the LLM and receive a spoken response!")

# Button to start recording
if st.button("Start Recording"):
    st.info("Listening... Please speak into your microphone.")
    
    recognizer = sr.Recognizer()

    try:
        # Use the microphone for live audio input
        with sr.Microphone() as source:
            st.info("Recording... Please wait.")
            audio_data = recognizer.listen(source, timeout=5)  # 5 seconds of listening
            st.success("Recording completed!")

            # Convert speech to text
            user_text = recognizer.recognize_google(audio_data)
            st.subheader("Recognized Speech:")
            st.write(user_text)

            # Send the recognized text to the LLM
            with st.spinner("Generating response..."):
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=[
                        {"role": "user", "content": user_text}
                    ]
                )
                bot_text = response.choices[0].message.content

            # Display the LLM response text
            st.subheader("LLM Response:")
            st.write(bot_text)

            # Convert the LLM response text to speech
            tts = gTTS(bot_text, lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)

            # Save the response audio temporarily for playback
            with open("response.mp3", "wb") as audio_file:
                audio_file.write(audio_fp.read())

            # Add audio playback
            st.subheader("Listen to the Response:")
            audio_bytes = open("response.mp3", "rb").read()
            st.audio(audio_bytes, format="audio/mp3")

    except sr.WaitTimeoutError:
        st.error("No speech detected. Please try again.")
    except sr.UnknownValueError:
        st.error("Sorry, could not recognize your speech. Please try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer
st.write("---")
st.caption("Powered by Groq LLM, gTTS, and SpeechRecognition.")
