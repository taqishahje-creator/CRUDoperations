from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from database import connection, initialize_database
# =====================================================
# Pydantic Models
# =====================================================
#Creating a Pydantic model for task creation. This model will be used to validate the incoming request data when creating a new task.
class TaskCreate(BaseModel):
    title: Optional[str] = None

#Creating a Pydantic model for task updates. This model will be used to validate the incoming request data when updating an existing task.
class TasksUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    done: Optional[bool] = None
    

# =====================================================
# FastAPI Application
# =====================================================

newapp = FastAPI(
    title="Task API",
    description="A simple CRUD API built using FastAPI.",
    version="1.0"
)

# =====================================================
# SQLite Database
# =====================================================
initialize_database()  # Initialize the database and insert sample data if needed.
# =====================================================
# Root Endpoint
# =====================================================

@newapp.get("/", summary="API Information")
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

@newapp.get("/health", summary="Health Check")
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

@newapp.get("/tasks", summary="Get All Tasks")
async def get_all_tasks():
    """
    Returns the complete list of tasks.
    """
    
    connect =  connection()

    cursor = connect.cursor()

    cursor.execute("SELECT * FROM tasks")

   
    row =  cursor.fetchall()
    connect.close()
    tasks = []

    tasks.extend(
        {"id": r["id"], "title": r["title"], "done": bool(r["done"])}
        for r in row
    )
    return tasks


# =====================================================
# Get Task by ID
# =====================================================

@newapp.get("/tasks/{task_id}", summary="Get Task by ID")
async def get_task(task_id: int):
    """
    Returns a single task using its ID.
    """
    connect = connection()
    
    cursor = connect.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    
    row = cursor.fetchone()
    
    connect.close()

    if row:
        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# =====================================================
# Create New Task
# =====================================================



@newapp.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    """
    Creates a new task.
    """

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

    connect = connection()
    
    cursor = connect.cursor()
    
    cursor.execute(
        "INSERT INTO tasks(title, done) VALUES (?, ?)",
        (title, False)
    )
    
    connect.commit()
    
    task_id = cursor.lastrowid
    
    connect.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }
    
#=======================================
#update task by id
#=======================================

@newapp.put("/tasks/{task_id}", summary = "Update task by id")
async def update_task(task_id: int, task: TasksUpdate):
    """
    Update a task by its id
    """
    if task.title is None and task.done is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "At least one field (title or done) must be provided for update"}
        )

    # Ensure if body contains id it matches path id
    if task.id is not None and task.id != task_id:
        raise HTTPException(
            status_code=400,
            detail={"error": "Task ID in the path does not match the ID in the request body"}
        )

    connect = connection()
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing = cursor.fetchone()
    if not existing:
        connect.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    fields = []
    params = []
    if task.title is not None:
        title = task.title.strip()
        if title == "":
            connect.close()
            raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})
        fields.append("title = ?")
        params.append(title)
    if task.done is not None:
        fields.append("done = ?")
        params.append(int(bool(task.done)))

    params.append(task_id)
    cursor.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", tuple(params))
    connect.commit()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    connect.close()

    return {"id": row["id"], "title": row["title"], "done": bool(row["done"]) }


#=====================================================
# Delete task by id
#=====================================================

@newapp.delete("/tasks/{task_id}", summary="Delete Task by ID")
async def delete_task(task_id: int):
    """ 
    Deletes a task by its ID.
    """
    connect = connection()
    cursor = connect.cursor()
    
    existing = cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not existing:
        connect.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connect.commit()
    
    connect.close()
    
    return Response(status_code=204)


