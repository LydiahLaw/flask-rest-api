# Flask REST API on AWS EC2

![CI](https://github.com/LydiahLaw/flask-rest-api/actions/workflows/ci.yml/badge.svg)

A task management REST API built with Python/Flask, deployed on AWS EC2 with Nginx and Gunicorn. Every push is linted, tested and built as a Docker image by a GitHub Actions pipeline.

## Deployment Stack
- Flask app served by Gunicorn (4 workers)
- Nginx as reverse proxy on port 80
- Systemd service for auto-restart on reboot
- AWS EC2 Ubuntu t2.micro (eu-central-1)

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
- Gunicorn (WSGI server, 4 workers)
- Nginx (reverse proxy)
- Systemd (process management)
- AWS EC2 Ubuntu 24.04 t2.micro
- Docker (container image)
- GitHub Actions (CI)
- pytest and flake8 (testing and linting)

## CI Pipeline

The workflow in `.github/workflows/ci.yml` runs on every push and pull request to `main`, on a pinned `ubuntu-24.04` runner.

| Job | What it does |
|-----|--------------|
| Lint and test | Installs Python 3.13, checks code style with flake8, runs 8 pytest tests covering every endpoint and error case |
| Build and smoke-test Docker image | Runs only if tests pass. Builds the image, starts the container and checks that `/health` responds |

<img width="1366" height="673" alt="github actions ci" src="https://github.com/user-attachments/assets/fbb1577a-79bf-40d9-892b-80a96b9363a1" />


## Run the Tests
```bash
pip install -r requirements-dev.txt
flake8 app.py tests --max-line-length=100
pytest -v
```

## Run with Docker
```bash
docker build -t flask-rest-api .
docker run -d -p 5000:5000 flask-rest-api
curl http://localhost:5000/health
```
The image uses `python:3.13-slim`, serves the app with Gunicorn (4 workers) and runs as a non-root user.

## How to Run Locally
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

## How to Deploy on EC2

**1. SSH into your EC2 instance:**
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

**2. Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv git nginx -y
```

**3. Clone and set up the app:**
```bash
git clone https://github.com/LydiahLaw/flask-rest-api.git
cd flask-rest-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**4. Create systemd service:**
```bash
sudo nano /etc/systemd/system/flask-api.service
```
```ini
[Unit]
Description=Flask REST API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/flask-rest-api
Environment="PATH=/home/ubuntu/flask-rest-api/venv/bin"
ExecStart=/home/ubuntu/flask-rest-api/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable flask-api
sudo systemctl start flask-api
```

**5. Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/flask-api
```
```nginx
server {
    listen 80;
    server_name YOUR_EC2_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/flask-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## EC2 Deployment (Screenshots)

The EC2 instance is no longer running; these screenshots show the deployment working.


<img width="1366" height="734" alt="8" src="https://github.com/user-attachments/assets/7f014bc2-158a-4d60-8e18-da4a8e3642f5" />
<img width="1366" height="768" alt="9" src="https://github.com/user-attachments/assets/dfe7a18d-88c5-484d-8de1-45f661c6241a" />
<img width="1366" height="768" alt="10" src="https://github.com/user-attachments/assets/c81148ab-e68e-42be-aa92-3d1ddee35760" />
<img width="1366" height="725" alt="browser ip" src="https://github.com/user-attachments/assets/addf9552-e0b3-40c3-acf0-d596329d91b8" />




## API Testing (Postman - Local)

<img width="1366" height="721" alt="2" src="https://github.com/user-attachments/assets/82720fd1-8fb6-4763-a1ca-60312c4bb870" />
<img width="1287" height="717" alt="3" src="https://github.com/user-attachments/assets/fe187a3d-3f5f-49bd-be0a-fed45d14d15b" />
<img width="1366" height="768" alt="4" src="https://github.com/user-attachments/assets/14ab0f47-26cd-4227-ab8e-39e1f556b1ea" />
<img width="1366" height="768" alt="4" src="https://github.com/user-attachments/assets/12635431-0e77-4fb5-b268-36c47e9864b8" />
<img width="1366" height="768" alt="6" src="https://github.com/user-attachments/assets/4b8c020c-5db2-4060-9efe-68af292ef3fb" />
<img width="1366" height="768" alt="7" src="https://github.com/user-attachments/assets/6ca2c839-af62-4236-8145-f8fbe5db84ce" />

## What I Learned
- Deploying a Python API on a remote Linux server via SSH
- Configuring Nginx as a reverse proxy in front of Gunicorn
- Managing long-running services with systemd
- REST API design with proper HTTP status codes
- Testing APIs with Postman
- AWS EC2 provisioning and security group configuration
- Writing automated tests with pytest and isolating tests that share in-memory state
- Building a CI pipeline with GitHub Actions, with jobs that depend on each other
- Containerising a Python app with Docker and smoke-testing it in CI
- Pinning runner and dependency versions so builds are reproducible
