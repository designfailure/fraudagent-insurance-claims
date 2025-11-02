# KumoRFM Insurance Claims AI Agent - Deployment Guide

This guide provides comprehensive instructions for deploying the **FraudAGENT** application in various environments, including development, staging, and production.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Production Deployment](#production-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Security Best Practices](#security-best-practices)

---

## System Requirements

### Minimum Requirements

-   **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
-   **Python**: Version 3.9, 3.10, 3.11, 3.12, or 3.13
-   **RAM**: 4 GB minimum, 8 GB recommended
-   **Disk Space**: 2 GB for application and dependencies
-   **Network**: Internet connection for API calls to KumoRFM and OpenAI

### Python Dependencies

All dependencies are listed in `requirements.txt`:

```
pandas>=2.0.0
numpy>=1.24.0
pyarrow>=12.0.0
kumoai>=2.7.0
openai>=1.12.0
gradio>=4.0.0
python-dotenv>=1.0.0
matplotlib>=3.7.0
plotly>=5.14.0
jsonschema>=4.17.0
```

---

## Installation Methods

### Method 1: Automated Setup (Recommended)

**Windows (PowerShell)**

1.  Open PowerShell as Administrator (optional, but recommended).
2.  Navigate to the project directory:
    ```powershell
    cd path\to\insurance-claims-kumo-agent
    ```
3.  Run the launcher:
    ```powershell
    .\launch.ps1
    ```

The script will:
-   Create a virtual environment (`venv`)
-   Install all dependencies
-   Check for `.env` configuration
-   Launch the application

**Linux/macOS (Bash)**

1.  Open Terminal.
2.  Navigate to the project directory:
    ```bash
    cd path/to/insurance-claims-kumo-agent
    ```
3.  Create and run a launcher script:
    ```bash
    chmod +x launch.sh  # If you created launch.sh
    ./launch.sh
    ```

Or run commands manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Method 2: Docker Deployment (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Gradio port
EXPOSE 7860

# Set environment variables (override with docker run -e)
ENV APP_HOST=0.0.0.0
ENV APP_PORT=7860

# Run application
CMD ["python", "main.py"]
```

Build and run:
```bash
# Build image
docker build -t fraudagent:latest .

# Run container
docker run -d \
  -p 7860:7860 \
  -e KUMO_API_KEY=your-kumo-key \
  -e OPENAI_API_KEY=your-openai-key \
  -v $(pwd)/data:/app/data \
  --name fraudagent \
  fraudagent:latest
```

---

## Configuration

### Environment Variables

All configuration is managed through the `.env` file. Copy `.env.template` to `.env` and configure:

```ini
# Required API Keys
KUMO_API_KEY=your-kumo-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Data Configuration
INSURANCE_DATA_PATH=data/insurance_claims_data.parquet

# OpenAI Model Selection
OPENAI_MODEL=gpt-4o-mini  # or gpt-4o for higher accuracy

# Server Configuration
APP_HOST=0.0.0.0
APP_PORT=7860
GRADIO_SHARE=false  # Set to true for public URL

# Optional Settings
LOG_LEVEL=INFO
MAX_QUERY_HISTORY=100
```

### Data Preparation

1.  **Parquet Format**: Ensure your insurance claims data is in Parquet format.
2.  **Schema Requirements**:
    -   At least one table with a primary key (e.g., `claim_id`, `customer_id`)
    -   Temporal columns for time-based predictions (e.g., `claim_date`)
    -   Fraud indicators (e.g., `fraud_flag`)
3.  **File Placement**: Place data files in the `data/` directory.

Example data structure:
```
data/
├── customers.parquet       # Customer information
├── claims.parquet          # Claims data
└── policies.parquet        # Policy information (optional)
```

---

## Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\Activate.ps1  # Windows

# Run with debug logging
LOG_LEVEL=DEBUG python main.py
```

### Production Mode

```bash
# Set production environment variables
export GRADIO_SHARE=false
export LOG_LEVEL=WARNING

# Run application
python main.py
```

### Running as a Service (Linux)

Create a systemd service file `/etc/systemd/system/fraudagent.service`:

```ini
[Unit]
Description=FraudAGENT - KumoRFM Insurance Claims AI Agent
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/insurance-claims-kumo-agent
Environment="PATH=/path/to/insurance-claims-kumo-agent/venv/bin"
EnvironmentFile=/path/to/insurance-claims-kumo-agent/.env
ExecStart=/path/to/insurance-claims-kumo-agent/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fraudagent
sudo systemctl start fraudagent
sudo systemctl status fraudagent
```

---

## Production Deployment

### Reverse Proxy with Nginx

Configure Nginx to proxy requests to the Gradio app:

```nginx
server {
    listen 80;
    server_name fraudagent.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support for Gradio
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### SSL/TLS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d fraudagent.yourdomain.com
```

### Load Balancing (Multiple Instances)

Run multiple instances on different ports and use Nginx for load balancing:

```nginx
upstream fraudagent_backend {
    server 127.0.0.1:7860;
    server 127.0.0.1:7861;
    server 127.0.0.1:7862;
}

server {
    listen 80;
    server_name fraudagent.yourdomain.com;

    location / {
        proxy_pass http://fraudagent_backend;
        # ... (same proxy settings as above)
    }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'gradio'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. API Key Errors

**Error**: `KUMO_API_KEY environment variable not set`

**Solution**:
-   Verify `.env` file exists in the project root
-   Check that API keys are correctly set (no quotes needed)
-   Ensure `.env` is loaded (use `python-dotenv`)

#### 3. Data Loading Errors

**Error**: `FileNotFoundError: Data path not found`

**Solution**:
-   Check `INSURANCE_DATA_PATH` in `.env`
-   Verify data files exist in the specified location
-   Ensure Parquet files are valid (test with `pd.read_parquet()`)

#### 4. Port Already in Use

**Error**: `OSError: [Errno 98] Address already in use`

**Solution**:
```bash
# Find process using port 7860
lsof -i :7860  # Linux/macOS
netstat -ano | findstr :7860  # Windows

# Kill the process or change APP_PORT in .env
```

#### 5. KumoRFM SDK Import Issues

**Error**: `Failed to import KumoRFM SDK`

**Solution**:
-   The `kumo_setup.py` module tries multiple import patterns
-   Ensure `kumoai>=2.7.0` is installed: `pip install --upgrade kumoai`
-   Check SDK documentation for latest import syntax

---

## Security Best Practices

### 1. API Key Management

-   **Never commit `.env` to version control**: Add `.env` to `.gitignore`
-   **Use environment-specific keys**: Different keys for dev/staging/prod
-   **Rotate keys regularly**: Update API keys every 90 days
-   **Use secrets management**: Consider AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault for production

### 2. Network Security

-   **Restrict access**: Use firewall rules to limit access to trusted IPs
-   **Enable HTTPS**: Always use SSL/TLS in production
-   **Disable public sharing**: Set `GRADIO_SHARE=false` unless needed

### 3. Data Security

-   **Encrypt data at rest**: Use encrypted file systems or databases
-   **Sanitize inputs**: Validate all user inputs before processing
-   **Audit logging**: Enable comprehensive logging for security audits

### 4. Application Security

-   **Keep dependencies updated**: Regularly run `pip list --outdated`
-   **Use virtual environments**: Isolate dependencies
-   **Implement rate limiting**: Prevent abuse of API endpoints
-   **Monitor usage**: Track API calls and costs

---

## Performance Optimization

### 1. Caching

Implement caching for frequently used queries:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_prediction(pql_query: str):
    return kumo_client.execute_pql(pql_query)
```

### 2. Async Processing

For high-concurrency scenarios, consider async execution:

```python
import asyncio

async def async_predict(query):
    # Implement async prediction logic
    pass
```

### 3. Database Backend

For large-scale deployments, use a database to store:
-   Query history
-   User sessions
-   Cached results

---

## Monitoring and Maintenance

### Logging

The application uses Python's `logging` module. Configure log level via `LOG_LEVEL` in `.env`.

### Metrics to Monitor

-   **API call latency**: Track response times for KumoRFM and OpenAI
-   **Error rates**: Monitor failed predictions and translations
-   **Resource usage**: CPU, memory, and disk usage
-   **User activity**: Track query patterns and usage trends

### Backup and Recovery

-   **Regular backups**: Back up `.env`, data files, and query history
-   **Version control**: Use Git for code versioning
-   **Disaster recovery plan**: Document recovery procedures

---

## Support and Resources

-   **KumoRFM Documentation**: [https://kumo-ai.github.io/kumo-sdk/](https://kumo-ai.github.io/kumo-sdk/)
-   **OpenAI API Docs**: [https://platform.openai.com/docs](https://platform.openai.com/docs)
-   **Gradio Documentation**: [https://www.gradio.app/docs](https://www.gradio.app/docs)

For issues specific to this application, refer to the project repository or contact your system administrator.
