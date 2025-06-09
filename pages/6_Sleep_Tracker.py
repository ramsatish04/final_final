import streamlit as st
from datetime import date, datetime, timedelta
from utils import load_data, save_data
from utils.charts import sleep_line

st.title("🛌 Sleep Tracker")

if 'sleep' not in st.session_state:
    st.session_state.sleep = load_data("sleep.json", [])

# --- Record sleep ---
st.subheader("Record Sleep")
with st.form("sleep_form", clear_on_submit=True):
    sleep_date = st.date_input("Date", date.today())
    bed_time = st.time_input("Bed Time")
    wake_time = st.time_input("Wake Time")
    submitted = st.form_submit_button("Save")

if submitted:
    bed_dt = datetime.combine(sleep_date, bed_time)
    wake_dt = datetime.combine(sleep_date + timedelta(days=1 if wake_time < bed_time else 0), wake_time)
    hours = round((wake_dt - bed_dt).total_seconds() / 3600, 2)
    st.session_state.sleep.append({
        "date": sleep_date.isoformat(),
        "hours": hours
    })
    save_data(st.session_state.sleep, "sleep.json")
    st.success(f"Recorded {hours} hrs of sleep.")

# --- Display ---
st.subheader("Last 7 Entries")
if st.session_state.sleep:
    st.dataframe(st.session_state.sleep[-7:])
    st.plotly_chart(sleep_line(st.session_state.sleep), use_container_width=True)
else:
    st.info("No sleep data yet.")
