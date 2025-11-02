# 🚀 FraudAGENT - Easy Permanent Deployment Guide

This guide provides a summary of the easiest ways to deploy your FraudAGENT application permanently using free or low-cost hosting platforms. For more advanced options (AWS, Azure, GCP), see the `PERMANENT_DEPLOYMENT.md` guide.

---

## 🎯 Choose Your Deployment Platform

Here are the top recommendations for easy, one-click deployment. All options have generous free tiers.

| Platform | Best For | Free Tier | Persistent Storage | Custom Domain | Ease of Use |
|---|---|---|---|---|---|
| **[Hugging Face Spaces](#1-hugging-face-spaces)** | **Easiest deployment**, Gradio apps | ✅ Free (CPU basic) | ✅ Yes | ❌ No (paid) | ⭐⭐⭐⭐⭐ |
| **[Railway.app](#2-railwayapp)** | **Flexible**, good for GitHub integration | ✅ $5/month credit | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐ |
| **[Render.com](#3-rendercom)** | **Auto-scaling**, good for production | ✅ Free (spins down) | ❌ No (paid) | ✅ Yes | ⭐⭐⭐⭐ |

---

## 1. Hugging Face Spaces (Recommended for Simplicity)

**Hugging Face Spaces** is the easiest and fastest way to deploy a Gradio application like FraudAGENT. It's designed specifically for hosting ML demos and apps.

### Why Choose Hugging Face?
- **Extremely simple**: Just upload your files and it works.
- **Free hosting**: The free tier is generous and sufficient for most use cases.
- **Persistent storage**: Your uploaded data will be saved across restarts.
- **Gradio-native**: Built-in support for Gradio applications.

### How to Deploy

1.  **Create a new Space**: Go to [huggingface.co/new-space](https://huggingface.co/new-space) and choose the Gradio SDK.
2.  **Upload files**: Upload the `app.py`, `requirements.txt`, `src/`, `data/`, and `mock_kumoai.py` files.
3.  **Add secrets**: In your Space settings, add your `KUMO_API_KEY` and `OPENAI_API_KEY`.
4.  **Done!** Your application will be live at `https://huggingface.co/spaces/YOUR_USERNAME/fraudagent`.

> **For detailed instructions, see: [DEPLOY_HF.md](README_HF.md)**

---

## 2. Railway.app

**Railway** is a modern hosting platform that makes it easy to deploy applications from a GitHub repository.

### Why Choose Railway?
- **Generous free tier**: $5/month credit is enough to run the app for free.
- **Persistent storage**: Your uploaded data is saved.
- **Custom domains**: Easily add your own domain.
- **Great GitHub integration**: Automatically deploys when you push changes.

### How to Deploy

1.  **Push to GitHub**: Create a GitHub repository and push your code.
2.  **Deploy on Railway**: Go to [railway.app/new](https://railway.app/new) and select "Deploy from GitHub repo".
3.  **Add environment variables**: In the Railway dashboard, add your API keys and other settings.
4.  **Done!** Your app will be live at a `*.up.railway.app` URL.

> **For detailed instructions, see: [DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)**

---

## 3. Render.com

**Render** is a powerful cloud platform that offers a free tier for web services. It's a good step up from simpler platforms and offers more production-grade features.

### Why Choose Render?
- **Auto-scaling**: Can automatically handle traffic spikes (paid plans).
- **Free SSL**: Automatic SSL certificates for custom domains.
- **Infrastructure as Code**: Use `render.yaml` to define your services.
- **Global CDN**: Fast content delivery.

### How to Deploy

1.  **Push to GitHub**: Create a GitHub repository and push your code.
2.  **Create a Web Service**: Go to the Render dashboard and create a new Web Service from your GitHub repo.
3.  **Configure settings**: Set the build command to `pip install -r requirements.txt` and the start command to `python3 app.py`.
4.  **Add environment variables**: Add your API keys in the environment settings.
5.  **Done!** Your app will be live at a `*.onrender.com` URL.

**Important Note**: Render's free tier has **ephemeral storage**, meaning your uploaded data will be lost on restart. For persistent storage, you'll need to upgrade to a paid plan.

> **For detailed instructions, see: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)**

---

## 🚀 One-Click Deployment Buttons

Once you have pushed your code to a public GitHub repository, you can add these buttons to your `README.md` for one-click deployment:

**Hugging Face Spaces**
```markdown
[![Deploy to Hugging Face Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/deploy-to-spaces-lg.svg)](https://huggingface.co/new-space?template=YOUR_USERNAME/fraudagent)
```

**Railway**
```markdown
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/YOUR_USERNAME/fraudagent)
```

**Render**
```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/fraudagent)
```

> **Replace `YOUR_USERNAME/fraudagent` with your actual GitHub repository URL.**

---

## Conclusion

For the quickest and easiest deployment with all features (including persistent storage for uploads), **Hugging Face Spaces is the recommended choice**.

For more control and production-oriented features, Railway and Render are excellent alternatives.

All the necessary configuration files (`railway.json`, `render.yaml`, `app.py` for Hugging Face) are already included in the project.
