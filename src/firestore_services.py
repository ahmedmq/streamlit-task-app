import firebase_admin
from firebase_admin import firestore, credentials

from Task import Task

cred = credentials.Certificate("firestore-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

app = firebase_admin.get_app()
db = firestore.client(app)
tasks_ref = db.collection(u'tasks')


def add_task(task):
    ref = tasks_ref.document()
    task.id = ref.id
    ref.set(task.to_dict())


def get_tasks():
    tasks = []
    for doc in tasks_ref.stream():
        tasks.append(Task.from_dict(doc.to_dict()))
    return tasks


def update_task(task):
    doc_ref = tasks_ref.document(task.id)
    doc_ref.update(task.to_dict())
