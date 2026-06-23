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

<img width="1366" height="721" alt="2" src="https://github.com/user-attachments/assets/82720fd1-8fb6-4763-a1ca-60312c4bb870" />
<img width="1287" height="717" alt="3" src="https://github.com/user-attachments/assets/fe187a3d-3f5f-49bd-be0a-fed45d14d15b" />
<img width="1366" height="768" alt="4" src="https://github.com/user-attachments/assets/14ab0f47-26cd-4227-ab8e-39e1f556b1ea" />
<img width="1366" height="768" alt="4" src="https://github.com/user-attachments/assets/12635431-0e77-4fb5-b268-36c47e9864b8" />
<img width="1366" height="768" alt="6" src="https://github.com/user-attachments/assets/4b8c020c-5db2-4060-9efe-68af292ef3fb" />
<img width="1366" height="768" alt="7" src="https://github.com/user-attachments/assets/6ca2c839-af62-4236-8145-f8fbe5db84ce" />





