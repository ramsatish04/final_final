import streamlit as st
from utils import load_data, save_data

st.title("✅ To‑Do List")

if 'todos' not in st.session_state:
    st.session_state.todos = load_data("todos.json", [])

# --- Add task ---
new_task = st.text_input("Add a new task")
if st.button("Add") and new_task.strip():
    st.session_state.todos.append({"task": new_task, "done": False})
    save_data(st.session_state.todos, "todos.json")

# --- Filter ---
filter_opt = st.radio("Filter", ["All", "Active", "Completed"], horizontal=True)

# --- Task list ---
def task_filter(item):
    if filter_opt == "Active":
        return not item['done']
    if filter_opt == "Completed":
        return item['done']
    return True

for i, todo in enumerate(st.session_state.todos):
    if task_filter(todo):
        cols = st.columns([0.1, 0.8, 0.1])
        done = cols[0].checkbox("", value=todo['done'], key=f"todo_{i}")
        if done != todo['done']:
            todo['done'] = done
            save_data(st.session_state.todos, "todos.json")
        cols[1].write(todo['task'])
        if cols[2].button("🗑️", key=f"del_{i}"):
            st.session_state.todos.pop(i)
            save_data(st.session_state.todos, "todos.json")
            st.experimental_rerun()
