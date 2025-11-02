# 🚀 Deploy FraudAGENT to Hugging Face Spaces

**A step-by-step guide to deploying your FraudAGENT application on Hugging Face Spaces for free permanent hosting.**

---

## 🎯 Overview

This guide will walk you through the process of deploying your FraudAGENT application to Hugging Face Spaces. This is the **easiest and fastest** way to get your application running permanently with a public URL.

**Time to Deploy**: ~5 minutes

---

## ✅ Prerequisites

1. **GitHub Account** - You need a GitHub account to host your code.
2. **Hugging Face Account** - You need a Hugging Face account to create a Space.
3. **API Keys**:
   - `KUMO_API_KEY` - Your KumoRFM API key
   - `OPENAI_API_KEY` - Your OpenAI API key

---

## 🛠️ Deployment Steps

### Step 1: Create a GitHub Repository

1. **Go to GitHub** and create a new repository.
   - Name: `fraud-agent-app` (or any name you prefer)
   - Visibility: **Public**

2. **Push the code** to your new repository:
   ```bash
   # Navigate to your project directory
   cd /path/to/insurance-claims-kumo-agent

   # Initialize Git (if not already done)
   git init
   git branch -m main

   # Add all files
   git add .

   # Commit the files
   git commit -m "Initial commit of FraudAGENT application"

   # Add the remote repository
   git remote add origin https://github.com/YOUR_USERNAME/fraud-agent-app.git

   # Push the code
   git push -u origin main
   ```

### Step 2: Create a Hugging Face Space

1. **Go to Hugging Face** and click on your profile picture, then **New Space**.

2. **Configure your Space**:
   - **Owner**: Your Hugging Face username
   - **Space name**: `FraudAGENT` (or any name you prefer)
   - **License**: `mit`
   - **SDK**: `Gradio`
   - **Space hardware**: `CPU basic - FREE`
   - **Visibility**: `Public`

3. **Click "Create Space"**.

### Step 3: Link to Your GitHub Repository

1. In your new Space, go to the **Files and versions** tab.

2. **Click "Use a Git repository"** and select your GitHub repository (`fraud-agent-app`).

3. **Hugging Face will automatically pull your code** from GitHub.

### Step 4: Add Your API Keys as Secrets

1. In your Space, go to the **Settings** tab.

2. **Scroll down to "Secrets"** and click **New secret**.

3. **Add your API keys**:
   - **Name**: `KUMO_API_KEY`
   - **Value**: `your-kumo-api-key-here`

4. **Click "Add secret"**.

5. **Repeat for your OpenAI API key**:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: `your-openai-api-key-here`

### Step 5: Deploy!

1. **Hugging Face will automatically detect the changes** and start building your application.

2. **Go to the "App" tab** to see the build progress.

3. **Once the build is complete**, your application will be live!

---

## 🎉 Your Application is Live!

Your FraudAGENT application is now permanently deployed on Hugging Face Spaces with a public URL!

**Example URL**: `https://huggingface.co/spaces/YOUR_USERNAME/FraudAGENT`

---

## 🔄 Automatic Updates

Every time you push a change to your GitHub repository, Hugging Face will automatically update your Space with the latest code.

```bash
# Make changes to your code
git add .
git commit -m "Updated feature X"
git push
```

---

##  troubleshooting

### Application Not Building?
- **Check `requirements.txt`**: Ensure all dependencies are listed.
- **Check `app.py`**: Make sure it points to the correct main application file.
- **Check logs**: Go to the "App" tab and look for build errors.

### API Key Errors?
- **Verify secret names**: Make sure they are exactly `KUMO_API_KEY` and `OPENAI_API_KEY`.
- **Verify secret values**: Double-check that you copied the correct API keys.

### Gradio Errors?
- **Check Gradio version**: Ensure `sdk_version` in `README_HF_SPACES.md` matches your Gradio version.
- **Check UI code**: Make sure your Gradio interface is correctly defined.

---

## 📖 Additional Resources

- **Hugging Face Spaces Documentation**: [https://huggingface.co/docs/spaces/](https://huggingface.co/docs/spaces/)
- **Gradio Documentation**: [https://www.gradio.app/docs/](https://www.gradio.app/docs/)

---

**Congratulations! You have successfully deployed your FraudAGENT application permanently for free!** 🚀
