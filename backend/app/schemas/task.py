from datetime import date

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: str = "open"
    due_date: date | None = None
    assignee_id: int | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    due_date: date | None = None
    assignee_id: int | None = None
