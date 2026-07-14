# Deployment Guide

## Prerequisites
- Docker Desktop
- Docker Compose
- Python 3.11+
- Node.js 20+
- Flutter SDK (optional for mobile build)

## Run backend locally
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run frontend locally
```bash
cd frontend
npm install
npm run dev
```

## Run full stack with Docker
```bash
docker compose up --build
```

## Deploy to a public server
- Copy [.env.production.example](../.env.production.example) to `.env`.
- Update the secret key and domain settings.
- Run `./scripts/deploy.sh`.
- Open port 80/443 and point your DNS to the server IP.

## Default credentials
- Username: admin
- Password: 123456
