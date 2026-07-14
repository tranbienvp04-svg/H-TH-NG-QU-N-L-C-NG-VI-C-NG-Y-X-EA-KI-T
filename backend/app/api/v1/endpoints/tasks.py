from fastapi import APIRouter

from app.schemas.task import TaskCreate, TaskOut
from app.services.task_service import TaskService

router = APIRouter()


@router.get("", response_model=list[TaskOut])
def list_tasks() -> list[TaskOut]:
    return TaskService.list_tasks()


@router.post("", response_model=TaskOut)
def create_task(payload: TaskCreate) -> TaskOut:
    return TaskService.create_task(payload)
