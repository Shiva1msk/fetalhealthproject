# Deployment Guide

## Overview

This guide covers multiple deployment options for the Fetal Health Prediction System.

## Prerequisites

- Python 3.10+
- Docker (for containerized deployment)
- Git
- Cloud platform account (for cloud deployment)

## Local Development

### 1. Clone and Setup
```bash
git clone <repository-url>
cd fetal-health-system
pip install -r requirements.txt
```

### 2. Run Applications
```bash
# Main application
python app.py

# AI Agent (in separate terminal)
python agent_app.py
```

### 3. Access Applications
- Main App: http://localhost:5000
- Agent App: http://localhost:5001

## Docker Deployment

### Single Container
```bash
# Build image
docker build -t fetal-health-app .

# Run main application
docker run -p 5000:5000 fetal-health-app

# Run agent application
docker run -p 5001:5001 -e PORT=5001 fetal-health-app gunicorn agent_app:app --bind 0.0.0.0:5001
```

### Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# With nginx proxy
docker-compose --profile production up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Cloud Deployment

### 1. Render (Recommended)

**Steps:**
1. Push code to GitHub
2. Connect repository at [render.com](https://render.com)
3. Render auto-detects `render.yaml` configuration
4. Deploy both main app and agent

**Features:**
- Free tier available
- Auto-deploys from GitHub
- SSL certificates included
- Custom domains supported

### 2. Railway

**Steps:**
1. Connect GitHub repository at [railway.app](https://railway.app)
2. Railway uses automatic detection
3. Set environment variables if needed

**Configuration:**
```bash
# Environment variables
FLASK_ENV=production
DEBUG=false
```

### 3. Heroku

**Steps:**
```bash
# Install Heroku CLI
heroku create fetal-health-app
heroku create fetal-health-agent

# Deploy main app
git push heroku main

# Deploy agent (separate app)
git subtree push --prefix=agent_app heroku-agent main
```

**Procfile Configuration:**
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### 4. Google Cloud Platform

**App Engine Deployment:**
```bash
# Install Google Cloud SDK
gcloud app deploy

# Deploy agent as separate service
gcloud app deploy agent.yaml
```

**app.yaml:**
```yaml
runtime: python310
service: default

env_variables:
  FLASK_ENV: production

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

### 5. AWS

**Elastic Beanstalk:**
```bash
# Install EB CLI
eb init fetal-health-system
eb create production
eb deploy
```

**Docker on ECS:**
```bash
# Build and push to ECR
docker build -t fetal-health-app .
docker tag fetal-health-app:latest <account>.dkr.ecr.<region>.amazonaws.com/fetal-health-app:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/fetal-health-app:latest
```

## Environment Configuration

### Required Environment Variables
```bash
# Application settings
FLASK_ENV=production
DEBUG=false
PORT=5000

# Optional settings
WORKERS=2
TIMEOUT=120
```

### Production Settings
```python
# config.py
import os

class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    
    # Database (if using)
    # DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Logging
    LOG_LEVEL = 'INFO'
```

## Security Configuration

### 1. HTTPS Setup
```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### 2. API Security
```python
# Add to app.py for production
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")
def api_predict():
    # ... existing code
```

### 3. Input Sanitization
```python
from flask import request
import bleach

def sanitize_input(data):
    """Sanitize input data."""
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, str):
        return bleach.clean(data)
    return data
```

## Monitoring and Logging

### 1. Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 2. Health Monitoring
```python
@app.route('/health')
def health_check():
    """Comprehensive health check."""
    checks = {
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'uptime': time.time() - start_time
    }
    
    # Add database check if using database
    # checks['database'] = check_database_connection()
    
    return jsonify(checks)
```

### 3. Performance Monitoring
```python
import time
from functools import wraps

def monitor_performance(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        app.logger.info(f'{f.__name__} took {end_time - start_time:.2f} seconds')
        return result
    return decorated_function

@app.route('/api/predict', methods=['POST'])
@monitor_performance
def api_predict():
    # ... existing code
```

## Scaling Considerations

### Horizontal Scaling
```yaml
# docker-compose.yml for scaling
version: '3.8'
services:
  fetal-health-app:
    build: .
    deploy:
      replicas: 3
    ports:
      - "5000-5002:5000"
```

### Load Balancing
```nginx
upstream fetal_health_backend {
    server app1:5000;
    server app2:5000;
    server app3:5000;
}

server {
    location / {
        proxy_pass http://fetal_health_backend;
    }
}
```

### Database Scaling (if needed)
```python
# For future database integration
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}
```

## Backup and Recovery

### 1. Model Backup
```bash
# Backup model files
aws s3 cp models/ s3://your-bucket/models/ --recursive

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "backup_${DATE}.tar.gz" models/ data/
aws s3 cp "backup_${DATE}.tar.gz" s3://your-backup-bucket/
```

### 2. Configuration Backup
```bash
# Backup configuration
kubectl get configmap fetal-health-config -o yaml > config-backup.yaml
```

## Troubleshooting

### Common Issues

**Model Loading Error:**
```bash
# Check model file exists and permissions
ls -la models/fetal_health.pkl
# Verify Python can import required libraries
python -c "import joblib, sklearn, numpy, pandas"
```

**Memory Issues:**
```bash
# Monitor memory usage
docker stats
# Increase container memory
docker run -m 1g fetal-health-app
```

**Port Conflicts:**
```bash
# Check port usage
netstat -tulpn | grep :5000
# Use different port
export PORT=5001
```

### Performance Optimization

**Gunicorn Configuration:**
```bash
# Optimize workers based on CPU cores
gunicorn app:app --workers $((2 * $(nproc) + 1)) --worker-class gevent
```

**Caching:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/features')
@cache.cached(timeout=3600)  # Cache for 1 hour
def get_features():
    # ... existing code
```

## Maintenance

### Regular Tasks
- Monitor application logs
- Check system resources
- Update dependencies
- Backup model files
- Review security logs
- Performance monitoring

### Updates
```bash
# Zero-downtime deployment
docker-compose pull
docker-compose up -d --no-deps --build app
```

This deployment guide ensures your Fetal Health Prediction System runs reliably in production environments.