# Flask REST API on AWS EC2

A task management REST API built with Python/Flask, deployed on AWS EC2.

## Endpoints

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | /tasks | Get all tasks | 200 OK |
| GET | /tasks/:id | Get single task | 200 OK |
| POST | /tasks | Create new task | 201 Created |
| DELETE | /tasks/:id | Delete task | 200 OK |
| GET | /health | Health check | 200 OK |

## Error Handling
- Returns 404 with error message for non-existent tasks
- Returns 400 for missing required fields

## Tech Stack
- Python 3.13 / Flask
- AWS EC2 (Ubuntu t2.micro)
- Tested with Postman and browser

## How to Run Locally
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python app.py
```