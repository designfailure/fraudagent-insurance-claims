# FraudAGENT - Microsoft Azure Deployment Guide

This guide provides detailed instructions for deploying the **FraudAGENT** application to Microsoft Azure. It covers three primary deployment methods: Azure Virtual Machines, Azure Container Instances (ACI), and Azure App Service.

---

## 📋 Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Secrets Management with Azure Key Vault](#secrets-management)
3.  [Deployment Options Overview](#deployment-options-overview)
4.  [**Option 1: Deploy to Azure Virtual Machine**](#option-1-deploy-to-azure-virtual-machine)
5.  [**Option 2: Deploy to Azure Container Instances (ACI)**](#option-2-deploy-to-azure-container-instances-aci) (Easiest)
6.  [**Option 3: Deploy to Azure App Service for Containers**](#option-3-deploy-to-azure-app-service-for-containers) (Recommended for Production)
7.  [Cost Considerations](#cost-considerations)

---

## Prerequisites

-   **Azure Account**: An active Azure subscription.
-   **Azure CLI**: The Azure Command Line Interface installed and configured. [Installation Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
-   **Docker**: Docker Desktop or Docker Engine installed.
-   **Git**: Git installed on your local machine.

---

## Secrets Management

Use **Azure Key Vault** to securely manage your API keys.

### Step 1: Create a Key Vault and Store Secrets

1.  Navigate to the **Azure Key Vault** service in the Azure portal.
2.  Create a new Key Vault.
3.  Go to **Secrets** and click **Generate/Import**.
4.  Create two secrets:
    -   Name: `KUMO-API-KEY`, Value: `your-kumo-api-key-here`
    -   Name: `OPENAI-API-KEY`, Value: `your-openai-api-key-here`

### Step 2: Grant Access

You will need to grant your deployment resource (VM, App Service, etc.) a managed identity and then create an access policy in Key Vault to allow that identity to read the secrets.

---

## Deployment Options Overview

| Option | Description | Use Case | Complexity | Cost Model |
|---|---|---|---|---|
| **Azure VM** | Deploy on a virtual machine. Full OS control. | Simple deployments, testing. | Low | Pay per hour for the VM. |
| **ACI** | Run containers without managing servers. | **Easiest option**. Quick tests, simple tasks. | Very Low | Pay per second for vCPU and memory. |
| **App Service** | Fully managed platform for web apps. | **Recommended for production**. Scalable, integrated with CI/CD, custom domains, SSL. | Medium | Pay for the App Service Plan. |

---

## Option 1: Deploy to Azure Virtual Machine

### Step 1: Create a Virtual Machine

1.  In the Azure portal, create a new **Virtual Machine**.
2.  **Image**: Choose **Ubuntu Server 22.04 LTS**.
3.  **Size**: Select `Standard_B2s` or larger.
4.  **Authentication**: Use an SSH public key.
5.  **Inbound port rules**: Allow SSH (22), HTTP (80), and HTTPS (443).
6.  **Managed Identity**: Enable a system-assigned managed identity.
7.  Create the VM.

### Step 2: Configure Key Vault Access

Go to your Key Vault -> **Access policies** -> **Create** and grant the VM's managed identity `Get` and `List` permissions for secrets.

### Step 3: Deploy the Application

1.  SSH into your VM.
2.  Install Docker and Docker Compose.
3.  Clone your repository.
4.  Use the Azure CLI to fetch secrets and create a `.env` file:
    ```bash
    # Example for fetching one secret
    export KUMO_API_KEY=$(az keyvault secret show --name KUMO-API-KEY --vault-name YOUR_VAULT_NAME --query value -o tsv)
    # Repeat for OPENAI_API_KEY and write to .env
    ```
5.  Run with Docker Compose:
    ```bash
    docker-compose up -d
    ```

### Step 4: Configure DNS and SSL

Follow the same steps as in the EC2 guide to configure a domain, Nginx, and Certbot for SSL.

---

## Option 2: Deploy to Azure Container Instances (ACI)

### Step 1: Push Docker Image to ACR

1.  Create an **Azure Container Registry (ACR)**.
2.  Log in to your ACR:
    ```bash
    az acr login --name YOUR_ACR_NAME
    ```
3.  Tag and push your Docker image:
    ```bash
    docker tag fraudagent:latest YOUR_ACR_NAME.azurecr.io/fraudagent:latest
    docker push YOUR_ACR_NAME.azurecr.io/fraudagent:latest
    ```

### Step 2: Create a Container Instance

Use the Azure CLI to create a container instance:

```bash
az container create \
    --resource-group YOUR_RESOURCE_GROUP \
    --name fraudagent-aci \
    --image YOUR_ACR_NAME.azurecr.io/fraudagent:latest \
    --registry-login-server YOUR_ACR_NAME.azurecr.io \
    --registry-username $(az acr credential show --name YOUR_ACR_NAME --query username -o tsv) \
    --registry-password $(az acr credential show --name YOUR_ACR_NAME --query passwords[0].value -o tsv) \
    --dns-name-label fraudagent-demo-`head /dev/urandom | tr -dc a-z0-9 | head -c 6` \
    --ports 7860 \
    --cpu 1 \
    --memory 2 \
    --environment-variables \
        KUMO_API_KEY=\'your-kumo-api-key-here\' \
        OPENAI_API_KEY=\'your-openai-api-key-here\'
```

*Note: For production, integrate with Key Vault instead of passing secrets as environment variables.*

### Step 3: Access the Application

Azure will provide a public FQDN (e.g., `fraudagent-demo-xxxxxx.region.azurecontainer.io`) that you can use to access the application on port 7860.

---

## Option 3: Deploy to Azure App Service for Containers

### Step 1: Push Docker Image to ACR

Follow the same steps as in the ACI guide.

### Step 2: Create an App Service Plan and App Service

1.  Create an **App Service Plan** (e.g., Linux, B1 SKU).
2.  Create a new **Web App**:
    -   **Publish**: Docker Container
    -   **Operating System**: Linux
    -   **Region**: Your preferred region
    -   **App Service Plan**: Select the one you created.
3.  In the **Docker** tab:
    -   **Options**: Single Container
    -   **Image Source**: Azure Container Registry
    -   Select your ACR, image, and tag.
4.  In the **Configuration** -> **Application settings** tab:
    -   Add your `KUMO_API_KEY` and `OPENAI_API_KEY` as application settings.
    -   Add a setting `WEBSITES_PORT` with a value of `7860`.
5.  Enable a **system-assigned managed identity** for the App Service.
6.  Grant this identity access to your Key Vault secrets.
7.  Update your application settings to use Key Vault references (e.g., `@Microsoft.KeyVault(SecretUri=...)`).

### Step 3: Configure Custom Domain and SSL

1.  In the App Service, go to **Custom domains** and add your domain.
2.  Go to **TLS/SSL settings** to upload your own certificate or create a free App Service Managed Certificate.

---

## Cost Considerations

-   **Azure VM**: Pay for the VM while it's running.
-   **ACI**: Pay per second for resource usage. Good for short-lived tasks or simple apps.
-   **App Service**: Pay for the App Service Plan. Offers a free tier for development and testing. Provides the most features for production web apps.

Always use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) to estimate costs.
