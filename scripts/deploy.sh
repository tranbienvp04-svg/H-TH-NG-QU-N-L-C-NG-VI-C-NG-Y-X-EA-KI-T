#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

docker compose pull
docker compose up -d --build

docker compose exec -T backend python -m alembic upgrade head

echo "Deployment completed. Open your domain or server IP to access the app."
