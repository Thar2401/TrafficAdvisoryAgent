# IBM Cloud Deployment Guide - AI Traffic Advisory Agent

## Deployment Options for IBM Cloud

IBM Cloud offers several deployment options. We'll cover the two best options for this Streamlit application:

### Option 1: IBM Cloud Code Engine (Recommended) ⭐
- **Best for**: Production deployment, auto-scaling, modern cloud-native apps
- **Cost**: Pay-per-use, generous free tier
- **Complexity**: Medium (containerized deployment)
- **Performance**: Excellent (automatic scaling)

### Option 2: IBM Cloud Foundry
- **Best for**: Quick deployment, traditional PaaS model
- **Cost**: Requires Cloud Foundry runtime
- **Complexity**: Easy (buildpack-based)
- **Performance**: Good (manual scaling)

---

## Option 1: IBM Cloud Code Engine Deployment (Recommended)

### Prerequisites
1. **IBM Cloud Account**: Sign up at https://cloud.ibm.com
2. **IBM Cloud CLI**: Install from https://cloud.ibm.com/docs/cli
3. **Docker**: Install from https://www.docker.com/products/docker-desktop
4. **Code Engine Plugin**: `ibmcloud plugin install code-engine`

### Step 1: Install and Configure IBM Cloud CLI

```bash
# Install IBM Cloud CLI (macOS)
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh

# Or using Homebrew
brew install ibmcloud-cli

# Install Code Engine plugin
ibmcloud plugin install code-engine

# Login to IBM Cloud
ibmcloud login

# Target your resource group
ibmcloud target -g Default
```

### Step 2: Create Code Engine Project

```bash
# Create a new Code Engine project
ibmcloud ce project create --name traffic-advisory-app

# Select the project
ibmcloud ce project select --name traffic-advisory-app
```

### Step 3: Build and Deploy Using Code Engine

**Method A: Build from Source (Easiest)**

```bash
# Navigate to project directory
cd /Users/tharunsmac/Desktop/Projects/TECHGIUM/TrafficAdvisoryAgent

# Create application directly from source
ibmcloud ce application create \
  --name traffic-advisor \
  --build-source . \
  --build-context-dir . \
  --strategy dockerfile \
  --port 8080 \
  --min-scale 1 \
  --max-scale 3 \
  --cpu 0.5 \
  --memory 1G \
  --env-from-configmap streamlit-config
```

**Method B: Build Docker Image Locally and Push**

```bash
# Build Docker image locally
docker build -t traffic-advisory-agent:latest .

# Tag for IBM Cloud Container Registry
docker tag traffic-advisory-agent:latest \
  us.icr.io/<your-namespace>/traffic-advisory-agent:latest

# Login to IBM Cloud Container Registry
ibmcloud cr login

# Create namespace (if not exists)
ibmcloud cr namespace-add <your-namespace>

# Push image
docker push us.icr.io/<your-namespace>/traffic-advisory-agent:latest

# Deploy to Code Engine
ibmcloud ce application create \
  --name traffic-advisor \
  --image us.icr.io/<your-namespace>/traffic-advisory-agent:latest \
  --port 8080 \
  --min-scale 1 \
  --max-scale 3 \
  --cpu 0.5 \
  --memory 1G
```

### Step 4: Access Your Application

```bash
# Get application URL
ibmcloud ce application get --name traffic-advisor

# Example output:
# URL: https://traffic-advisor.abc123xyz.us-south.codeengine.appdomain.cloud
```

### Step 5: Configure Auto-Scaling (Optional)

```bash
# Update scaling configuration
ibmcloud ce application update \
  --name traffic-advisor \
  --min-scale 1 \
  --max-scale 5 \
  --concurrency 50 \
  --scale-down-delay 300
```

### Step 6: Monitor and Manage

```bash
# View application status
ibmcloud ce application get --name traffic-advisor

# View logs
ibmcloud ce application logs --name traffic-advisor

# View revisions
ibmcloud ce revision list

# Delete application (cleanup)
ibmcloud ce application delete --name traffic-advisor
```

---

## Option 2: IBM Cloud Foundry Deployment

### Prerequisites
1. IBM Cloud Account
2. Cloud Foundry CLI: `ibmcloud cf install`

### Step 1: Create manifest.yml

See the `manifest.yml` file in the project root (created below).

### Step 2: Deploy to Cloud Foundry

```bash
# Login and target Cloud Foundry
ibmcloud login
ibmcloud target --cf

# Push application
ibmcloud cf push traffic-advisor

# Get application URL
ibmcloud cf apps
```

---

## Configuration Files Reference

### Dockerfile (Already Created)
- Base: Python 3.11-slim
- Port: 8080 (IBM Cloud default)
- Streamlit optimized settings
- Health check enabled

### .dockerignore (Already Created)
- Excludes unnecessary files from Docker build
- Reduces image size
- Improves build performance

### manifest.yml (Created Below)
- Cloud Foundry deployment configuration
- Defines buildpack, memory, instances

---

## Environment Variables (Optional)

Create a `.env` file for local testing:

```bash
# .env
PORT=8080
STREAMLIT_SERVER_PORT=8080
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

For IBM Cloud Code Engine:

```bash
# Create config map
ibmcloud ce configmap create streamlit-config \
  --from-literal PORT=8080 \
  --from-literal STREAMLIT_SERVER_HEADLESS=true
```

---

## Cost Estimation

### Code Engine Pricing (Pay-as-you-go)
- **Free Tier**: 
  - 100,000 vCPU-seconds/month
  - 200,000 GB-seconds/month
  - Sufficient for moderate traffic
  
- **Paid Tier**:
  - CPU: $0.00003375/vCPU-second
  - Memory: $0.00000375/GB-second
  - Estimated: ~$5-15/month for moderate use

### Cloud Foundry Pricing
- Lite Plan: Free for testing (1 instance, 256MB)
- Standard Plan: ~$0.07/GB-hour (~$50/month for 1GB instance)

---

## Troubleshooting

### Issue: Application Not Starting

```bash
# Check logs
ibmcloud ce application logs --name traffic-advisor --follow

# Check application events
ibmcloud ce application events --name traffic-advisor
```

### Issue: Port Binding Errors

Ensure Streamlit is configured to use port 8080:
```python
# In Dockerfile CMD
--server.port=8080 --server.address=0.0.0.0
```

### Issue: Build Failures

```bash
# Check build logs
ibmcloud ce buildrun logs --name <buildrun-name>

# Verify Dockerfile syntax locally
docker build -t test .
```

### Issue: Out of Memory

```bash
# Increase memory allocation
ibmcloud ce application update --name traffic-advisor --memory 2G
```

---

## Production Optimizations

### 1. Enable Caching
Already implemented with `@st.cache_resource`

### 2. Add Custom Domain (Optional)

```bash
# Add custom domain mapping
ibmcloud ce application update \
  --name traffic-advisor \
  --domain traffic.yourdomain.com
```

### 3. Enable HTTPS
Code Engine automatically provides HTTPS certificates

### 4. Implement Health Checks
Already included in Dockerfile

### 5. Set Up Monitoring

```bash
# Enable IBM Cloud Monitoring
ibmcloud resource service-instance-create \
  traffic-advisor-monitor \
  sysdig-monitor \
  lite \
  us-south
```

---

## Security Best Practices

1. **API Keys**: Store in IBM Cloud Secrets Manager
2. **Environment Variables**: Use Code Engine configmaps/secrets
3. **Network Policies**: Configure VPC if needed
4. **CORS**: Already disabled for security
5. **Rate Limiting**: Implement using IBM Cloud Internet Services

---

## Continuous Deployment (CI/CD)

### Using GitHub Actions

Create `.github/workflows/deploy-ibm-cloud.yml`:

```yaml
name: Deploy to IBM Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install IBM Cloud CLI
        run: |
          curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
          ibmcloud plugin install code-engine
      
      - name: Login to IBM Cloud
        run: |
          ibmcloud login --apikey ${{ secrets.IBM_CLOUD_API_KEY }} -r us-south
          ibmcloud ce project select --name traffic-advisory-app
      
      - name: Deploy Application
        run: |
          ibmcloud ce application update \
            --name traffic-advisor \
            --build-source . \
            --build-context-dir .
```

---

## Rollback Strategy

```bash
# List revisions
ibmcloud ce revision list

# Rollback to previous revision
ibmcloud ce application update \
  --name traffic-advisor \
  --revision traffic-advisor-00002
```

---

## Complete Deployment Checklist

- [ ] IBM Cloud account created
- [ ] IBM Cloud CLI installed
- [ ] Code Engine plugin installed
- [ ] Dockerfile created
- [ ] .dockerignore created
- [ ] Application tested locally with Docker
- [ ] Code Engine project created
- [ ] Application deployed
- [ ] URL accessed and tested
- [ ] Scaling configured
- [ ] Monitoring set up (optional)
- [ ] Custom domain configured (optional)

---

## Quick Start Commands (Complete Workflow)

```bash
# 1. Login
ibmcloud login

# 2. Create project
ibmcloud ce project create --name traffic-advisory-app
ibmcloud ce project select --name traffic-advisory-app

# 3. Deploy
cd /Users/tharunsmac/Desktop/Projects/TECHGIUM/TrafficAdvisoryAgent
ibmcloud ce application create \
  --name traffic-advisor \
  --build-source . \
  --port 8080 \
  --min-scale 1 \
  --max-scale 3 \
  --cpu 0.5 \
  --memory 1G

# 4. Get URL
ibmcloud ce application get --name traffic-advisor --output url
```

Visit the URL and your Traffic Advisory Agent will be live! 🚀
