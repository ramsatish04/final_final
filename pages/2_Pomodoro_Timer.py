import streamlit as st
import time
from datetime import datetime
from utils import save_data

st.title("⏱️ Pomodoro Timer")

# --- User settings ---
work_minutes = st.number_input("Work duration (minutes)", 10, 120, 25)
break_minutes = st.number_input("Break duration (minutes)", 1, 60, 5)

# --- Session state initialization ---
if 'pomodoro_running' not in st.session_state:
    st.session_state.pomodoro_running = False
    st.session_state.pomodoro_start = None
    st.session_state.pomodoro_mode = 'Work'

if 'pomodoro_history' not in st.session_state:
    st.session_state.pomodoro_history = []

# --- Timer control functions ---
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

    # Display current mode
    if st.session_state.pomodoro_mode == 'Work':
        st.success("🔨 Work Time!")
    else:
        st.info("☕ Break Time!")

    # Session complete
    if remaining == 0:
        session_end = datetime.now()
        session_start = st.session_state.pomodoro_start
        mode = st.session_state.pomodoro_mode
        duration = (session_end - session_start).seconds // 60

        # Add to history
        st.session_state.pomodoro_history.append({
            "Mode": mode,
            "Started At": session_start.strftime("%H:%M:%S"),
            "Ended At": session_end.strftime("%H:%M:%S"),
            "Duration (min)": duration
        })

        # Switch mode
        st.session_state.pomodoro_mode = 'Break' if mode == 'Work' else 'Work'
        st.session_state.pomodoro_start = datetime.now()

    # Refresh every second
    time.sleep(1)
    st.experimental_rerun()

# --- History Table ---
st.subheader("Session History")
if st.session_state.pomodoro_history:
    st.table(st.session_state.pomodoro_history)
else:
    st.info("No completed sessions yet.")

# --- Save history to file ---
save_data(st.session_state.pomodoro_history, "pomodoro_history.json")
