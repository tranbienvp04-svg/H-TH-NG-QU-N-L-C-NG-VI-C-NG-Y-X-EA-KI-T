from app.schemas.task import TaskCreate, TaskOut


class TaskCRUD:
    _tasks: list[TaskOut] = []

    @classmethod
    def list_tasks(cls) -> list[TaskOut]:
        return cls._tasks

    @classmethod
    def create_task(cls, payload: TaskCreate) -> TaskOut:
        task = TaskOut(id=len(cls._tasks) + 1, **payload.model_dump())
        cls._tasks.append(task)
        return task
