import streamlit as st
from datetime import datetime, timedelta
from utils import save_data

st.title("⏱️ Pomodoro Timer")

# --- User settings ---
work_minutes = st.number_input("Work duration (minutes)", 10, 120, 25)
break_minutes = st.number_input("Break duration (minutes)", 1, 60, 5)

# --- Session state initialisation ---
if 'pomodoro_running' not in st.session_state:
    st.session_state.pomodoro_running = False
    st.session_state.pomodoro_start = None
    st.session_state.pomodoro_mode = 'Work'  # or 'Break'

def start_timer():
    st.session_state.pomodoro_running = True
    st.session_state.pomodoro_start = datetime.now()
    st.session_state.pomodoro_mode = 'Work'

def stop_timer():
    st.session_state.pomodoro_running = False
    st.session_state.pomodoro_start = None

# --- Buttons ---
col1, col2 = st.columns(2)
if col1.button("Start" if not st.session_state.pomodoro_running else "Restart"):
    start_timer()
if col2.button("Stop"):
    stop_timer()

# --- Timer display ---
if st.session_state.pomodoro_running and st.session_state.pomodoro_start:
    elapsed = (datetime.now() - st.session_state.pomodoro_start).total_seconds()
    target = work_minutes * 60 if st.session_state.pomodoro_mode == 'Work' else break_minutes * 60
    remaining = max(0, target - elapsed)
    mins, secs = divmod(int(remaining), 60)
    st.header(f"{st.session_state.pomodoro_mode} — {mins:02d}:{secs:02d}")
    if remaining == 0:
        # switch mode
        st.session_state.pomodoro_mode = 'Break' if st.session_state.pomodoro_mode == 'Work' else 'Work'
        st.session_state.pomodoro_start = datetime.now()

# --- History table ---
if 'pomodoro_history' not in st.session_state:
    st.session_state.pomodoro_history = []

st.subheader("Session History")
st.table(st.session_state.pomodoro_history)

# --- Persist history ---
save_data(st.session_state.pomodoro_history, "pomodoro_history.json")
