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

## Author

Taqi Shah
