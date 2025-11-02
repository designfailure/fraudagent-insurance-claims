# FraudAGENT - AWS Deployment Guide

This guide provides detailed instructions for deploying the **FraudAGENT** application to Amazon Web Services (AWS). It covers three primary deployment methods suitable for different needs, from simple virtual servers to fully managed container orchestration.

---

## 📋 Table of Contents

1.  [Prerequisites](#prerequisites)
2.  [Secrets Management with AWS Secrets Manager](#secrets-management)
3.  [Deployment Options Overview](#deployment-options-overview)
4.  [**Option 1: Deploy to Amazon EC2**](#option-1-deploy-to-amazon-ec2) (Virtual Server)
5.  [**Option 2: Deploy to Amazon ECS with Fargate**](#option-2-deploy-to-amazon-ecs-with-fargate) (Recommended for Production)
6.  [**Option 3: Deploy to AWS App Runner**](#option-3-deploy-to-aws-app-runner) (Easiest)
7.  [Cost Considerations](#cost-considerations)

---

## Prerequisites

Before you begin, ensure you have the following:

-   **AWS Account**: An active AWS account with administrative privileges.
-   **IAM User**: An IAM user with permissions to create and manage EC2, ECS, ECR, App Runner, and Secrets Manager resources.
-   **AWS CLI**: The AWS Command Line Interface installed and configured on your local machine. [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
-   **Docker**: Docker Desktop or Docker Engine installed on your local machine. [Installation Guide](https://docs.docker.com/get-docker/)
-   **Git**: Git installed on your local machine.

---

## Secrets Management

For production deployments, never hardcode API keys. Use **AWS Secrets Manager** to securely store and manage your `KUMO_API_KEY` and `OPENAI_API_KEY`.

### Step 1: Store Your Secrets

1.  Navigate to the **AWS Secrets Manager** console.
2.  Click **Store a new secret**.
3.  Select **Other type of secret**.
4.  In the **Secret key/value** section, add two key-value pairs:
    -   Key: `KUMO_API_KEY`, Value: `your-kumo-api-key-here`
    -   Key: `OPENAI_API_KEY`, Value: `your-openai-api-key-here`
5.  Click **Next**.
6.  Give your secret a name (e.g., `fraudagent/api_keys`) and an optional description.
7.  Follow the prompts to complete the secret creation.

### Step 2: Create an IAM Policy

Create an IAM policy that grants read-only access to this secret. This policy will be attached to the IAM role used by your EC2 instance or ECS task.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "arn:aws:secretsmanager:YOUR_REGION:YOUR_ACCOUNT_ID:secret:fraudagent/api_keys-??????"
        }
    ]
}
```

*Replace `YOUR_REGION`, `YOUR_ACCOUNT_ID`, and the secret ARN with your specific values.*

---

## Deployment Options Overview

| Option | Description | Use Case | Complexity | Cost Model |
|---|---|---|---|---|
| **EC2** | Deploy on a virtual server. Full control over the environment. | Simple deployments, testing, or when you need full OS control. | Low | Pay per hour for the instance. |
| **ECS + Fargate** | Serverless container orchestration. AWS manages the underlying infrastructure. | **Recommended for production**. Scalable, resilient, and integrated with AWS ecosystem. | Medium | Pay per vCPU and GB of memory used by your containers. |
| **App Runner** | Fully managed service for containerized web apps. | **Easiest option**. Ideal for simple web services where you don't want to manage infrastructure. | Very Low | Pay for active compute resources and a deployment fee. |

---

## Option 1: Deploy to Amazon EC2

### Step 1: Launch EC2 Instance

1.  Navigate to the **EC2** console and click **Launch instances**.
2.  **AMI**: Choose **Ubuntu Server 22.04 LTS**.
3.  **Instance Type**: Select `t3.medium` or larger.
4.  **Key Pair**: Create or select an existing key pair to SSH into the instance.
5.  **Network Settings**: Create a security group that allows inbound traffic on:
    -   **SSH (Port 22)** from your IP address.
    -   **HTTP (Port 80)** from anywhere (0.0.0.0/0).
    -   **HTTPS (Port 443)** from anywhere (0.0.0.0/0).
6.  **IAM Role**: Create and attach an IAM role with the Secrets Manager policy you created earlier.
7.  Launch the instance.

### Step 2: Install Dependencies

1.  Connect to your instance via SSH.
2.  Install Docker and Docker Compose:
    ```bash
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo usermod -aG docker $USER
    newgrp docker
    ```

### Step 3: Deploy the Application

1.  Clone your repository:
    ```bash
    git clone https://your-repo-url/insurance-claims-kumo-agent.git
    cd insurance-claims-kumo-agent
    ```
2.  Create a `.env` file. Instead of hardcoding secrets, you can use a startup script to fetch them, or manually populate it for simplicity.
3.  Build and run the application using Docker Compose:
    ```bash
    # This will build the image and start the container in the background
    docker-compose up -d
    ```

### Step 4: Configure DNS and SSL

1.  Point a domain name (e.g., `fraudagent.yourdomain.com`) to the public IP address of your EC2 instance.
2.  Install Certbot and obtain an SSL certificate:
    ```bash
    sudo apt-get install -y certbot python3-certbot-nginx
    # Follow the prompts to configure SSL for your domain
    sudo certbot --nginx
    ```
3.  Start the Nginx reverse proxy container:
    ```bash
    # This will start the nginx service defined in docker-compose.yml
    docker-compose --profile with-nginx up -d
    ```

---

## Option 2: Deploy to Amazon ECS with Fargate

### Step 1: Push Docker Image to ECR

1.  Navigate to the **Elastic Container Registry (ECR)** console and create a new **private** repository (e.g., `fraudagent`).
2.  Select the repository and click **View push commands**.
3.  Follow the commands to build, tag, and push your local Docker image to ECR.

### Step 2: Create ECS Cluster and Task Definition

1.  Navigate to the **Elastic Container Service (ECS)** console.
2.  Create a new cluster using the **Networking only** template (for Fargate).
3.  Go to **Task Definitions** and create a new task definition:
    -   Select **Fargate** launch type.
    -   **Task size**: Assign CPU (e.g., 1 vCPU) and memory (e.g., 2 GB).
    -   **Container Details**:
        -   **Name**: `fraudagent`
        -   **Image**: Paste the ECR image URI from the previous step.
        -   **Port Mappings**: `7860` TCP.
        -   **Environment Variables**: In the `environment` section, for `KUMO_API_KEY` and `OPENAI_API_KEY`, set the `ValueFrom` to the ARN of your secret in Secrets Manager.
    -   **IAM Roles**: Create or assign a **Task execution role** that has permissions for ECR (`ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, etc.) and the Secrets Manager policy.

### Step 3: Create ECS Service and Load Balancer

1.  In your ECS cluster, create a new **Service**.
2.  **Launch Type**: Fargate.
3.  **Task Definition**: Select the one you just created.
4.  **Desired tasks**: Set to `1` (or more for scaling).
5.  **Networking**: Choose a VPC and subnets.
6.  **Load Balancing**: Select **Application Load Balancer (ALB)**.
    -   Create a new ALB.
    -   Create a new target group.
    -   Configure the listener on port 80 (it will be updated to 443 later).
7.  Create the service.

### Step 4: Configure DNS and SSL

1.  Navigate to the **EC2** console -> **Load Balancers**.
2.  Point your domain name to the DNS name of the ALB.
3.  Use **AWS Certificate Manager (ACM)** to request a public SSL certificate for your domain.
4.  Edit the ALB's listener to use **HTTPS on port 443**, and select the ACM certificate you created.

---

## Option 3: Deploy to AWS App Runner

### Step 1: Push Docker Image to ECR

Follow the same steps as in the ECS deployment to push your Docker image to an ECR repository.

### Step 2: Create an App Runner Service

1.  Navigate to the **AWS App Runner** console and click **Create an App Runner service**.
2.  **Source**: Select **Container registry** and **Amazon ECR**.
3.  **Container image URI**: Browse and select your `fraudagent` image from ECR.
4.  **Deployment settings**: Choose **Automatic**.
5.  **Service settings**:
    -   **Service name**: `fraudagent-service`
    -   **Virtual CPU & memory**: Select appropriate values (e.g., 1 vCPU, 2 GB).
    -   **Port**: `7860`.
    -   **Environment variables**: Add your `KUMO_API_KEY` and `OPENAI_API_KEY` here. For production, you can integrate with Secrets Manager by providing the secret ARN in the service configuration.
6.  Review and create the service.

### Step 3: Access Your Application

App Runner will automatically build, deploy, and provide a default public domain (e.g., `...awsapprunner.com`). You can access your application via this URL. You can also link a custom domain in the App Runner console.

---

## Cost Considerations

-   **EC2**: You pay for the instance while it's running, regardless of traffic. Good for predictable workloads.
-   **ECS with Fargate**: You pay for the vCPU and memory resources consumed by your running containers. Cost-effective for variable or bursty traffic.
-   **App Runner**: You pay for the time your application is running and processing requests, plus a small fee for deployment. Can be very cost-effective for low-traffic applications.

Always use the [AWS Pricing Calculator](https://calculator.aws/) to estimate your costs before deploying.
