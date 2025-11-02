# FraudAGENT - Hugging Face Spaces Deployment

This file contains instructions for deploying FraudAGENT to Hugging Face Spaces.

## Quick Deploy to Hugging Face Spaces

Hugging Face Spaces provides **free hosting** for Gradio applications with persistent URLs.

### Prerequisites

- Hugging Face account (free at https://huggingface.co/join)
- Your API keys (KUMO_API_KEY and OPENAI_API_KEY)

### Step-by-Step Deployment

#### 1. Create a New Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Space name**: `fraudagent` (or your preferred name)
   - **License**: Apache 2.0
   - **Select SDK**: Gradio
   - **Python version**: 3.11
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private

3. Click **Create Space**

#### 2. Upload Files

Upload these files to your Space:

**Required files:**
- `app.py` (renamed from `main_with_upload.py`)
- `requirements.txt`
- `src/` directory (all Python modules)
- `data/` directory (sample data)
- `mock_kumoai.py` (for demo mode)

**Optional files:**
- `README.md`
- `.gitignore`

#### 3. Configure Secrets

In your Space settings, add these secrets:

1. Go to **Settings** → **Repository secrets**
2. Add the following secrets:

```
KUMO_API_KEY=your-actual-kumo-api-key
OPENAI_API_KEY=your-actual-openai-api-key
```

#### 4. The Space Will Auto-Deploy

Hugging Face Spaces will automatically:
- Install dependencies from `requirements.txt`
- Run `app.py`
- Expose the Gradio interface at `https://huggingface.co/spaces/YOUR_USERNAME/fraudagent`

### Files to Upload

The repository structure for Hugging Face Spaces:

```
fraudagent/
├── app.py                    # Main application (renamed from main_with_upload.py)
├── requirements.txt          # Python dependencies
├── README.md                 # Space description
├── .gitignore               # Git ignore file
├── mock_kumoai.py           # Mock KumoRFM SDK
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── kumo_setup.py
│   ├── text_to_pql.py
│   ├── kumo_agent.py
│   ├── excel_converter.py
│   └── upload_ui.py
└── data/
    ├── customers.parquet
    └── claims.parquet
```

### Using Git to Deploy

Alternatively, you can use Git:

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/fraudagent
cd fraudagent

# Copy application files
cp -r /path/to/insurance-claims-kumo-agent/src .
cp -r /path/to/insurance-claims-kumo-agent/data .
cp /path/to/insurance-claims-kumo-agent/main_with_upload.py app.py
cp /path/to/insurance-claims-kumo-agent/requirements.txt .
cp /path/to/insurance-claims-kumo-agent/mock_kumoai.py .

# Commit and push
git add .
git commit -m "Initial deployment of FraudAGENT"
git push
```

### Environment Variables

The app will automatically read secrets from Hugging Face Spaces environment.

### Persistent Storage

Hugging Face Spaces provides persistent storage for uploaded data:
- Uploaded Excel files will be stored in `uploaded_data/`
- Data persists across restarts

### Custom Domain (Optional)

Hugging Face Spaces provides a free subdomain:
- `https://huggingface.co/spaces/YOUR_USERNAME/fraudagent`

For a custom domain, you'll need to upgrade to a paid plan.

### Monitoring

View logs in your Space:
1. Go to your Space page
2. Click **Logs** tab
3. Monitor application startup and errors

### Updating the Application

To update:
1. Push changes to your Space repository
2. Hugging Face will automatically rebuild and redeploy

### Cost

**Free tier includes:**
- CPU basic hardware
- Persistent storage
- Public or private visibility
- Unlimited usage

**Paid upgrades available for:**
- GPU hardware
- More storage
- Custom domains
