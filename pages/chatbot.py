import openai
from openai import OpenAI
import streamlit as st
from scripts.gpt import answer

from dotenv import load_dotenv
import os

load_dotenv()


openai_api_key = str(os.getenv('open_api_key'))

with st.sidebar:
    openai.api_key = openai_api_key


history = st.session_state.get('history', [{"role": "assistant", "content": "Halo, apa yang bisa saya bantu?"}])
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")


for msg in history:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    user_chat = {"role": "user", "content": prompt}
    st.chat_message("user").write(prompt)

    history.append(user_chat)
    msg = answer(history)

    ai_answer = {"role": "assistant", "content": msg}
    st.chat_message("assistant").write(msg)

    history.append(ai_answer)

    st.session_state['history'] = history