import streamlit as st
from utils.data_utils import ensure_data_file, load_data, save_data

# -------- Page Config -------- #
st.set_page_config(
    page_title="Life Dashboard",
    page_icon="🌟",
    layout="wide"
)

# -------- Initialise Global Session State -------- #
default_lists = {
    'expenses': [],
    'todos': [],
    'medicines': [],
    'sleep': [],
    'pomodoro_history': []
}

for key, val in default_lists.items():
    if key not in st.session_state:
        st.session_state[key] = load_data(f"{key}.json", val)

# -------- Simple landing content -------- #
st.title("Welcome to Your Life Dashboard ✨")
st.markdown(
    "This home page just sets things up. Use the sidebar to open the individual tracker pages. " 
    "All data you enter is saved locally in **./data/**. Enjoy!")

# -------- Persist session data on every run -------- #
for key in default_lists:
    save_data(st.session_state[key], f"{key}.json")
