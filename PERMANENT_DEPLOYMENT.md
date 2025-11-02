# FraudAGENT - Permanent Deployment Guide

This guide provides comprehensive instructions for deploying the **FraudAGENT** application permanently across various platforms. Choose the deployment method that best fits your needs, infrastructure, and budget.

---

## 📋 Table of Contents

1.  [Deployment Options Overview](#deployment-options-overview)
2.  [Quick Start with Docker](#quick-start-with-docker)
3.  [Cloud Platform Deployments](#cloud-platform-deployments)
4.  [VPS and Self-Hosted Options](#vps-and-self-hosted-options)
5.  [Platform-as-a-Service (PaaS) Options](#platform-as-a-service-paas-options)
6.  [Production Best Practices](#production-best-practices)
7.  [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Deployment Options Overview

The table below summarizes the available deployment options, ordered from simplest to most complex.

| Platform | Complexity | Cost | Scalability | Use Case |
|----------|-----------|------|-------------|----------|
| **Docker (Local/VPS)** | ⭐ Low | $ | Manual | Development, small deployments |
| **Railway** | ⭐ Very Low | $$ | Auto | Quick production deployment |
| **Render** | ⭐ Very Low | $$ | Auto | Simple production apps |
| **Heroku** | ⭐⭐ Low | $$$ | Auto | Traditional PaaS deployment |
| **AWS App Runner** | ⭐⭐ Low | $$ | Auto | Serverless container deployment |
| **Google Cloud Run** | ⭐⭐ Low | $ | Auto | **Recommended** - Cost-effective, serverless |
| **Azure Container Instances** | ⭐⭐ Low | $$ | Manual | Simple Azure deployment |
| **DigitalOcean App Platform** | ⭐⭐ Low | $$ | Auto | Developer-friendly PaaS |
| **AWS ECS Fargate** | ⭐⭐⭐ Medium | $$$ | Auto | Enterprise AWS deployment |
| **Azure App Service** | ⭐⭐⭐ Medium | $$$ | Auto | Enterprise Azure deployment |
| **Google Kubernetes Engine** | ⭐⭐⭐⭐ High | $$$$ | Auto | Complex, large-scale apps |

**Legend**: $ = Low cost, $$ = Medium cost, $$$ = Higher cost, $$$$ = Highest cost

---

## Quick Start with Docker

The fastest way to deploy FraudAGENT is using Docker on any server with Docker installed.

### Prerequisites

-   A server (VPS, cloud VM, or local machine) with:
    -   Docker and Docker Compose installed
    -   At least 2 GB RAM
    -   Port 7860 accessible

### Deployment Steps

1.  **Clone the repository**:
    ```bash
    git clone https://your-repo-url/insurance-claims-kumo-agent.git
    cd insurance-claims-kumo-agent
    ```

2.  **Configure environment**:
    ```bash
    cp .env.template .env
    nano .env  # Edit and add your API keys
    ```

3.  **Run the automated deployment script**:
    ```bash
    chmod +x deploy.sh
    ./deploy.sh
    ```

4.  **Access the application**:
    -   Local: `http://localhost:7860`
    -   Network: `http://YOUR_SERVER_IP:7860`

### Docker Commands Reference

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# View running containers
docker-compose ps
```

---

## Cloud Platform Deployments

For production deployments, cloud platforms offer managed infrastructure, automatic scaling, and integrated monitoring.

### ☁️ Google Cloud Run (Recommended)

**Why Cloud Run?**
-   Fully managed serverless platform
-   Scales to zero (no cost when idle)
-   Automatic HTTPS
-   Pay only for what you use

**Deployment Steps**:

See the detailed guide in [`DEPLOY_GCP.md`](DEPLOY_GCP.md).

**Quick Deploy**:
```bash
# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/fraudagent

# Deploy to Cloud Run
gcloud run deploy fraudagent \
    --image gcr.io/YOUR_PROJECT/fraudagent \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 7860 \
    --set-secrets=KUMO_API_KEY=KUMO_API_KEY:latest,OPENAI_API_KEY=OPENAI_API_KEY:latest
```

**Estimated Cost**: $0-$20/month for low to medium traffic.

---

### ☁️ AWS App Runner

**Why App Runner?**
-   Simplest AWS deployment option
-   Automatic scaling and load balancing
-   Integrated with AWS services

**Deployment Steps**:

See the detailed guide in [`DEPLOY_AWS.md`](DEPLOY_AWS.md).

**Estimated Cost**: $5-$50/month depending on usage.

---

### ☁️ Azure Container Instances

**Why Azure Container Instances?**
-   Quick deployment without managing VMs
-   Integrated with Azure ecosystem
-   Pay-per-second billing

**Deployment Steps**:

See the detailed guide in [`DEPLOY_AZURE.md`](DEPLOY_AZURE.md).

**Estimated Cost**: $10-$40/month for continuous operation.

---

## VPS and Self-Hosted Options

For full control over your infrastructure, deploy to a Virtual Private Server (VPS).

### 🖥️ DigitalOcean Droplet

1.  **Create a Droplet**:
    -   Choose Ubuntu 22.04 LTS
    -   Select at least the $12/month plan (2 GB RAM)
    -   Add your SSH key

2.  **SSH into your Droplet**:
    ```bash
    ssh root@YOUR_DROPLET_IP
    ```

3.  **Install Docker**:
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo apt-get install docker-compose
    ```

4.  **Deploy the application** (follow the Docker Quick Start steps above).

5.  **Configure a domain and SSL**:
    -   Point your domain to the Droplet's IP
    -   Use Certbot to obtain a free SSL certificate
    -   Configure Nginx as a reverse proxy (see `nginx.conf`)

**Estimated Cost**: $12-$24/month.

---

### 🖥️ Linode, Vultr, or Other VPS Providers

The deployment process is identical to DigitalOcean. Simply:
1.  Create a Linux VM (Ubuntu 22.04 recommended)
2.  Install Docker and Docker Compose
3.  Clone the repository and run `deploy.sh`

---

## Platform-as-a-Service (PaaS) Options

PaaS platforms abstract away infrastructure management, allowing you to focus on your application.

### 🚂 Railway (Easiest PaaS)

**Why Railway?**
-   Zero-configuration deployments
-   Free tier available
-   Automatic HTTPS and custom domains
-   GitHub integration for CI/CD

**Deployment Steps**:

1.  **Sign up** at [railway.app](https://railway.app)
2.  **Create a new project** from your GitHub repository
3.  **Add environment variables** in the Railway dashboard:
    -   `KUMO_API_KEY`
    -   `OPENAI_API_KEY`
    -   `PORT=7860`
4.  Railway will automatically detect the `Dockerfile` and deploy

**Estimated Cost**: Free tier available, then $5-$20/month.

---

### 🎨 Render

**Why Render?**
-   Simple, modern PaaS
-   Free tier for web services
-   Automatic SSL and custom domains

**Deployment Steps**:

1.  **Sign up** at [render.com](https://render.com)
2.  **Create a new Web Service** from your GitHub repository
3.  **Configure**:
    -   Environment: Docker
    -   Add environment variables
4.  Render will build and deploy automatically

**Estimated Cost**: Free tier available, then $7-$25/month.

---

### 🟣 Heroku

**Why Heroku?**
-   Mature, well-documented platform
-   Extensive add-on ecosystem
-   Easy rollbacks and staging environments

**Deployment Steps**:

1.  **Install the Heroku CLI** and log in
2.  **Create a Heroku app**:
    ```bash
    heroku create fraudagent-app
    ```
3.  **Set environment variables**:
    ```bash
    heroku config:set KUMO_API_KEY=your-key
    heroku config:set OPENAI_API_KEY=your-key
    ```
4.  **Deploy**:
    ```bash
    git push heroku main
    ```

**Estimated Cost**: $7-$50/month (no free tier as of 2022).

---

## Production Best Practices

### 1. Secrets Management

**Never commit secrets to version control**. Use platform-specific secret management:

-   **AWS**: AWS Secrets Manager
-   **Azure**: Azure Key Vault
-   **GCP**: Google Secret Manager
-   **Docker**: Docker Secrets or environment variables
-   **PaaS**: Platform environment variables

### 2. Custom Domain and SSL

-   Register a domain name (e.g., `fraudagent.yourdomain.com`)
-   Configure DNS to point to your deployment
-   Enable HTTPS using:
    -   **Cloud platforms**: Automatic SSL (Cloud Run, App Runner, etc.)
    -   **VPS**: Certbot with Let's Encrypt
    -   **PaaS**: Built-in SSL (Railway, Render, Heroku)

### 3. Monitoring and Logging

-   **Application logs**: Use `docker-compose logs` or platform-specific logging
-   **Uptime monitoring**: Use services like UptimeRobot, Pingdom, or cloud-native monitoring
-   **Error tracking**: Integrate Sentry or similar services
-   **Performance monitoring**: Use APM tools like New Relic or Datadog

### 4. Backup and Disaster Recovery

-   **Data backups**: Regularly back up your data directory
-   **Configuration backups**: Store `.env` and configuration files securely
-   **Version control**: Use Git for code versioning
-   **Disaster recovery plan**: Document recovery procedures

### 5. Scaling Considerations

-   **Horizontal scaling**: Deploy multiple instances behind a load balancer
-   **Vertical scaling**: Increase CPU and memory resources
-   **Database**: For high traffic, consider moving to a managed database for query history
-   **Caching**: Implement Redis or similar for frequently accessed data

---

## Monitoring and Maintenance

### Health Checks

The application includes a built-in health check endpoint. Configure your platform to monitor it:

-   **Endpoint**: `http://your-app-url:7860/`
-   **Expected response**: HTTP 200
-   **Check interval**: Every 30 seconds

### Log Monitoring

Monitor application logs for:
-   API errors (KumoRFM or OpenAI)
-   PQL execution failures
-   High latency warnings
-   Unusual traffic patterns

### Regular Maintenance

-   **Update dependencies**: Run `pip list --outdated` monthly
-   **Security patches**: Update base Docker image regularly
-   **API key rotation**: Rotate API keys every 90 days
-   **Performance review**: Monitor response times and optimize as needed

---

## Cost Comparison

Here's a rough monthly cost estimate for different deployment options (based on moderate usage):

| Platform | Monthly Cost | Notes |
|----------|-------------|-------|
| **VPS (DigitalOcean, Linode)** | $12-$24 | Fixed cost, predictable |
| **Railway** | $5-$20 | Pay-per-use, free tier available |
| **Render** | $7-$25 | Free tier, then flat rate |
| **Google Cloud Run** | $0-$20 | Scales to zero, very cost-effective |
| **AWS App Runner** | $5-$50 | Pay-per-use |
| **Azure Container Instances** | $10-$40 | Pay-per-second |
| **Heroku** | $7-$50 | Flat rate, no free tier |
| **AWS ECS Fargate** | $30-$100+ | Enterprise-grade |

*Costs vary based on traffic, compute resources, and data transfer.*

---

## Support and Resources

-   **Docker Documentation**: [docs.docker.com](https://docs.docker.com)
-   **AWS Documentation**: [docs.aws.amazon.com](https://docs.aws.amazon.com)
-   **Azure Documentation**: [docs.microsoft.com/azure](https://docs.microsoft.com/azure)
-   **GCP Documentation**: [cloud.google.com/docs](https://cloud.google.com/docs)
-   **Railway Docs**: [docs.railway.app](https://docs.railway.app)
-   **Render Docs**: [render.com/docs](https://render.com/docs)

For application-specific issues, refer to the main [README.md](README.md) and [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
