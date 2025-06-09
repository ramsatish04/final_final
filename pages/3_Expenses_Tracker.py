import streamlit as st
import pandas as pd
from utils import load_data, save_data
from utils.charts import expenses_pie
from datetime import date

st.title("💰 Expenses Tracker")

if 'expenses' not in st.session_state:
    st.session_state.expenses = load_data("expenses.json", [])

# --- Add / edit form ---
st.subheader("Add / Edit Expense")
with st.form("expense_form", clear_on_submit=True):
    amount = st.number_input("Amount", min_value=0.0, step=0.5)
    category_list = list({e['category'] for e in st.session_state.expenses})
    new_category = st.text_input("New category (leave blank to use existing)")
    category = st.selectbox("Category", options=category_list) if not new_category else new_category
    date_input = st.date_input("Date", value=date.today())
    description = st.text_input("Description")
    status = st.selectbox("Status", ["Paid", "Unpaid"])
    submitted = st.form_submit_button("Save")

if submitted:
    exp = {
        "amount": amount,
        "category": category,
        "date": date_input.isoformat(),
        "description": description,
        "status": status
    }
    st.session_state.expenses.append(exp)
    save_data(st.session_state.expenses, "expenses.json")
    st.success("Expense saved!")

# --- Display table ---
st.subheader("All Expenses")
df = pd.DataFrame(st.session_state.expenses)
if not df.empty:
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "expenses.csv", mime="text/csv")
    st.plotly_chart(expenses_pie(st.session_state.expenses), use_container_width=True)
else:
    st.info("No expenses recorded yet.")
