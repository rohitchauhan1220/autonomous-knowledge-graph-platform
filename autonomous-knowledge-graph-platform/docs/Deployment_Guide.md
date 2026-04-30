# Deployment Guide

## Production Checklist

- Replace default secrets in `.env`.
- Use PostgreSQL or managed SQL instead of local SQLite.
- Enable Neo4j with a strong password and network restrictions.
- Configure HTTPS at the reverse proxy.
- Add object storage for uploads.
- Set API rate limits suitable for tenant size.
- Run database migrations before traffic is routed to the app.

## Gunicorn

```bash
gunicorn -c deployment/gunicorn/gunicorn.conf.py backend.wsgi:app
```

## Docker Compose

```bash
docker compose up --build -d
```

## Kubernetes

Use `deployment/kubernetes/deployment.yaml` as a starting point and provide secrets through your cloud secret manager.
