import streamlit as st
from streamlit.components.v1 import components
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("firestore-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

app = firebase_admin.get_app()
db = firestore.client(app)

if 'todo_list' not in st.session_state:
    tasks = []
    posts_ref = db.collection(u'tasks')
    for doc in posts_ref.stream():
        task = doc.to_dict()
        tasks.append(task['task'])
    st.session_state.todo_list = tasks
else:
    tasks = st.session_state.todo_list

if 'counter' not in st.session_state:
    st.session_state['counter'] = 0


def submit():
    task = st.session_state["task"]
    if task:
        tasks.append(task)
        doc_ref = db.collection(u'tasks').document()
        # format the task date and task time as a datetime object
        due_date = f'{task_date} {task_time}'
        doc_ref.set({"task": task, "due_date": due_date, "priority": task_priority})
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