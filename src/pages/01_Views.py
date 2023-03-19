import pandas as pd
import streamlit as st
import plotly.express as px


# Create example data
data = {
    "name": ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"],
    "due_date": ["2023-03-20", "2023-03-25", "2023-03-22", "2023-03-27", "2023-03-23"],
    "category": ["Work", "Personal", "Work", "Personal", "Work"],
    "priority": [2, 1, 3, 2, 1]
}

df = pd.DataFrame(data)

df['due_date'] = pd.to_datetime(df['due_date'])
bar_col1, bar_col2 = st.columns(2)

with bar_col1:
    st.write('Check box')
with bar_col2:
    st.bar_chart(df['category'].value_counts())

scatter_col1, scatter_col2 = st.columns(2)
with scatter_col1:
    st.write('Scatter plot')
with scatter_col2:
    fig = px.scatter(df, x='due_date', y='priority')
    st.plotly_chart(fig)

heatmap_col1, heatmap_col2 = st.columns(2)
with heatmap_col1:
    st.write('Heatmap')
with heatmap_col2:
    heatmap_data = df['due_date'].value_counts().rename_axis('due_date').reset_index(name='count')
    heatmap_data = heatmap_data.pivot(index='due_date', columns='count', values='count')
    fig = px.imshow(heatmap_data, labels=dict(x="due_date", y="count", color="count"))
    st.plotly_chart(fig)
