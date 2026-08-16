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

## Author

Taqi Shah
