from fastapi import FastAPI, HTTPException

# Create the FastAPI application
app = FastAPI()

# In-memory list of tasks (acts as our temporary database)
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
    }
]


# ==========================
# Root Endpoint
# ==========================
@app.get("/")
async def read_home():
    """
    Returns basic information about the API.
    """
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# ==========================
# Health Check Endpoint
# ==========================
@app.get("/health")
async def health_check():
    """
    Returns the health status of the API.
    """
    return {
        "status": "ok"
    }


# ==========================
# Get All Tasks
# ==========================
@app.get("/tasks")
async def get_all_tasks():
    """
    Returns the complete list of tasks.
    """
    return tasks


# ==========================
# Get Single Task by ID
# ==========================
@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """
    Returns a single task using its ID.
    """

    # Search for the requested task
    for task in tasks:
        if task["id"] == task_id:
            return task

    # If the task is not found, return HTTP 404
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )