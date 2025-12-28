# Production Deployment Guide

This guide provides comprehensive instructions for deploying Sankalpa in a production environment.

## Deployment Options

Sankalpa can be deployed using various methods:

1. **Docker Compose**: Simplest approach for small to medium deployments
2. **Kubernetes**: Recommended for larger, scalable deployments
3. **AWS ECS/EKS**: Cloud-native deployment on AWS
4. **Azure AKS**: Cloud-native deployment on Azure
5. **GCP GKE**: Cloud-native deployment on Google Cloud

## Prerequisites

- Docker and Docker Compose (for Docker-based deployments)
- Kubernetes CLI (for Kubernetes-based deployments)
- Domain name with DNS configured
- SSL/TLS certificates

## Environment Configuration

Create a production-ready `.env` file based on the `.env.example` template:

```bash
# Make a copy of the example
cp .env.example .env.production

# Edit the production environment file
nano .env.production
```

Important production settings:

```
# API Settings
SANKALPA_ENV=production
SANKALPA_API_PORT=8000
SANKALPA_DEBUG=false
SANKALPA_LOG_LEVEL=INFO
SANKALPA_ALLOWED_ORIGINS=https://yourdomain.com

# Security - Use a strong secret!
SANKALPA_JWT_SECRET=<generate-a-strong-random-secret>

# Database
POSTGRES_USER=<production-db-user>
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=sankalpa
POSTGRES_HOST=postgres

# Redis
REDIS_URL=redis://redis:6379/0

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Docker Compose Deployment

1. Build the Docker images:

```bash
docker-compose -f docker-compose.yml build
```

2. Start the services:

```bash
docker-compose -f docker-compose.yml --env-file .env.production up -d
```

3. Verify the deployment:

```bash
docker-compose ps
```

## Kubernetes Deployment

1. Create Kubernetes configuration files:

```bash
# Create namespace
kubectl create namespace sankalpa

# Create secrets
kubectl create secret generic sankalpa-secrets \
  --from-env-file=.env.production \
  --namespace=sankalpa

# Apply configurations
kubectl apply -f k8s/
```

2. Verify the deployment:

```bash
kubectl get all -n sankalpa
```

## SSL Configuration

### Using NGINX as a Reverse Proxy

1. Install NGINX:

```bash
apt update
apt install nginx
```

2. Configure NGINX:

```
server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Obtain SSL certificates using Let's Encrypt:

```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com
```

## Database Backup

Set up a cron job to back up the PostgreSQL database:

```bash
# Create a backup script
cat > /usr/local/bin/backup-sankalpa-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/path/to/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/sankalpa_backup_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Create the backup
docker exec sankalpa_postgres pg_dump -U postgres -d sankalpa > $BACKUP_FILE

# Compress the backup
gzip $BACKUP_FILE

# Delete backups older than 30 days
find $BACKUP_DIR -name "sankalpa_backup_*.sql.gz" -mtime +30 -delete
EOF

# Make the script executable
chmod +x /usr/local/bin/backup-sankalpa-db.sh

# Add to crontab (daily at 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/backup-sankalpa-db.sh") | crontab -
```

## Monitoring

### Prometheus and Grafana Setup

1. Add monitoring configuration to `docker-compose.yml`:

```yaml
prometheus:
  image: prom/prometheus:latest
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    - prometheus_data:/prometheus
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana:latest
  volumes:
    - grafana_data:/var/lib/grafana
  ports:
    - "3001:3000"
  depends_on:
    - prometheus

volumes:
  prometheus_data:
  grafana_data:
```

2. Configure Prometheus:

```yaml
# ./monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'sankalpa'
    static_configs:
      - targets: ['backend:8000']
```

## Security Considerations

1. **Secrets Management**: Use environment variables and never commit secrets to version control
2. **Network Security**: Use private networks for services and only expose necessary ports
3. **Regular Updates**: Keep all dependencies up to date
4. **Access Control**: Implement proper authentication and authorization
5. **Firewall Configuration**: Restrict access to only necessary ports and services

## Scaling Considerations

For high-load scenarios:

1. **Horizontal Scaling**: Add more backend instances behind a load balancer
2. **Database Scaling**: Set up PostgreSQL replication or sharding
3. **Redis Clustering**: Implement Redis Sentinel or Redis Cluster
4. **CDN Integration**: Use a CDN for static assets
5. **Rate Limiting**: Implement rate limiting to protect against abuse

## Troubleshooting

### Common Issues

1. **Database Connection Failures**:
   - Check PostgreSQL is running: `docker ps | grep postgres`
   - Verify connection string in environment variables
   - Check network connectivity between services

2. **API Errors**:
   - Check API logs: `docker logs sankalpa_backend`
   - Verify JWT secret is properly set
   - Check CORS configuration matches your domain

3. **Frontend Issues**:
   - Verify API URL in frontend environment variables
   - Check browser console for errors
   - Verify build process completed successfully

### Getting Help

If you encounter issues not covered in this guide, please:

1. Check the [GitHub Issues](https://github.com/yourusername/sankalpa/issues) for similar problems
2. Join our [Community Discord](https://discord.gg/yourdiscord) for real-time support
3. Open a new issue with detailed information about your deployment