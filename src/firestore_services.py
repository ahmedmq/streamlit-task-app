import firebase_admin
from firebase_admin import firestore, credentials

cred = credentials.Certificate("firestore-key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

app = firebase_admin.get_app()
db = firestore.client(app)
tasks_ref = db.collection(u'tasks')


def add_task(**kwargs):
    ref = tasks_ref.document()
    ref.set({
        u'id': ref.id,
        u'title': kwargs.pop('title'),
        u'priority': kwargs.pop('priority'),
        u'project': kwargs.pop('project'),
        u'due_date': kwargs.pop('due_date'),
        u'completed': kwargs.pop('completed')
    })


def get_tasks():
    tasks = []
    for doc in tasks_ref.stream():
        tasks.append(doc.to_dict())
    return tasks


def update_task(task_id, completed):
    doc_ref = tasks_ref.document(task_id)
    doc_ref.update({
        u'completed': completed,
        u'priority': 'Low'
    })
