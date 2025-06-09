import streamlit as st
import pandas as pd
from datetime import date, datetime
from utils import load_data
from utils.charts import expenses_pie, sleep_line

st.title("📊 Daily Overview")

# --- Load data ---
expenses = load_data("expenses.json", [])
todos = load_data("todos.json", [])
medicines = load_data("medicines.json", [])
sleep_records = load_data("sleep.json", [])
pomodoros = load_data("pomodoro_history.json", [])

today = date.today().isoformat()

# --- Quick stats ---
daily_expenses = sum(e['amount'] for e in expenses if e['date'] == today)
completed_tasks = sum(1 for t in todos if t['done'])
pending_tasks = len(todos) - completed_tasks
upcoming_meds = [m for m in medicines if m['date'] == today and not m.get('taken')]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Today's Spend", f"₹{daily_expenses:,.2f}")
col2.metric("Tasks Pending", pending_tasks)
col3.metric("Pomodoro Sessions", len(pomodoros))
col4.metric("Meds Remaining", len(upcoming_meds))

# --- Compact charts ---
st.subheader("Expenses Breakdown")
st.plotly_chart(expenses_pie(expenses), use_container_width=True)

st.subheader("Sleep Trend")
st.plotly_chart(sleep_line(sleep_records), use_container_width=True)
