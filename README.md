# Hệ thống quản lý công việc Đảng ủy xã Ea Kiết

## Tổng quan
Dự án này cung cấp một nền tảng monorepo đầy đủ cho:
- Backend FastAPI
- Frontend React/Vite
- Ứng dụng Android Flutter
- Docker, Nginx, PostgreSQL, Alembic
- Tài liệu triển khai và kiểm thử

## Cấu trúc chính
- backend/: API FastAPI và migration Alembic
- frontend/: ứng dụng web React/Vite
- mobile/: ứng dụng Flutter Android
- docs/: hướng dẫn triển khai
- nginx/: cấu hình proxy

## Chạy backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Chạy frontend
```bash
cd frontend
npm install
npm run dev
```

## Chạy toàn bộ stack bằng Docker
```bash
docker compose up --build
```

## Triển khai lên internet (VPS / cloud)
1. Mua hoặc cấp một VPS/VM có Docker và Docker Compose.
2. Đăng nhập vào server và clone repo.
3. Sao chép file môi trường:
   ```bash
   cp .env.production.example .env
   ```
4. Cập nhật `SECRET_KEY`, tên miền, và thông tin database nếu cần.
5. Chạy deployment tự động:
   ```bash
   chmod +x deploy-server.sh
   ./deploy-server.sh
   ```
6. Trỏ DNS của tên miền về IP server và mở port 80/443.
7. Nếu cần HTTPS, chạy:
   ```bash
   ./scripts/setup-https.sh your-domain.com admin@your-domain.com
   ```

## Tài khoản demo
- admin / 123456

## Kiểm thử backend
```bash
cd backend
pytest app/tests/test_api.py
```
