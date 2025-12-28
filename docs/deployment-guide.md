# Sankalpa Deployment Guide

This comprehensive guide provides step-by-step instructions for deploying Sankalpa in various environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
   - [AWS](#aws-deployment)
   - [Azure](#azure-deployment)
   - [Google Cloud](#google-cloud-deployment)
5. [Kubernetes Deployment](#kubernetes-deployment)
6. [Vercel Deployment](#vercel-deployment)
7. [Configuration Options](#configuration-options)
8. [Security Considerations](#security-considerations)
9. [Monitoring and Maintenance](#monitoring-and-maintenance)
10. [Troubleshooting](#troubleshooting)

## Prerequisites

Before deploying Sankalpa, ensure you have the following:

- **For local development:**
  - Python 3.10 or higher
  - Node.js 18 or higher
  - PostgreSQL 14 or higher (optional for production)
  - Redis 7 or higher (optional for production)

- **For production deployment:**
  - Docker and Docker Compose
  - Domain name (for SSL/TLS)
  - SMTP server details (for notifications)
  - OpenAI API key (for natural language features)

## Local Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/sankalpa.git
cd sankalpa
```

### Step 2: Set Up Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit the environment variables
nano .env
```

Important variables to configure:

```
# API Settings
SANKALPA_API_PORT=8000
SANKALPA_DEBUG=true
SANKALPA_LOG_LEVEL=INFO
SANKALPA_ALLOWED_ORIGINS=http://localhost:3000

# Security
SANKALPA_JWT_SECRET=your_secure_random_secret

# Database (if using)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=sankalpa
POSTGRES_HOST=localhost

# Redis (if using)
REDIS_URL=redis://localhost:6379/0

# OpenAI (for NLP features)
OPENAI_API_KEY=your_openai_api_key
```

### Step 3: Backend Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (if using database)
python -m alembic upgrade head

# Start the backend
python -m sankalpa.backend.enhanced_main
```

### Step 4: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### Step 5: Access the Application

Open your browser and navigate to:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/api/docs

## Docker Deployment

### Step 1: Configure Environment

```bash
# Copy example environment file
cp .env.example .env.production

# Edit the environment variables
nano .env.production
```

### Step 2: Build and Run with Docker Compose

```bash
# Build the containers
docker-compose -f docker-compose.yml --env-file .env.production build

# Start the services
docker-compose -f docker-compose.yml --env-file .env.production up -d

# Check status
docker-compose ps
```

### Step 3: Run Database Migrations

```bash
docker-compose exec backend python -m alembic upgrade head
```

### Step 4: Create Initial Admin User

```bash
docker-compose exec backend python -m scripts.create_admin
```

### Step 5: Access the Application

Open your browser and navigate to:
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/api/docs

## Cloud Deployment

### AWS Deployment

#### Using AWS ECS

1. **Set up an ECS cluster:**
   ```bash
   aws ecs create-cluster --cluster-name sankalpa-cluster
   ```

2. **Create task definitions:**
   ```bash
   aws ecs register-task-definition --cli-input-json file://aws/task-definition.json
   ```

3. **Create an ALB:**
   ```bash
   aws elbv2 create-load-balancer --name sankalpa-lb --subnets subnet-xxxx subnet-yyyy
   ```

4. **Create ECS services:**
   ```bash
   aws ecs create-service --cluster sankalpa-cluster --service-name sankalpa-service --task-definition sankalpa:1 --desired-count 2 --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:region:xxxx:targetgroup/sankalpa-tg/1234,containerName=sankalpa,containerPort=8000 --launch-type FARGATE
   ```

#### Using Elastic Beanstalk

1. **Initialize EB CLI:**
   ```bash
   eb init -p docker sankalpa
   ```

2. **Create environment:**
   ```bash
   eb create sankalpa-production
   ```

3. **Deploy:**
   ```bash
   eb deploy
   ```

### Azure Deployment

#### Using Azure Container Apps

1. **Create resource group:**
   ```bash
   az group create --name sankalpa-group --location eastus
   ```

2. **Create container app environment:**
   ```bash
   az containerapp env create --name sankalpa-env --resource-group sankalpa-group --location eastus
   ```

3. **Create container apps:**
   ```bash
   az containerapp create --name sankalpa-backend --resource-group sankalpa-group --environment sankalpa-env --image ghcr.io/yourusername/sankalpa-backend:latest --target-port 8000 --ingress external
   
   az containerapp create --name sankalpa-frontend --resource-group sankalpa-group --environment sankalpa-env --image ghcr.io/yourusername/sankalpa-frontend:latest --target-port 3000 --ingress external
   ```

### Google Cloud Deployment

#### Using Google Cloud Run

1. **Push images to GCR:**
   ```bash
   docker push gcr.io/your-project/sankalpa-backend
   docker push gcr.io/your-project/sankalpa-frontend
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy sankalpa-backend --image gcr.io/your-project/sankalpa-backend --platform managed --region us-central1 --allow-unauthenticated
   
   gcloud run deploy sankalpa-frontend --image gcr.io/your-project/sankalpa-frontend --platform managed --region us-central1 --allow-unauthenticated
   ```

## Kubernetes Deployment

### Step 1: Create Kubernetes Namespace

```bash
kubectl create namespace sankalpa
```

### Step 2: Create ConfigMaps and Secrets

```bash
# Create secret from .env.production
kubectl create secret generic sankalpa-config --from-env-file=.env.production --namespace=sankalpa

# Create TLS secret for HTTPS
kubectl create secret tls sankalpa-tls --cert=path/to/tls.crt --key=path/to/tls.key --namespace=sankalpa
```

### Step 3: Apply Kubernetes Manifests

```bash
kubectl apply -f k8s/database.yaml --namespace=sankalpa
kubectl apply -f k8s/redis.yaml --namespace=sankalpa
kubectl apply -f k8s/backend.yaml --namespace=sankalpa
kubectl apply -f k8s/frontend.yaml --namespace=sankalpa
kubectl apply -f k8s/ingress.yaml --namespace=sankalpa
```

### Step 4: Verify Deployment

```bash
kubectl get all --namespace=sankalpa
```

### Step 5: Run Database Migrations

```bash
kubectl exec -it $(kubectl get pod -l app=sankalpa-backend -n sankalpa -o jsonpath="{.items[0].metadata.name}") -n sankalpa -- python -m alembic upgrade head
```

## Vercel Deployment

### Step 1: Deploy the Backend

Follow either the Docker, AWS, Azure, or GCP deployment guides for the backend.

### Step 2: Configure Vercel for Frontend

1. Push your code to GitHub, GitLab, or Bitbucket
2. Import the project in Vercel
3. Configure environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```
4. Deploy

### Step 3: Set Up Custom Domain

1. In Vercel dashboard, go to project settings
2. Add your custom domain
3. Configure DNS settings as instructed

## Configuration Options

### Core Configuration

Key configuration options in `.env` file:

- `SANKALPA_ENV`: Environment (`development`, `test`, `production`)
- `SANKALPA_API_PORT`: API server port
- `SANKALPA_ALLOWED_ORIGINS`: CORS origins (comma-separated)
- `SANKALPA_JWT_SECRET`: Secret for JWT tokens
- `SANKALPA_LOG_LEVEL`: Logging level

### Database Configuration

- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port (default: 5432)

### Redis Configuration

- `REDIS_URL`: Redis connection URL

### Feature Flags

- `ENABLE_NLP_FEATURES`: Enable natural language processing features
- `ENABLE_MARKETPLACE`: Enable marketplace features
- `ENABLE_MULTI_TENANT`: Enable multi-tenant features

## Security Considerations

### API Security Measures

1. **JWT Authentication:**
   - Use strong secrets
   - Set appropriate token expiration
   - Implement refresh token rotation

2. **CORS Configuration:**
   - Restrict to known domains only
   - Disable credentials for public APIs

3. **Rate Limiting:**
   - Configure appropriate limits per IP and user
   - Implement progressive throttling

### Database Security

1. **Connection Security:**
   - Use SSL/TLS for database connections
   - Implement connection pooling with timeouts

2. **Credential Management:**
   - Use environment variables for credentials
   - Rotate credentials regularly

3. **Data Protection:**
   - Encrypt sensitive data at rest
   - Implement proper backup procedures

### Frontend Security

1. **Content Security Policy:**
   - Restrict sources for scripts, styles, and other content
   - Implement strict CSP rules

2. **Token Storage:**
   - Store tokens in HttpOnly cookies
   - Implement proper CSRF protection

3. **Input Validation:**
   - Validate all user inputs
   - Sanitize data before rendering

## Monitoring and Maintenance

### Health Checks

Configure health check endpoints:
- `/api/health`: API server health
- `/api/metrics`: System metrics

### Logging

Configure structured logging:
- Development: Console output
- Production: JSON format to log aggregation service

### Backup Procedures

1. **Database Backups:**
   ```bash
   # Set up daily backups
   cat > /usr/local/bin/backup-sankalpa-db.sh << 'EOF'
   #!/bin/bash
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   pg_dump -U postgres -d sankalpa | gzip > /backups/sankalpa_${TIMESTAMP}.sql.gz
   # Keep last 30 days
   find /backups -name "sankalpa_*.sql.gz" -mtime +30 -delete
   EOF
   chmod +x /usr/local/bin/backup-sankalpa-db.sh
   
   # Add to crontab (daily at 3 AM)
   (crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/backup-sankalpa-db.sh") | crontab -
   ```

2. **File Backups:**
   ```bash
   # Back up user uploads
   rsync -avz /path/to/uploads/ /backups/uploads/
   ```

### Upgrades

Follow this procedure for upgrades:

1. Review release notes
2. Back up all data
3. Apply database migrations
4. Deploy new version
5. Verify functionality
6. Update documentation

## Troubleshooting

### Common Issues

1. **Database Connection Issues:**
   - Check database credentials and connection string
   - Verify network connectivity
   - Check database logs for errors

2. **API Errors:**
   - Check API logs (`/var/log/sankalpa/api.log`)
   - Verify environment variables
   - Check permissions on files and directories

3. **Frontend Issues:**
   - Check browser console for errors
   - Verify API URL configuration
   - Clear browser cache and reload

### Logs Location

- API Logs: `/var/log/sankalpa/api.log`
- Frontend Logs: Browser console or Vercel logs
- Database Logs: PostgreSQL logs
- Redis Logs: Redis server logs

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search for similar issues in [GitHub Issues](https://github.com/yourusername/sankalpa/issues)
3. Join our [Discord Community](https://discord.gg/sankalpa) for real-time help
4. Contact us at support@example.com