import datetime

import firebase_admin
from firebase_admin import firestore, credentials

from Task import Task

cred = credentials.Certificate("firestore-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

app = firebase_admin.get_app()
db = firestore.client(app)
tasks_ref = db.collection(u'tasks')


def save(task):
    ref = tasks_ref.document()
    task.id = ref.id
    ref.set(task.to_dict())


def find_all(flag_dict):
    tasks = []
    query = tasks_ref
    for key, value in flag_dict.items():
        query = query.where(key, u'==', value)
    for doc in query.stream():
        tasks.append(Task.from_dict(doc.to_dict()))
    return tasks


def update(task):
    doc_ref = tasks_ref.document(task.id)
    doc_ref.update(task.to_dict())


def delete(task):
    task.deleted_at = datetime.datetime.now()
    task.deleted_flag = True
    doc_ref = tasks_ref.document(task.id)
    doc_ref.update(task.to_dict())
