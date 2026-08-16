# Task API - FastAPI CRUD

A simple RESTful Task Management API built using FastAPI. The project demonstrates CRUD operations using an in-memory list and includes interactive API documentation through Swagger UI.

---

## Features

- FastAPI
- CRUD Operations
- In-memory storage
- Input validation
- Swagger UI
- JSON responses
- HTTP status codes

---

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/TaskAPI.git
```

Move into the project

```bash
cd TaskAPI
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run

```bash
uvicorn app:app --reload
```

Visit

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API Information |
| GET | /health | Health Check |
| GET | /tasks | Get All Tasks |
| GET | /tasks/{id} | Get Task by ID |
| POST | /tasks | Create Task |
| PUT | /tasks/{id} | Update Task |
| DELETE | /tasks/{id} | Delete Task |

---

## Example curl

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example Response

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

---

## Swagger UI

Open

```
http://127.0.0.1:8000/docs
```

Insert a screenshot of Swagger UI here.

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI

---
# Assignment 2 – Connecting the CRUD API to SQLite

## Overview

In this assignment, the Task CRUD API was upgraded from using an in-memory Python list to a persistent SQLite database. The API endpoints remained the same, but the application's data storage layer was replaced with a database, allowing tasks to persist even after the server is restarted.

## What Changed

### Before (Assignment 1)

In Assignment 1, all tasks were stored inside a Python list:

```python
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": True}
]
```

This approach had one major limitation:

* Every time the server restarted, all tasks were lost because they existed only in the program's memory (RAM).

Application architecture:

```
Client
   │
   ▼
FastAPI
   │
   ▼
Python In-Memory List
```

### After (Assignment 2)

The in-memory list was replaced with an SQLite database named `tasks.db`.

Now every CRUD operation interacts directly with the database using SQL queries.

Application architecture:

```
Client
   │
   ▼
FastAPI
   │
   ▼
SQLite Database (tasks.db)
```

Because the data is stored on disk instead of memory, tasks remain available after restarting the application.

## Why SQLite?

SQLite was chosen because it:

* Requires no separate database server.
* Automatically creates the database file when the application runs.
* Is lightweight and easy to integrate with Python.
* Is suitable for small applications and learning SQL.
* Stores all data inside a single database file.

## Database File

The project automatically creates:

```
tasks.db
```

during the first execution if it does not already exist.

## Automatic Database Initialization

When the application starts, it automatically:

1. Connects to the SQLite database.
2. Creates the `tasks` table if it does not exist.
3. Checks whether the table already contains data.
4. Inserts three sample tasks only when the table is empty.

This prevents duplicate sample records from being inserted every time the application starts.

## CRUD Operations

The API endpoints remain unchanged.

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/tasks`      | Retrieve all tasks      |
| GET    | `/tasks/{id}` | Retrieve a task by ID   |
| POST   | `/tasks`      | Create a new task       |
| PUT    | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task           |

The only difference from Assignment 1 is that every operation now executes SQL queries instead of modifying a Python list.

## SQL Operations Used

The application uses the following SQL statements:

* `CREATE TABLE IF NOT EXISTS`
* `SELECT`
* `INSERT`
* `UPDATE`
* `DELETE`
* `COUNT(*)`

These queries allow the API to create, retrieve, update, and delete tasks while keeping the data permanently stored.

## Example SQL Query

Retrieve all tasks:

```sql
SELECT * FROM tasks;
```

## Running the Project

1. Create and activate a virtual environment.
2. Install the required packages:

```bash
pip install fastapi uvicorn
```

3. Start the application:

```bash
uvicorn app:app --reload
```

4. Open the interactive API documentation:

```
http://127.0.0.1:8000/docs
```

On the first run, the application automatically creates the SQLite database and initializes it with sample data if the database is empty.


# Assignment 3 Variant with Postgres SQL on Docker Setup

A Task CRUD API built with FastAPI, backed by a PostgreSQL database running in Docker. This is the third storage swap in the FlyRank Backend Track series — memory (A1) → SQLite (A2) → containerized Postgres (this one). The API surface is identical across all three; only the storage engine underneath changes.

## What this is

A simple task management REST API supporting full CRUD (Create, Read, Update, Delete) operations, with tasks persisted in a PostgreSQL database running inside a Docker container. Configuration (database credentials) is kept out of source control via environment variables.

## Tech stack

- **Language:** Python 3 (FastAPI)
- **Database:** PostgreSQL 17 (Docker container)
- **Driver:** psycopg 3
- **Config:** python-dotenv (`.env`)

## Prerequisites

- Docker Desktop (or Podman) installed and running
- Python 3.10+
- pip

## Setup — one command to run everything

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd <your-repo-folder>

# 2. Copy the example env file and adjust if needed
cp .env.example .env

# 3. Create a virtual environment and install dependencies
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt

# 4. Start Postgres in Docker
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks \
  -p 5432:5432 -v taskdata:/var/lib/postgresql/data -d postgres:17

# 5. Run the API
uvicorn A3ModifiedApp:app --reload
```

The API will be available at `http://localhost:8000`, and the interactive docs at `http://localhost:8000/docs`.

## Environment variables

Set in `.env` (git-ignored). See `.env.example` for the required keys.

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | Postgres connection string | `postgresql://postgres:dev@localhost:5432/tasks` |

> Note: if port `5432` is already in use on your machine (e.g. by a native Postgres install), map the container to a different host port such as `5433` and update `DATABASE_URL` accordingly.

## Database

On startup, the app automatically:
- Connects to Postgres using `DATABASE_URL`
- Creates the `tasks` table if it doesn't already exist
- Seeds three example tasks, but only if the table is empty (won't duplicate on restart)

**Schema:**

| Column | Type | Notes |
|---|---|---|
| `id` | `SERIAL PRIMARY KEY` | Auto-incrementing |
| `title` | `TEXT NOT NULL` | Task title |
| `done` | `BOOLEAN NOT NULL` | Completion status |

## Endpoints

| Method | Path | Description | Success | Error |
|---|---|---|---|---|
| GET | `/` | API info | 200 | — |
| GET | `/health` | Health check | 200 | — |
| GET | `/tasks` | List all tasks | 200 | — |
| GET | `/tasks/{id}` | Get a single task | 200 | 404 if not found |
| POST | `/tasks` | Create a task | 201 | 400 if title missing/empty |
| PUT | `/tasks/{id}` | Update a task | 200 | 400 invalid body, 404 if not found |
| DELETE | `/tasks/{id}` | Delete a task | 204 | 404 if not found |

## Example request

```bash
curl -i http://localhost:8000/tasks
```

```
HTTP/1.1 200 OK
content-type: application/json

[
  {"id": 1, "title": "Buy groceries", "done": false},
  {"id": 2, "title": "Complete assignment", "done": true},
  {"id": 3, "title": "Exercise for 30 minutes", "done": false}
]
```

## Verifying data in the database

```bash
docker exec -it taskdb psql -U postgres -d tasks -c "\dt"
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

**Screenshot:**

*(insert screenshot of `\dt` and `SELECT * FROM tasks;` output here)*

## Notes on the storage swap

The routes and request/response shapes are unchanged from A1 (in-memory) and A2 (SQLite). Only the `database.py` module — the single place all database logic lives — changed to talk to Postgres instead of SQLite. This is the point of keeping storage logic isolated from route logic: swapping the underlying engine three times required touching only one file each time, proving storage really is "just an implementation detail" behind a stable API.

## Project structure

```
.
├── A3ModifiedApp.py    # FastAPI app and routes
├── database.py         # All database connection/query logic
├── models.py           # Pydantic request models
├── .env.example         # Template for required environment variables
├── .gitignore
└── README.md
```

## Author

Taqi Shah
