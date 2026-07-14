# Production checklist

- [ ] Buy or allocate a VPS/VM with public IP.
- [ ] Open ports 80 and 443.
- [ ] Point DNS A record to the server IP.
- [ ] Copy .env.production.example to .env and update values.
- [ ] Run ./scripts/deploy.sh.
- [ ] Run ./scripts/setup-https.sh your-domain.com admin@your-domain.com.
- [ ] Configure a reverse proxy or Cloudflare if needed.
- [ ] Set up automated backups with ./scripts/backup.sh.
- [ ] Monitor health with ./scripts/monitor.sh.
