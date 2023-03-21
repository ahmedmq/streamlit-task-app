import streamlit as st
from streamlit.components.v1 import components
from firestore_services import (
    save,
    find_all,
    update, delete,
)
from Task import Task

# st.set_page_config(page_title='Home', layout='wide')


def update_complete(task):
    task.completed = not task.completed
    update(task)


def display_tasks():
    for i, task in enumerate(tasks):
        check_col, priority_col, due_date_col, action_col = st.columns((0.5, 0.2, 0.2, 0.1))
        with check_col:
            checkbox = st.checkbox(task.title, key=i, value=task.completed, on_change=update_complete, args=(task,))
            st.markdown("""
                <style>
                    input[aria-checked="true"] + div div[data-testid="stMarkdownContainer"] p {
                    text-decoration: line-through;
                    font-style: italic;
                 }
                </style>    
            """, unsafe_allow_html=True)
        with priority_col:
            st.write(task.priority)
        with due_date_col:
            st.write(task.due_date)
        with action_col:
            st.button("❌", key=task.id, on_click=delete, args=(task,))


tasks = find_all()
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0


def submit():
    task = st.session_state["title"]
    if task:
        due_date = f'{new_task_date} {new_task_time}'
        save(Task(None, task, "Home", new_task_priority, False, due_date))
        tasks.append(task)
        st.session_state["title"] = ""


st.text_input("Enter a task: 🚀", placeholder="Add Task", key="title", on_change=submit)
with st.expander("ℹ️"):
    date_col, time_col = st.columns(2)
    with date_col:
        new_task_date = st.date_input("Due Date: 📅", key="date")
    with time_col:
        new_task_time = st.time_input("Due Time: ⏰", key="time")
    new_task_priority = st.selectbox("Priority: ❗️", ["High", "Medium", "Low"], key="priority")

display_tasks()

# Hack to focus on the text input
st.components.v1.html(
    f"""
        <script>
            var input = window.parent.document.querySelectorAll("input[type=text]");

            for (var i = 0; i < input.length; ++i) {{
                input[i].focus();
            }}
        </script>
    """,
    height=1
)
