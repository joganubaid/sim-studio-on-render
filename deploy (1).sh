#!/bin/bash

# Sim Studio Render Deployment Script
# This script helps you deploy Sim Studio to Render

set -e

echo "🚀 Sim Studio Render Deployment Helper"
echo "======================================"

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ This must be run from a Git repository."
    exit 1
fi

echo "✅ Git repository detected"

# Generate a secure secret for BETTER_AUTH_SECRET
generate_secret() {
    openssl rand -base64 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "CHANGE-THIS-SECRET-$(date +%s)"
}

SECRET=$(generate_secret)

echo "🔐 Generated BETTER_AUTH_SECRET: $SECRET"
echo ""

# Get domain from user
read -p "🌐 Enter your Render domain (e.g., my-simstudio.onrender.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "❌ Domain is required"
    exit 1
fi

# Update render.yaml with user's domain
echo "📝 Updating render.yaml with your domain..."

# Create a temporary file for sed
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/your-simstudio-app.onrender.com/$DOMAIN/g" render.yaml
else
    # Linux
    sed -i "s/your-simstudio-app.onrender.com/$DOMAIN/g" render.yaml
fi

echo "✅ Updated render.yaml"

# Commit changes
echo "📦 Committing changes..."
git add render.yaml
git commit -m "Configure deployment for $DOMAIN" || echo "No changes to commit"

echo ""
echo "🎉 Configuration complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push"
echo "2. Go to https://render.com/dashboard"
echo "3. Click 'New' → 'Blueprint'"
echo "4. Connect this repository"
echo "5. Add these environment variables in Render Dashboard:"
echo "   - BETTER_AUTH_SECRET: $SECRET"
echo "   - OPENAI_API_KEY: (your OpenAI API key)"
echo "   - ANTHROPIC_API_KEY: (your Anthropic API key)"
echo "   - Add other API keys as needed"
echo ""
echo "6. Click 'Deploy Blueprint'"
echo ""
echo "Your Sim Studio will be available at: https://$DOMAIN"
echo ""