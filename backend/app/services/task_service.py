from app.schemas.task import TaskCreate, TaskOut


class TaskService:
    _tasks: list[TaskOut] = []

    @classmethod
    def list_tasks(cls) -> list[TaskOut]:
        return cls._tasks

    @classmethod
    def create_task(cls, payload: TaskCreate) -> TaskOut:
        task_id = len(cls._tasks) + 1
        task = TaskOut(id=task_id, **payload.model_dump())
        cls._tasks.append(task)
        return task
