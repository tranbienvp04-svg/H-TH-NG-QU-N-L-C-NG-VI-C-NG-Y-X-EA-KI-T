#!/bin/bash
set -euo pipefail

BACKUP_DIR="${1:-./backups}"
mkdir -p "$BACKUP_DIR"
DATE=$(date +%Y%m%d_%H%M%S)

docker compose exec -T db pg_dump -U postgres danguy > "$BACKUP_DIR/db_$DATE.sql"

echo "Database backup saved to $BACKUP_DIR/db_$DATE.sql"
