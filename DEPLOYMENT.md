# Deployment Guide: Survey Agent to Render.com

This guide explains how to deploy the Survey Agent to Render.com.

## Prerequisites

1. **GitHub Repository** - Push your code to a public GitHub repository
2. **Render Account** - Create a free account at [render.com](https://render.com)
3. **Azure Credentials** - Have your Azure API credentials ready:
   - `AZURE_API_BASE`
   - `AZURE_API_KEY`

## Deployment Steps

### Step 1: Prepare Your Repository

Ensure all files are committed and pushed to GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Grant Render access to your repositories

### Step 3: Create a New Web Service

1. Log in to Render Dashboard
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repository (`azure-llm-agent`)
4. Configure the service:

   **Basic Settings:**

   - **Name:** `survey-agent`
   - **Runtime:** Docker
   - **Region:** Oregon (or your preferred region)
   - **Plan:** Free (or upgrade for production)

   **Build & Deploy:**

   - **Build Command:** (leave empty - Docker handles it)
   - **Start Command:** (leave empty - Dockerfile handles it)

5. Click **"Create Web Service"**

### Step 4: Set Environment Variables

1. Go to the deployed service dashboard
2. Click **"Environment"** section
3. Add the following environment variables:

   ```
   AZURE_API_BASE = <your-azure-api-base>
   AZURE_API_KEY = <your-azure-api-key>
   PYTHONUNBUFFERED = 1
   ```

   ⚠️ **Important:** These are sensitive credentials. Use Render's secret management:

   - Click the lock icon when adding `AZURE_API_KEY` to mark it as a secret

4. Click **"Save Changes"** (the service will redeploy)

### Step 5: Monitor Deployment

1. Go to **"Logs"** tab to watch the build process
2. Wait for the message: `"Application startup complete"`
3. Click the URL at the top to access your deployed agent

### Step 6: Access Your Agent

Once deployed, you can access the ADK web interface at:

```
https://<your-service-name>.onrender.com
```

The web UI will allow you to:

- Interact with the survey agent
- Test the `get_user_info` tool
- View agent responses in real-time

## Docker Configuration

### Dockerfile Explained

- **Base Image:** Python 3.13 slim
- **Dependencies:** Installed via `uv` (fast package manager)
- **Port:** 8000 (ADK web server)
- **Command:** Starts ADK web server with public host binding

### Environment Variables

The service needs:

| Variable           | Description               | Required |
| ------------------ | ------------------------- | -------- |
| `AZURE_API_BASE`   | Azure OpenAI API endpoint | Yes      |
| `AZURE_API_KEY`    | Azure OpenAI API key      | Yes      |
| `PYTHONUNBUFFERED` | Python output buffering   | Yes      |

## Troubleshooting

### Service Won't Start

1. **Check Logs:** Click "Logs" in Render dashboard
2. **Common Issues:**
   - Missing environment variables → Add to Render dashboard
   - Python version mismatch → Update Dockerfile if needed
   - Dependency issues → Run `uv sync` locally first

### Connection Timeout

- Render free tier has limited resources
- If agent is slow, consider upgrading to Standard plan

### Members.json Not Found

- Ensure `survey_agent/data/members.json` is committed to Git
- Don't include in `.gitignore`

## Advanced Configuration

### Using render.yaml

Instead of manual configuration, you can use `render.yaml`:

```bash
# Deploy using render.yaml
git push origin main
```

Render will automatically read `render.yaml` and configure the service.

### Custom Domain

1. Go to service settings
2. Click **"Custom Domain"**
3. Add your domain (requires DNS configuration)

### Auto-Deploy on Push

Render automatically redeploys when you push to main branch. To disable:

1. Go to service settings
2. Disable **"Auto-Deploy"**

## Cost Considerations

- **Free Tier:** Spins down after 15 minutes of inactivity (cold start)
- **Standard Plan:** $7/month - Always running
- **Pro Plan:** $25/month - Premium features

For development/testing, free tier is fine. For production, upgrade to Standard.

## Testing After Deployment

Once deployed, test the agent:

1. Open the web UI at your Render URL
2. Ask the agent to get user info: _"Can you get the profile for member M001?"_
3. Agent should retrieve member data and conduct survey questions

## CI/CD Integration

Render automatically:

- Builds Docker image on each push to main
- Deploys updated version
- Keeps previous versions for rollback

To rollback a deployment:

1. Go to service dashboard
2. Click **"Deployments"**
3. Click the previous deployment version
4. Click **"Deploy"** to rollback

## Next Steps

1. **Monitor Performance:** Use Render's metrics dashboard
2. **Set Up Alerts:** Enable email notifications for failures
3. **Add Logging:** Consider adding error tracking (Sentry, DataDog)
4. **Scale:** Upgrade plan if needed for production use

## Additional Resources

- [Render Docker Documentation](https://render.com/docs/docker)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [ADK Framework Documentation](https://github.com/mmphego/adk-python)
