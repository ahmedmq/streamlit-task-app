# Streamlit Task Application

This repository contains code for a simple Task management application built 
using [Streamlit](https://streamlit.io/) and [Cloud Firestore](https://firebase.google.com/products/firestore). The goal is to understand how to build a simple application using Streamlit, visualize the data and how to store data in Cloud Firestore.

## Overview

This app allows user to create and complete tasks. It uses Cloud Firestore to store the tasks and Streamlit is used to build the frontend UI and display basic visualizations.

![Overview](static/overview.png)


## Prerequisites

To run this app, you'll need to have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- Docker 
- Create a new firebase project by following the instructions here

## Running the app

- To run the app, first clone this repository and install the requirements:

    ```bash 
    git clone
    cd streamlit-task-app
    pip install -r requirements.txt
    ```
  
- Run the streamlit app

    ```bash
    streamlit run app.py
    ```

Alternatively if you wanted to build a docker image and run the app in a container, you can do the following:

- Build the docker image:

    ```bash
    docker build -t streamlit-task-app .
    ```
- Run the docker container:

    ```bash
    docker run -p 8501:8501 streamlit-task-app
    ```
  
## Deployment