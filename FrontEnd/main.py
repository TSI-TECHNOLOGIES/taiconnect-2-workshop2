import os
import json
import time
import base64
import requests
import streamlit as st
from audio import configData
from streamlit_float import *
from audio_handler import speech_to_text, text_to_speech

USER_ICON = "./assert/user_profile.png"
ASSISTANT_ICON = "https://www.octonomy.ai/wp-content/uploads/2025/01/Octonomy_Purple.svg"

st.set_page_config(
    page_title="Octonomy",
    page_icon="https://www.octonomy.ai/wp-content/uploads/2025/01/Octonomy_Purple.svg",
    initial_sidebar_state='auto'
)

float_init()

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        min-width: 200px; /* Change this value to set the desired width */
        max-width: 500px; /* Ensures consistent size */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

st.title("TAI - Healthcare Bot")
chatBotUrl = configData["chatBotURL"]
embeddingUrl = configData["embeddingURL"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "KB_PDF")

with st.sidebar:
    st.image("https://www.octonomy.ai/wp-content/uploads/2025/01/octonomy-Light-Logo-1.svg", width=200)
    st.header("Base config")
    flowOption = st.selectbox('Select the user flow', ('patient'))
    serviceProvider = st.selectbox('Select the service provider', ('groq','openai'))

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today !"}
    ]

# Make use below code snippet to get the user input from the chatbot and append it to the session state messages.
# if prompt := st.chat_input("Your question"):
#     st.session_state.messages.append({"role": "user", "content": prompt})

footer_container = st.container()
footer_container.float("bottom: 0rem;")

with footer_container:
    audio_bytes = st.audio_input("Record a voice message")
    if audio_bytes:
        with st.spinner("Transcribing..."):
            with open(configData['audioInputPath'], "wb") as f:
                f.write(audio_bytes.getbuffer())
            userQuery = speech_to_text(configData['audioInputPath'])
            print("userQuery", userQuery)
            st.session_state.messages.append({"role": "user", "content": userQuery})
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar=(USER_ICON if message["role"] == "user" else ASSISTANT_ICON)
    ):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner("Thinking..."):
            requestData = {
                    "userQuery": userQuery,
                    "userType": flowOption,
                    "provider": serviceProvider,
                    "conversationHistory": st.session_state.messages,
            }
            print(requestData)
            response = requests.post(chatBotUrl, json = requestData).text
        with st.chat_message("assistant", avatar=ASSISTANT_ICON):
            if response:
                with st.spinner("Generating audio response..."):    
                    audio_file = text_to_speech(response, configData['audioOutputPath'])
                    autoplay_audio(audio_file)
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)
