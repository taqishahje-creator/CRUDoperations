from fastapi import FastAPI, HTTPException, Response

from database import connection, initialize_database
from models import TaskCreate, TasksUpdate


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="Task API",
    description="A simple CRUD API built using FastAPI and PostgreSQL.",
    version="1.0"
)


# =====================================================
# PostgreSQL Database Initialization
# =====================================================

initialize_database()


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
        "database": "PostgreSQL",
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
    Returns all tasks from the PostgreSQL database.
    """

    connect = connection()

    try:
        cursor = connect.cursor()

        cursor.execute(
            """
            SELECT id, title, done
            FROM tasks
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row["id"], # type: ignore
                "title": row["title"], # type: ignore
                "done": row["done"] # type: ignore
            }
            for row in rows
        ]

    finally:
        connect.close()


# =====================================================
# Get Task by ID
# =====================================================

@app.get("/tasks/{task_id}", summary="Get Task by ID")
async def get_task(task_id: int):
    """
    Returns a single task using its ID.
    """

    connect = connection()

    try:
        cursor = connect.cursor()

        cursor.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        return {
            "id": row["id"], # type: ignore
            "title": row["title"], # type: ignore
            "done": row["done"] # type: ignore
        }

    finally:
        connect.close()


# =====================================================
# Create New Task
# =====================================================

@app.post(
    "/tasks",
    status_code=201,
    summary="Create New Task"
)
async def create_task(task: TaskCreate):
    """
    Creates a new task in PostgreSQL.
    """

    # -------------------------------------------------
    # Validate title
    # -------------------------------------------------

    if task.title is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Title is required"}
        )

    title = task.title.strip()

    if title == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "Title cannot be empty"}
        )

    connect = connection()

    try:
        cursor = connect.cursor()

        # -------------------------------------------------
        # Insert task into PostgreSQL
        # -------------------------------------------------

        cursor.execute(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id, title, done
            """,
            (title, False)
        )

        row = cursor.fetchone()

        if row is None:
            connect.rollback()

            raise HTTPException(
                status_code=500,
                detail={"error": "Task could not be created"}
            )

        # -------------------------------------------------
        # Commit transaction
        # -------------------------------------------------

        connect.commit()

        return {
            "id": row["id"], # type: ignore
            "title": row["title"], # type: ignore
            "done": row["done"] # type: ignore
        }

    except HTTPException:
        connect.rollback()
        raise

    except Exception:
        connect.rollback()
        raise

    finally:
        connect.close()


# =====================================================
# Update Task by ID
# =====================================================

@app.put(
    "/tasks/{task_id}",
    summary="Update Task by ID"
)
async def update_task(
    task_id: int,
    task: TasksUpdate
):
    """
    Updates an existing task in PostgreSQL.
    """

    # -------------------------------------------------
    # Make sure at least one field is provided
    # -------------------------------------------------

    if task.title is None and task.done is None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": (
                    "At least one field (title or done) "
                    "must be provided for update"
                )
            }
        )

    # -------------------------------------------------
    # Check body ID against URL ID
    # -------------------------------------------------

    if task.id is not None and task.id != task_id:
        raise HTTPException(
            status_code=400,
            detail={
                "error": (
                    "Task ID in the path does not match "
                    "the ID in the request body"
                )
            }
        )

    connect = connection()

    try:
        cursor = connect.cursor()

        # -------------------------------------------------
        # Check if task exists
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

        existing = cursor.fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        # -------------------------------------------------
        # Build UPDATE statement
        # -------------------------------------------------

        fields = []
        params = []

        # Update title if provided
        if task.title is not None:

            title = task.title.strip()

            if title == "":
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Title cannot be empty"
                    }
                )

            fields.append("title = %s")
            params.append(title)

        # Update done if provided
        if task.done is not None:

            fields.append("done = %s")
            params.append(task.done)

        # Add ID for WHERE clause
        params.append(task_id)

        # -------------------------------------------------
        # Execute UPDATE
        # -------------------------------------------------

        query = f"""
            UPDATE tasks
            SET {", ".join(fields)}
            WHERE id = %s
            RETURNING id, title, done
        """

        cursor.execute(query, tuple(params))

        row = cursor.fetchone()

        if row is None:
            connect.rollback()

            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        # -------------------------------------------------
        # Commit transaction
        # -------------------------------------------------

        connect.commit()

        return {
            "id": row["id"], # type: ignore
            "title": row["title"], # type: ignore
            "done": row["done"] # type: ignore 
        }

    except HTTPException:
        connect.rollback()
        raise

    except Exception:
        connect.rollback()
        raise

    finally:
        connect.close()


# =====================================================
# Delete Task by ID
# =====================================================

@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete Task by ID"
)
async def delete_task(task_id: int):
    """
    Deletes a task from PostgreSQL.
    """

    connect = connection()

    try:
        cursor = connect.cursor()

        # -------------------------------------------------
        # Check if task exists
        # -------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

        existing = cursor.fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found"
            )

        # -------------------------------------------------
        # Delete task
        # -------------------------------------------------

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

        # -------------------------------------------------
        # Commit transaction
        # -------------------------------------------------

        connect.commit()

        return Response(status_code=204)

    except HTTPException:
        connect.rollback()
        raise

    except Exception:
        connect.rollback()
        raise

    finally:
        connect.close()