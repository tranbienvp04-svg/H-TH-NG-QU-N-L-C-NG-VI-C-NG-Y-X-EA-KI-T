#!/bin/bash
set -euo pipefail

echo "Checking app health..."
curl -fsS http://localhost/api/health || true
curl -fsS http://localhost/ || true
