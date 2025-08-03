
import streamlit as st
from chat_engine import run_chat

st.set_page_config(
    page_title="Kastol AI Chatbot",
    layout="wide"
)

run_chat()
