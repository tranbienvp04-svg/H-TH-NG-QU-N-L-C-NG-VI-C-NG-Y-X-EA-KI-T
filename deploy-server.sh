#!/bin/bash
set -euo pipefail

echo "Installing Docker..."
chmod +x scripts/install-docker.sh
./scripts/install-docker.sh || true

echo "Configuring firewall..."
chmod +x scripts/setup-firewall.sh
./scripts/setup-firewall.sh || true

echo "Preparing environment..."
if [ ! -f .env ]; then
  cp .env.production.example .env
fi

echo "Deploying application..."
chmod +x scripts/deploy.sh
./scripts/deploy.sh

echo "Setup HTTPS (replace domain if needed)..."
chmod +x scripts/setup-https.sh
./scripts/setup-https.sh your-domain.com admin@your-domain.com || true

echo "Deployment finished."
