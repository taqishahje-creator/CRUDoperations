from typing import Optional
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

# =====================================================
# Pydantic Models
# =====================================================

class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built using FastAPI.",
    version="1.0"
)

# =====================================================
# SQLite Database
# =====================================================

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Test with Swagger",
        "done": True
    },
    {
        "id": 4,
        "title": "Deploy to Production",
        "done": False
    },
    {
        "id": 5,
        "title": "Upload to GitHub",
        "done": True
    }
]

# =====================================================
# Root Endpoint
# =====================================================

@app.get("/", summary="API Information")
async def read_home():
    """
    Returns basic information about the API.
    """

    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# =====================================================
# Health Check Endpoint
# =====================================================

@app.get("/health", summary="Health Check")
async def health_check():
    """
    Checks whether the API is running.
    """

    return {
        "status": "ok"
    }


# =====================================================
# Get All Tasks
# =====================================================

@app.get("/tasks", summary="Get All Tasks")
async def get_all_tasks():
    """
    Returns the complete list of tasks.
    """

    return tasks


# =====================================================
# Get Task by ID
# =====================================================

@app.get("/tasks/{task_id}", summary="Get Task by ID")
async def get_task(task_id: int):
    """
    Returns a single task using its ID.
    """

    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# =====================================================
# Create New Task
# =====================================================

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):

    # Missing title
    if task.title is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Title is required"}
        )

    title = task.title.strip()

    # Empty title
    if title == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "Title cannot be empty"}
        )

    next_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

# =====================================================
# Update Existing Task
# =====================================================

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate):

    # Missing title
    if task.title is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Title is required"}
        )

    title = task.title.strip()

    # Empty title
    if title == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "Title cannot be empty"}
        )

    # Missing done field
    if task.done is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Done field is required"}
        )

    for existing_task in tasks:

        if existing_task["id"] == task_id:

            existing_task["title"] = title
            existing_task["done"] = task.done

            return existing_task

    raise HTTPException(
        status_code=404,
        detail={"error": f"Task {task_id} not found"}
    )


# =====================================================
# Delete Task
# =====================================================

@app.delete("/tasks/{task_id}", status_code=204, summary="Delete Task")
async def delete_task(task_id: int):
    """
    Deletes a task using its ID.
    """

    for index, task in enumerate(tasks):

        if task["id"] == task_id:

            tasks.pop(index)

            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )