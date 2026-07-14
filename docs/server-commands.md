# Server commands

## One-shot deployment
```bash
chmod +x deploy-server.sh
./deploy-server.sh
```

## Manual steps
```bash
chmod +x scripts/install-docker.sh scripts/setup-firewall.sh scripts/deploy.sh scripts/setup-https.sh scripts/backup.sh scripts/monitor.sh
./scripts/install-docker.sh
./scripts/setup-firewall.sh
cp .env.production.example .env
./scripts/deploy.sh
./scripts/setup-https.sh your-domain.com admin@your-domain.com
```

## Useful commands
```bash
docker compose ps
docker compose logs -f
docker compose down
docker compose up -d --build
./scripts/backup.sh
./scripts/monitor.sh
```
