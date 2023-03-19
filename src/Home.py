import streamlit as st
from streamlit.components.v1 import components

if 'todo_list' not in st.session_state:
    tasks = []
    st.session_state.todo_list = tasks
else:
    tasks = st.session_state.todo_list

if 'counter' not in st.session_state:
    st.session_state['counter'] = 0


def submit():
    new_task = st.session_state["task"]
    if new_task:
        st.write(f'New task: {new_task} with date: {task_date} and time: {task_time} and priority: {task_priority}')
        tasks.append(new_task)
        st.session_state["task"] = ""


st.text_input("Enter a task: 🚀", placeholder="Add Task", key="task", on_change=submit)
with st.expander("ℹ️"):
    date_col, time_col = st.columns(2)
    with date_col:
        task_date = st.date_input("Due Date: 📅", key="date")
    with time_col:
        task_time = st.time_input("Due Time: ⏰", key="time")
    task_priority = st.selectbox("Priority: ❗️", ["High", "Medium", "Low"], key="priority")

for i, task in enumerate(tasks):
    check_col, priority_col = st.columns(2)
    with check_col:
        checkbox = st.checkbox(task, key=i)
        st.markdown("""
            <style>
                input[aria-checked="true"] + div div[data-testid="stMarkdownContainer"] p {
                text-decoration: line-through;
                font-style: italic;
             }
            </style>    
        """, unsafe_allow_html=True)
    with priority_col:
        st.write(f'Priority: {task_priority}')

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
