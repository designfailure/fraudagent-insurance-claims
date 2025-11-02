# FraudAGENT - Google Cloud Platform (GCP) Deployment Guide

This guide provides detailed instructions for deploying the **FraudAGENT** application to Google Cloud Platform (GCP). It covers three primary deployment methods: Compute Engine, Cloud Run, and Google Kubernetes Engine (GKE).

---

## 📋 Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Secrets Management with Google Secret Manager](#secrets-management)
3.  [Deployment Options Overview](#deployment-options-overview)
4.  [**Option 1: Deploy to Compute Engine**](#option-1-deploy-to-compute-engine)
5.  [**Option 2: Deploy to Cloud Run**](#option-2-deploy-to-cloud-run) (Recommended for Production)
6.  [**Option 3: Deploy to Google Kubernetes Engine (GKE)**](#option-3-deploy-to-google-kubernetes-engine-gke)
7.  [Cost Considerations](#cost-considerations)

---

## Prerequisites

-   **GCP Account**: An active GCP project.
-   **gcloud CLI**: The Google Cloud CLI installed and configured. [Installation Guide](https://cloud.google.com/sdk/docs/install)
-   **Docker**: Docker Desktop or Docker Engine installed.
-   **Git**: Git installed on your local machine.

---

## Secrets Management

Use **Google Secret Manager** to securely manage your API keys.

### Step 1: Create Secrets

1.  Navigate to the **Secret Manager** page in the Google Cloud Console.
2.  Click **Create secret**.
3.  Create two secrets:
    -   Name: `KUMO_API_KEY`, Value: `your-kumo-api-key-here`
    -   Name: `OPENAI_API_KEY`, Value: `your-openai-api-key-here`

### Step 2: Grant Access

Grant the service account of your deployment resource (Compute Engine, Cloud Run, etc.) the **Secret Manager Secret Accessor** IAM role.

---

## Deployment Options Overview

| Option | Description | Use Case | Complexity | Cost Model |
|---|---|---|---|---|
| **Compute Engine** | Deploy on a virtual machine. | Simple deployments, testing. | Low | Pay per hour for the VM. |
| **Cloud Run** | Fully managed serverless platform for containers. | **Recommended for production**. Scales to zero, cost-effective. | Very Low | Pay per vCPU-second and GB-second. |
| **GKE** | Managed Kubernetes service. | Complex, large-scale applications requiring orchestration. | High | Pay for GKE cluster management and worker nodes. |

---

## Option 1: Deploy to Compute Engine

### Step 1: Create a VM Instance

1.  In the GCP Console, go to **Compute Engine** -> **VM instances** and click **Create Instance**.
2.  **Machine type**: `e2-medium` or larger.
3.  **Boot disk**: Choose **Container-Optimized OS**.
4.  **Firewall**: Allow HTTP and HTTPS traffic.
5.  **Service account**: Use the default Compute Engine service account or create a new one. Grant it the Secret Manager role.

### Step 2: Deploy the Application

1.  SSH into your VM.
2.  Use the `gcloud` CLI to fetch secrets and create a `.env` file.
3.  Clone your repository.
4.  Run with Docker Compose:
    ```bash
    docker-compose up -d
    ```

### Step 3: Configure DNS and SSL

Follow the same steps as in the EC2 guide to configure a static IP, Cloud DNS, a Google-managed SSL certificate with a Load Balancer, or use Nginx and Certbot.

---

## Option 2: Deploy to Cloud Run

### Step 1: Push Docker Image to Artifact Registry

1.  Enable the Artifact Registry API.
2.  Create a Docker repository in Artifact Registry.
3.  Configure Docker to authenticate with Artifact Registry:
    ```bash
    gcloud auth configure-docker YOUR_REGION-docker.pkg.dev
    ```
4.  Tag and push your image:
    ```bash
    docker tag fraudagent:latest YOUR_REGION-docker.pkg.dev/YOUR_PROJECT/YOUR_REPO/fraudagent:latest
    docker push YOUR_REGION-docker.pkg.dev/YOUR_PROJECT/YOUR_REPO/fraudagent:latest
    ```

### Step 2: Deploy to Cloud Run

Deploy using the `gcloud` CLI:

```bash
gcloud run deploy fraudagent-service \
    --image YOUR_REGION-docker.pkg.dev/YOUR_PROJECT/YOUR_REPO/fraudagent:latest \
    --platform managed \
    --region YOUR_REGION \
    --port 7860 \
    --allow-unauthenticated \
    --set-secrets=KUMO_API_KEY=KUMO_API_KEY:latest,OPENAI_API_KEY=OPENAI_API_KEY:latest
```

This command:
-   Deploys your container image.
-   Exposes port 7860.
-   Allows public access.
-   Securely mounts your secrets from Secret Manager as environment variables.

### Step 3: Access the Application

Cloud Run will provide a stable public URL to access your service. You can also map a custom domain in the Cloud Run console.

---

## Option 3: Deploy to Google Kubernetes Engine (GKE)

### Step 1: Create a GKE Cluster

Create a GKE cluster, either Autopilot (serverless) or Standard.

### Step 2: Create Kubernetes Manifests

Create `deployment.yaml` and `service.yaml` files.

**deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fraudagent-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fraudagent
  template:
    metadata:
      labels:
        app: fraudagent
    spec:
      containers:
      - name: fraudagent
        image: YOUR_REGION-docker.pkg.dev/YOUR_PROJECT/YOUR_REPO/fraudagent:latest
        ports:
        - containerPort: 7860
        env:
        - name: KUMO_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: kumo-api-key
        # ... and so on for other secrets
```

**service.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fraudagent-service
spec:
  type: LoadBalancer
  selector:
    app: fraudagent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 7860
```

### Step 3: Deploy

1.  Create Kubernetes secrets from your secrets in Secret Manager (or use Workload Identity for a more secure approach).
2.  Apply the manifests:
    ```bash
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

---

## Cost Considerations

-   **Compute Engine**: Pay for the VM while it's running.
-   **Cloud Run**: Generous free tier. Pay-per-use model makes it very cost-effective for apps with variable traffic.
-   **GKE**: Can be expensive. Best for large, complex applications that need the power of Kubernetes.

Always use the [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator) to estimate costs.
