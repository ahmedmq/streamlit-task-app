import datetime

import pandas as pd
import streamlit as st
import plotly.express as px
from faker import Faker
from streamlit.components.v1 import components
from Firestore_services import (
    save,
    find_all,
    update, delete,
)
from Task import Task

st.set_page_config(page_title='Home', layout='wide')

completed_flag = st.checkbox('Show completed tasks', key='show_completed', value=False)


def generate_fake_data():
    fake = Faker()
    fact_dict = []
    for i in range(100):
        fact_dict.append({
            'id': fake.uuid4(),
            'title': fake.sentence(nb_words=3),
            'project': fake.random_element(elements=('Project 1', 'Project 2', 'Project 3')),
            'priority': fake.random_element(elements=('High', 'Medium', 'Low')),
            'completed': fake.boolean(chance_of_getting_true=50),
            'due_date': fake.date_between(start_date='-1y', end_date='today'),
            'created_at': fake.date_between(start_date='-1y', end_date='today'),
            'completed_at': fake.date_between(start_date='-1y', end_date='today'),
            'deleted_flag': fake.boolean(chance_of_getting_true=2),
            'deleted_at': fake.date_between(start_date='-1y', end_date='today')
        })
    return fact_dict


def update_complete(task):
    task.completed = not task.completed
    task.completed_at = datetime.datetime.now()
    update(task)


def display_tasks():
    for i, task in enumerate(tasks):
        row_spacer, check_col, priority_col, due_date_col, action_col = st.columns((0.02, 0.48, 0.1, 0.3, 0.1))
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
                    f"""{'~~_**:red[High]**_~~' if task.priority == 'High' 
                    else '~~_**:orange[Medium]**_~~' if task.priority == 'Medium' else '~~_**:green[Low]**_~~'}""",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""{'**:red[High]**' if task.priority == 'High'
                    else '**:orange[Medium]**' if task.priority == 'Medium' else '**:green[Low]**'}""",
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
        with st.expander("ℹ️ Details (click to expand)"):
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

with st.expander(" 📈 Visualize your tasks (click to expand)"):
    st.info(
        'Use the below checkbox to generate fake tasks. This is to demonstrate the '
        'functionality of the visualizations.')
    fake_flag = st.checkbox('Use fake data', key='use_fake_data')

    if fake_flag:
        dict_data = generate_fake_data()
    else:
        dict_data = [item.to_dict() for item in find_all({})]

    df = pd.DataFrame(dict_data)

    df['due_date'] = pd.to_datetime(df['due_date'])

    characteristics_dict = {'Project': 'project', 'Priority': 'priority', 'Completed': 'completed'}

    row1_1, row1_spacer2 = st.columns((7.1, .2))
    with row1_1:
        st.subheader('Number of Tasks by Type:')
    row2_1, row2_spacer2, row2_2, row2_spacer3 = st.columns((3.3, .4, 5.4, .2))
    with row2_1:
        st.markdown(
            'Use the below filter to select the attribute you want group and compute the count. A pie chart is '
            'displayed on the right to visualize the results.')
        characteristic_selected = st.selectbox("Which attribute do you want to analyze?",
                                               list(characteristics_dict.keys()), key='attribute_category')
    with row2_2:
        characteristic_df = pd.DataFrame(df[characteristics_dict[characteristic_selected]])
        characteristic_df['Instances'] = ''
        characteristic_count_df = characteristic_df.groupby(characteristics_dict[characteristic_selected]).count()
        fig = px.pie(
            characteristic_count_df,
            values='Instances',
            names=characteristic_count_df.index,
        )
        st.plotly_chart(fig, use_container_width=True)

    row3_1, row3_spacer2 = st.columns((7.1, .2))
    with row3_1:
        st.subheader('Find yours most busy days:')
    row4_1, row4_spacer2, row4_2, row4_spacer3 = st.columns((3.3, .4, 5.4, .2))
    with row4_1:
        st.markdown(
            'Use the below filter to select the attribute you want group and compute the count. A pie chart is '
            'displayed on the right to visualize the results.')
    with row4_2:
        fig = px.scatter(df, x='due_date', y='priority')
        st.plotly_chart(fig)

    row5_1, row5_spacer2 = st.columns((7.1, .2))
    with row5_1:
        st.subheader('See how much time you spend on each task')
    row6_1, row6_spacer2, row6_2, row6_spacer3 = st.columns((3.3, .4, 5.4, .2))
    with row6_1:
        st.markdown(
            'The Gantt chart show a visual representation of tasks and their timelines. It displays tasks as horizontal'
            'bars on a timeline, with their start and end dates indicated. This is useful for seeing how different '
            'tasks relate to each other and identifying potential scheduling conflicts')
    with row6_2:
        gant_df = df[['title', 'created_at', 'completed_at', 'priority']]
        fig = px.timeline(df, x_start='created_at', x_end='completed_at', y='title', color='priority')
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig)
