from typing import Optional
from pydantic import BaseModel

#Creating a Pydantic model for task creation. This model will be used to validate the incoming request data when creating a new task.
class TaskCreate(BaseModel):
    title: Optional[str] = None

#Creating a Pydantic model for task updates. This model will be used to validate the incoming request data when updating an existing task.
class TasksUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    done: Optional[bool] = None