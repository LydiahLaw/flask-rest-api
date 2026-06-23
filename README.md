# Flask REST API on AWS EC2

A task management REST API built with Python/Flask, deployed on AWS EC2 with Nginx and Gunicorn.

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

## Live Demo (EC2 Deployment)

[ADD YOUR EC2 SCREENSHOTS HERE - replace localhost screenshots with EC2 IP screenshots]

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