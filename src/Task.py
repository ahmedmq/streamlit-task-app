import datetime


class Task(object):
    id: int
    title: str
    project: str
    priority: str
    completed: bool
    due_date: datetime
    created_at: datetime
    completed_at: datetime

    def __init__(self, task_id, title, project, priority, completed=False, due_date=None) -> None:
        self.id = task_id
        self.title = title
        self.project = project
        self.priority = priority
        self.completed = completed
        self.due_date = due_date
        self.created_at = datetime.datetime.now()
        self.completed_at = None

    @staticmethod
    def from_dict(source):
        task = Task(source['id'], source['title'], source['project'], source['priority'], source['completed'], source['due_date'])
        return task

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'project': self.project,
            'priority': self.priority,
            'completed': self.completed,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    def __repr__(self):
        return (
            f'Task(\
                id={self.id}, \
                title={self.title}, \
                project={self.project}, \
                priority={self.priority}, \
                completed={self.completed}, \
                due_date={self.due_date}, \
                created_at={self.created_at}, \
                completed_at={self.completed_at}\
            )'
        )
