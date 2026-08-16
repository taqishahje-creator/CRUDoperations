from fastapi import FastAPI, HTTPException, Response
from database import connection, initialize_database
from models import TaskCreate, TasksUpdate

# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built using FastAPI.",
    version="1.0"
)

# =====================================================
# PostgreSQL Database Initialization
# =====================================================
initialize_database()  # Initialize the database and insert sample data if needed.

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
    connect = connection()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM tasks")
    row = cursor.fetchall()
    connect.close()

    tasks = []
    tasks.extend(
        {"id": r[0], "title": r[1], "done": bool(r[2])}
        for r in row
    )
    return tasks


# =====================================================
# Get Task by ID
# =====================================================

@app.get("/tasks/{task_id}", summary="Get Task by ID")
async def get_task(task_id: int):
    """
    Returns a single task using its ID.
    """
    connect = connection()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    connect.close()

    if row:
        return {
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])
        }

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


# =====================================================
# Create New Task
# =====================================================

@app.post("/tasks", status_code=201)
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

    # RETURNING id is required for PostgreSQL — no lastrowid in psycopg
    cursor.execute(
        "INSERT INTO tasks(title, done) VALUES (%s, %s) RETURNING id",
        (title, False)
    )

    row = cursor.fetchone()
    if row is None:
        connect.rollback()
        connect.close()
        raise HTTPException(
            status_code=500,
            detail={"error": "Task could not be created"}
        )

    task_id = row[0]

    connect.commit()
    connect.close()

    return {
        "id": task_id,
        "title": title,
        "done": False
    }


# =====================================================
# Update Task by ID
# =====================================================

@app.put("/tasks/{task_id}", summary="Update task by id")
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

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
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
        fields.append("title = %s")
        params.append(title)
    if task.done is not None:
        fields.append("done = %s")
        params.append(bool(task.done))

    params.append(task_id)
    cursor.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s", tuple(params))
    connect.commit()

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    connect.close()

    if row is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return {"id": row[0], "title": row[1], "done": bool(row[2])}


# =====================================================
# Delete Task by ID
# =====================================================

@app.delete("/tasks/{task_id}", summary="Delete Task by ID")
async def delete_task(task_id: int):
    """
    Deletes a task by its ID.
    """
    connect = connection()
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing = cursor.fetchone()
    if not existing:
        connect.close()
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connect.commit()
    connect.close()

    return Response(status_code=204)
