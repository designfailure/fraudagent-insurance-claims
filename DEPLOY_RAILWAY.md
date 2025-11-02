# Deploy FraudAGENT to Railway.app

Railway provides **$5/month free credit** and easy deployment from GitHub.

## Prerequisites

- Railway account (free at https://railway.app)
- GitHub account
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

#### 2. Deploy on Railway

1. Go to https://railway.app/new
2. Click **Deploy from GitHub repo**
3. Select your `fraudagent` repository
4. Railway will automatically detect Python and deploy

#### 3. Configure Environment Variables

In the Railway dashboard:

1. Go to your project
2. Click **Variables** tab
3. Add these variables:

```
KUMO_API_KEY=your-actual-kumo-api-key
OPENAI_API_KEY=your-actual-openai-api-key
APP_HOST=0.0.0.0
APP_PORT=8080
OPENAI_MODEL=gpt-4o-mini
```

#### 4. Access Your App

Railway will provide a public URL like:
`https://fraudagent-production.up.railway.app`

### Option 2: Deploy with Railway CLI

#### 1. Install Railway CLI

```bash
# macOS/Linux
curl -fsSL https://railway.app/install.sh | sh

# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex
```

#### 2. Login

```bash
railway login
```

#### 3. Initialize Project

```bash
cd /path/to/insurance-claims-kumo-agent
railway init
```

#### 4. Add Environment Variables

```bash
railway variables set KUMO_API_KEY=your-actual-kumo-api-key
railway variables set OPENAI_API_KEY=your-actual-openai-api-key
railway variables set APP_HOST=0.0.0.0
railway variables set APP_PORT=8080
```

#### 5. Deploy

```bash
railway up
```

#### 6. Open Your App

```bash
railway open
```

## Configuration Files

Railway uses `railway.json` for configuration (already included).

## Monitoring

View logs in Railway dashboard:
1. Go to your project
2. Click **Deployments** tab
3. Select latest deployment
4. View logs in real-time

## Persistent Storage

Railway provides persistent storage:
- Uploaded Excel files are stored in `uploaded_data/`
- Data persists across deployments

## Custom Domain

To add a custom domain:
1. Go to **Settings** → **Domains**
2. Click **Add Domain**
3. Enter your domain name
4. Configure DNS records as shown

## Cost

**Free tier includes:**
- $5/month credit
- 500 hours of execution time
- 100 GB outbound bandwidth
- Shared CPU/RAM

**Paid plans start at $5/month** for additional credits.

## Updating

To update your deployment:

**Via GitHub:**
```bash
git add .
git commit -m "Update application"
git push
```
Railway will automatically redeploy.

**Via CLI:**
```bash
railway up
```

## Troubleshooting

### Port Issues

Railway uses dynamic ports. Ensure your app reads from `PORT` environment variable:

```python
port = int(os.getenv('PORT', 8080))
```

### Build Failures

Check `requirements.txt` is present and contains all dependencies.

### Memory Issues

Free tier has limited memory. Optimize by:
- Using smaller datasets
- Reducing concurrent requests
- Upgrading to paid plan

## Support

Railway documentation: https://docs.railway.app
