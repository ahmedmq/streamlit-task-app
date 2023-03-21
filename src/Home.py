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
                    input[aria-checked="true"]:not([aria-label="Show completed tasks"]) + div div[data-testid="stMarkdownContainer"] p {
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
    due_date = f'{new_task_date} {new_task_time}'
    new_task = Task(None, new_task_title, new_task_project, new_task_priority, False, due_date)
    save(new_task)
    tasks.append(new_task)


with st.form(key='new_task_form'):
    row1, row2 = st.columns((9, 1))
    with row1:
        new_task_title = st.text_input("Enter a task: 📝", placeholder="Add Task", key="title")
        with st.expander("ℹ️"):
            row_3, row_4 = st.columns(2)
            with row_3:
                new_task_priority = st.selectbox("Priority: ❗️", ["High", "Medium", "Low"], key="priority")
                new_task_date = st.date_input("Due Date: 📅", key="date")
            with row_4:
                new_task_project = st.text_input("Project: 📁", key="project")
                new_task_time = st.time_input("Due Time: ⏰", key="time")

    with row2:
        submitted = st.form_submit_button("Submit 🚀", use_container_width=True)
        st.markdown("""
            <style>
            div.stButton > button[kind=secondaryFormSubmit] {
               height: 40px;
               margin-top: 32px;
               background-color: green;
            }
            </style>
            """, unsafe_allow_html=True)
        if submitted:
            submit()

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
