#!/bin/bash
set -euo pipefail

DOMAIN="${1:-your-domain.com}"
EMAIL="${2:-admin@your-domain.com}"

mkdir -p certbot/conf

docker run --rm \
  -v "$PWD/certbot/conf:/etc/letsencrypt" \
  -p 80:80 \
  certbot/certbot certonly --standalone \
  --preferred-challenges http \
  --email "$EMAIL" \
  --agree-tos \
  -d "$DOMAIN"

echo "HTTPS certificates installed for $DOMAIN"
