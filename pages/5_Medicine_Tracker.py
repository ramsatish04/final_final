import streamlit as st
from datetime import date, datetime
from utils import load_data, save_data

st.title("💊 Medicine Tracker")

if 'medicines' not in st.session_state:
    st.session_state.medicines = load_data("medicines.json", [])

with st.form("add_med"):
    name = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage (e.g., 500mg)")
    time_of_day = st.selectbox("Time", ["Morning", "Afternoon", "Evening", "Night"])
    meal = st.selectbox("Meal", ["Before Meal", "After Meal"])
    date_input = st.date_input("Date", date.today())
    submitted = st.form_submit_button("Add")

if submitted and name:
    st.session_state.medicines.append({
        "name": name,
        "dosage": dosage,
        "time": time_of_day,
        "meal": meal,
        "date": date_input.isoformat(),
        "taken": False
    })
    save_data(st.session_state.medicines, "medicines.json")
    st.success("Medicine logged.")

# --- Upcoming reminders ---
today = date.today().isoformat()
upcoming = [m for m in st.session_state.medicines if m['date'] == today and not m['taken']]
st.subheader("Today's Pending Doses")
for med in upcoming:
    st.info(f"{med['time']} — {med['name']} {med['dosage']} ({med['meal']})")
    if st.button("Mark Taken", key=f"take_{med['name']}_{med['time']}"):
        med['taken'] = True
        save_data(st.session_state.medicines, "medicines.json")
        st.experimental_rerun()

# --- History ---
st.subheader("All Records")
if st.session_state.medicines:
    st.dataframe(st.session_state.medicines)
