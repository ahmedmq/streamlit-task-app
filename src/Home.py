import datetime

import streamlit as st
from streamlit.components.v1 import components
from firestore_services import (
    save,
    find_all,
    update, delete,
)
from Task import Task

st.set_page_config(page_title='Home', layout='wide')

completed_flag = st.checkbox('Show completed tasks', key='show_completed', value=False)

st.markdown("""
    <style>
    div.stAlert > div:first-child {
        position: absolute;
        bottom: 0;
        right: 0;
        animation: hideDiv 5s forwards;
    }
    @keyframes hideDiv {
      to {
        opacity: 0;
        visibility: hidden;
      }
    }
    </style>
""", unsafe_allow_html=True)


def update_complete(task):
    task.completed = not task.completed
    task.completed_at = datetime.datetime.now()
    update(task)


def display_tasks():
    for i, task in enumerate(tasks):
        check_col, priority_col, due_date_col, action_col = st.columns((0.5, 0.1, 0.3, 0.1))
        with check_col:
            checkbox = st.checkbox(task.title, key=i, value=task.completed, on_change=update_complete, args=(task,))
            # FIXME: only strike through the display tasks and not all checkboxes
            st.markdown("""
                <style>
                    input[aria-checked="true"] + div div[data-testid="stMarkdownContainer"] p {
                    text-decoration: line-through;
                    font-style: italic;
                 }
                </style>    
            """, unsafe_allow_html=True)
        with priority_col:
            if checkbox:
                st.markdown(
                    f"""{'~~_**:red[High]**_~~' if task.priority == 'High' else '~~_**:orange[Medium]**_~~' if task.priority == 'Medium' else '~~_**:green[Low]**_~~'}""",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""{'**:red[High]**' if task.priority == 'High' else '**:orange[Medium]**' if task.priority == 'Medium' else '**:green[Low]**'}""",
                    unsafe_allow_html=True)
        with due_date_col:
            if checkbox:
                st.markdown(
                    f"""~~_{task.due_date}_~~""",
                    unsafe_allow_html=True)
            else:
                st.markdown(f"""{task.due_date}""", unsafe_allow_html=True)
        with action_col:
            st.button("❌", key=task.id, on_click=delete, args=(task,))


if completed_flag:
    tasks = find_all({'deleted_flag': False})
else:
    tasks = find_all({'completed': False, 'deleted_flag': False})
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0


def submit():
    task = st.session_state["title"]
    if task:
        due_date = f'{new_task_date} {new_task_time}'
        save(Task(None, task, "Home", new_task_priority, False, due_date))
        tasks.append(task)
        st.session_state["title"] = ""


# TODO: Make this textbox a form and bigger?
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
