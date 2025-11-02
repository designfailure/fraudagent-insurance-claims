# Deploy FraudAGENT to Render.com

Render provides **free hosting** for web applications with automatic SSL and custom domains.

## Prerequisites

- Render account (free at https://render.com)
- GitHub account (or GitLab/Bitbucket)
- Your API keys (KUMO_API_KEY and OPENAI_API_KEY)

## Deployment Steps

### Option 1: Deploy from GitHub (Recommended)

#### 1. Push to GitHub

```bash
# Create a new repository on GitHub
# Then push your code

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/fraudagent.git
git push -u origin main
```

#### 2. Create Web Service on Render

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Select `fraudagent` repository

#### 3. Configure Service

Fill in the following:

**Basic Settings:**
- **Name**: `fraudagent`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python3 app.py`

**Instance Type:**
- Select **Free** (or paid for better performance)

#### 4. Add Environment Variables

In the **Environment** section, add:

```
KUMO_API_KEY=your-actual-kumo-api-key
OPENAI_API_KEY=your-actual-openai-api-key
APP_HOST=0.0.0.0
APP_PORT=10000
OPENAI_MODEL=gpt-4o-mini
```

#### 5. Deploy

Click **Create Web Service**

Render will:
- Clone your repository
- Install dependencies
- Start your application
- Provide a public URL

#### 6. Access Your App

Your app will be available at:
`https://fraudagent.onrender.com`

### Option 2: Deploy with render.yaml (Infrastructure as Code)

The repository includes `render.yaml` for automatic configuration.

#### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit with render.yaml"
git remote add origin https://github.com/YOUR_USERNAME/fraudagent.git
git push -u origin main
```

#### 2. Create Blueprint on Render

1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Render will automatically read `render.yaml`
5. Add environment variables when prompted
6. Click **Apply**

## Configuration Files

Render uses `render.yaml` for configuration (already included).

## Monitoring

View logs in Render dashboard:
1. Go to your service
2. Click **Logs** tab
3. View real-time logs

## Persistent Storage

Render free tier has ephemeral storage:
- Uploaded files are lost on restart
- For persistent storage, upgrade to paid plan or use external storage (S3, etc.)

**Workaround for free tier:**
- Use environment variables for configuration
- Store uploaded data temporarily
- Inform users to re-upload after restarts

## Custom Domain

To add a custom domain:
1. Go to **Settings** → **Custom Domain**
2. Click **Add Custom Domain**
3. Enter your domain name
4. Configure DNS records as shown
5. Render provides free SSL certificates

## Auto-Deploy

Render automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update application"
git push
```

## Cost

**Free tier includes:**
- 750 hours/month of free usage
- Automatic SSL
- Custom domains
- Auto-deploy from Git
- Shared CPU/RAM

**Limitations:**
- Spins down after 15 minutes of inactivity
- Slower cold starts
- Ephemeral storage

**Paid plans start at $7/month** for:
- Always-on instances
- Persistent storage
- More CPU/RAM
- Faster builds

## Health Checks

Render automatically monitors your app:
- HTTP health checks every 30 seconds
- Auto-restart on failures

## Troubleshooting

### Port Issues

Render uses port 10000 by default. Ensure your app uses:

```python
port = int(os.getenv('PORT', 10000))
```

### Cold Starts

Free tier spins down after inactivity. First request after idle will be slow (~30 seconds).

**Solutions:**
- Upgrade to paid plan
- Use a ping service to keep it alive
- Accept the cold start delay

### Build Failures

Common issues:
- Missing `requirements.txt`
- Python version mismatch
- Dependency conflicts

**Fix:**
- Ensure all dependencies are in `requirements.txt`
- Specify Python version in `render.yaml`

### Memory Limits

Free tier has 512 MB RAM. Optimize by:
- Using smaller datasets
- Reducing concurrent requests
- Upgrading to paid plan

## Scaling

To scale your application:
1. Go to **Settings** → **Scaling**
2. Upgrade instance type
3. Add more instances (paid plans only)

## Support

Render documentation: https://render.com/docs
Community: https://community.render.com
