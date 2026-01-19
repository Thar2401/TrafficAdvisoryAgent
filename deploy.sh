#!/bin/bash
# deploy.sh - Automated IBM Cloud Code Engine Deployment Script

set -e  # Exit on error

echo "🚀 AI Traffic Advisory Agent - IBM Cloud Deployment"
echo "=================================================="

# Configuration
APP_NAME="traffic-advisor"
PROJECT_NAME="traffic-advisory-app"
MIN_SCALE=1
MAX_SCALE=3
CPU="0.5"
MEMORY="1G"
PORT=8080

# Check if IBM Cloud CLI is installed
if ! command -v ibmcloud &> /dev/null; then
    echo "❌ IBM Cloud CLI not found. Please install it first:"
    echo "   https://cloud.ibm.com/docs/cli"
    exit 1
fi

# Check if Code Engine plugin is installed
if ! ibmcloud plugin list | grep -q code-engine; then
    echo "📦 Installing Code Engine plugin..."
    ibmcloud plugin install code-engine -f
fi

# Login check
echo "🔐 Checking IBM Cloud login status..."
if ! ibmcloud account show &> /dev/null; then
    echo "Please login to IBM Cloud:"
    ibmcloud login
fi

# Create or select project
echo "📁 Setting up Code Engine project..."
if ibmcloud ce project get --name "$PROJECT_NAME" &> /dev/null; then
    echo "✓ Project exists, selecting it..."
    ibmcloud ce project select --name "$PROJECT_NAME"
else
    echo "✓ Creating new project..."
    ibmcloud ce project create --name "$PROJECT_NAME"
fi

# Deploy application
echo "🚢 Deploying application..."
if ibmcloud ce application get --name "$APP_NAME" &> /dev/null; then
    echo "✓ Updating existing application..."
    ibmcloud ce application update \
        --name "$APP_NAME" \
        --build-source . \
        --strategy dockerfile \
        --port "$PORT"
else
    echo "✓ Creating new application..."
    ibmcloud ce application create \
        --name "$APP_NAME" \
        --build-source . \
        --build-context-dir . \
        --strategy dockerfile \
        --port "$PORT" \
        --min-scale "$MIN_SCALE" \
        --max-scale "$MAX_SCALE" \
        --cpu "$CPU" \
        --memory "$MEMORY"
fi

# Wait for deployment
echo "⏳ Waiting for deployment to complete..."
sleep 10

# Get application URL
echo ""
echo "✅ Deployment Complete!"
echo "===================="
APP_URL=$(ibmcloud ce application get --name "$APP_NAME" --output url)
echo "🌐 Application URL: $APP_URL"
echo ""
echo "📊 Application Status:"
ibmcloud ce application get --name "$APP_NAME"

echo ""
echo "🔍 View logs: ibmcloud ce application logs --name $APP_NAME --follow"
echo "🗑️  Delete app: ibmcloud ce application delete --name $APP_NAME"
