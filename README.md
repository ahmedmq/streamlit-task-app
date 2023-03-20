# Streamlit Task Application

This repository contains code for a simple Task management application. 

### Tech Stack

1. [Streamlit](https://streamlit.io/) is used to build the frontend UI and display basic visualizations.

2. [Firestore](https://firebase.google.com/products/firestore) is used as the primary database

3. [Docker](https://www.docker.com/) is used to containerize the application

4. [Kubernetes](https://kubernetes.io/) is used to deploy the application

5. [TestContainers](https://github.com/testcontainers/testcontainers-python) is used to run integration tests


## Overview

This app allows a single user to create and complete tasks. The user can also see different visualizations to track progress.
The high-level deployment architecture is depicted below

![Overview](static/overview.png)


## Prerequisites

To run this app, you'll need to have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- Docker & Kubernetes (optional)
- Create a new firebase project by following the instructions [here](https://firebase.google.com/docs/firestore/quickstart)

## Running the app locally

If you would like to run the app locally without docker and kubernetes, you can do the following:

-  Clone this repository:

    ```bash 
    git clone
    cd streamlit-task-app
    ```
  
- Install the requirements and run the streamlit app

    ```bash
    ./run.sh
    ```
The above command should open a browser window and access the app running on http://localhost:8501

## Running the app on Docker

Alternatively if you want to build a docker image and run the app in a container, you can do the following:

- Build the docker image:

    ```bash
    docker build -t streamlit-task-app .
    ```
- Run the docker container:

    ```bash
    docker run -p 8501:8501 streamlit-task-app
    ```
  
Open a browser window and access the app running on http://localhost:8501

## Deploying the app to Kubernetes

Once you have built the container image in the previous step, use the following steps to deploy the app to Kubernetes:

- Run the following command to deploy the app to Kubernetes:

    ```bash
    kubectl apply -f k8s/
    ```

- Access the app by navigating to the following URL:

    ```browser
    http://localhost:30080
    ```


