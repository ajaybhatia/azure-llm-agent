# Quick Deploy to Render.com

## TL;DR - 5 Minutes to Production

### 1. Push to GitHub

```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### 2. Create Service on Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Select your `azure-llm-agent` GitHub repo
4. Name it: `survey-agent`
5. Select **"Docker"** runtime
6. Click **"Create Web Service"**

### 3. Add Environment Variables

In the Render dashboard, go to **"Environment"** and add:

```
AZURE_API_BASE = your-azure-api-base-url
AZURE_API_KEY = your-azure-api-key
```

### 4. Wait for Deploy

- Monitor in **"Logs"** tab
- When you see `"Application startup complete"`, it's ready!
- Visit your URL: `https://survey-agent.onrender.com`

## What Gets Deployed

✅ Survey agent with ADK web interface
✅ 100-member database (members.json)
✅ All Python packages via uv
✅ Azure LLM integration

## Key Files for Deployment

- `Dockerfile` - Container configuration
- `render.yaml` - Service configuration
- `pyproject.toml` - Python dependencies
- `survey_agent/` - Your agent code

## Cost

- **Free Tier:** $0/month (may spin down after inactivity)
- **Standard:** $7/month (always running)

## Troubleshooting

| Problem            | Solution                                          |
| ------------------ | ------------------------------------------------- |
| Build fails        | Check Dockerfile - ensure Python 3.13+            |
| Missing env vars   | Add AZURE_API_BASE and AZURE_API_KEY in dashboard |
| Dependencies fail  | Run `uv sync` locally first to verify             |
| Can't access agent | Wait for "startup complete" in logs               |

## Redeploy After Changes

Just push to main:

```bash
git push origin main
```

Render auto-deploys! No manual steps needed.

For detailed guide, see [DEPLOYMENT.md](./DEPLOYMENT.md)
