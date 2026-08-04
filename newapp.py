from fastapi import FastAPI, HTTPException, Response

from database import connection, initialize_database

# =====================================================
# Pydantic Models
# =====================================================



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
