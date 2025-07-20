# Create the complete file structure for Sim Studio deployment on Render
# Following the n8n pattern but adapted for Sim Studio

# First, let's create the render.yaml blueprint file
render_yaml = """services:
  - type: web
    name: simstudio
    env: docker
    region: oregon # optional (defaults to oregon)
    plan: standard # optional (defaults to starter)
    branch: main # optional (defaults to master)
    numInstances: 1
    healthCheckPath: /
    dockerfilePath: ./Dockerfile
    dockerContext: ./
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: simstudio-db
          property: connectionString
      - key: BETTER_AUTH_SECRET
        generateValue: true
      - key: BETTER_AUTH_URL
        value: https://your-simstudio-app.onrender.com
      - key: WEBHOOK_URL
        value: https://your-simstudio-app.onrender.com/
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 3000
      - key: NEXTAUTH_URL
        value: https://your-simstudio-app.onrender.com
      - key: OPENAI_API_KEY
        sync: false # Prompt for value in Render Dashboard
      - key: ANTHROPIC_API_KEY
        sync: false # Prompt for value in Render Dashboard
      - key: GOOGLE_API_KEY
        sync: false # Prompt for value in Render Dashboard
      - key: DISABLE_REGISTRATION
        value: "false"
    disk:
      name: simstudio-disk
      mountPath: /app/data
      sizeGB: 5

  - type: pserv
    name: realtime-server
    env: docker
    region: oregon
    plan: starter
    branch: main
    dockerfilePath: ./Dockerfile.realtime
    dockerContext: ./
    envVars:
      - key: PORT
        value: 3001
      - key: NODE_ENV
        value: production
      - fromService:
          name: simstudio-db
          type: postgres
          envVarKey: DATABASE_URL

databases:
  - name: simstudio-db
    plan: basic-1gb
    databaseName: simstudio
    user: simstudio_user
"""

# Create the main Dockerfile
dockerfile = """# Use the official Node.js image
FROM node:20-alpine AS base

# Install system dependencies
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \\
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \\
  elif [ -f package-lock.json ]; then npm ci; \\
  elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm i --frozen-lockfile; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

# Build the application
FROM base AS builder
WORKDIR /app
COPY . .

# Set build-time environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Build the Next.js application
RUN \\
  if [ -f yarn.lock ]; then yarn build; \\
  elif [ -f package-lock.json ]; then npm run build; \\
  elif [ -f pnpm-lock.yaml ]; then pnpm run build; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

# Production image
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Create data directory for persistent storage
RUN mkdir -p /app/data && chown nextjs:nodejs /app/data

USER nextjs

EXPOSE 3000

ENV PORT=3000

CMD ["node", "server.js"]
"""

# Create the realtime server Dockerfile
dockerfile_realtime = """FROM node:20-alpine AS base

# Install system dependencies
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \\
  if [ -f yarn.lock ]; then yarn --frozen-lockfile --production; \\
  elif [ -f package-lock.json ]; then npm ci --only=production; \\
  elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm i --frozen-lockfile --prod; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

# Copy application files
COPY . .

# Build the realtime server if needed
RUN \\
  if [ -f yarn.lock ]; then yarn build:realtime; \\
  elif [ -f package-lock.json ]; then npm run build:realtime; \\
  elif [ -f pnpm-lock.yaml ]; then pnpm run build:realtime; \\
  else echo "Starting realtime server"; \\
  fi

EXPOSE 3001

ENV NODE_ENV=production
ENV PORT=3001

CMD ["node", "apps/realtime/dist/index.js"]
"""

# Create package.json
package_json = """{
  "name": "simstudio-render",
  "version": "1.0.0",
  "description": "Sim Studio deployment for Render",
  "main": "index.js",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "dev:realtime": "cd apps/realtime && npm run dev",
    "build:realtime": "cd apps/realtime && npm run build",
    "migrate": "cd apps/sim && bunx drizzle-kit push"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@next/bundle-analyzer": "^14.0.0",
    "socket.io": "^4.7.0",
    "socket.io-client": "^4.7.0",
    "drizzle-orm": "^0.29.0",
    "drizzle-kit": "^0.20.0",
    "postgres": "^3.4.0",
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}"""

# Create environment variables example file
env_example = """# Database
DATABASE_URL=postgresql://username:password@localhost:5432/simstudio

# Authentication
BETTER_AUTH_SECRET=your-super-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
NEXTAUTH_URL=http://localhost:3000

# Application
NODE_ENV=development
PORT=3000
WEBHOOK_URL=http://localhost:3000/

# AI API Keys (Optional - Add your API keys)
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key
DEEPSEEK_API_KEY=your-deepseek-api-key

# Features
DISABLE_REGISTRATION=false
NEXT_TELEMETRY_DISABLED=1

# Realtime Server
REALTIME_PORT=3001
"""

# Create docker-compose.yml for local development
docker_compose = """version: '3.8'

services:
  simstudio:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://simstudio:simstudio@db:5432/simstudio
      - BETTER_AUTH_SECRET=your-development-secret
      - BETTER_AUTH_URL=http://localhost:3000
      - NODE_ENV=development
    depends_on:
      - db
      - realtime
    volumes:
      - simstudio-data:/app/data

  realtime:
    build:
      context: .
      dockerfile: Dockerfile.realtime
    ports:
      - "3001:3001"
    environment:
      - DATABASE_URL=postgresql://simstudio:simstudio@db:5432/simstudio
      - PORT=3001
      - NODE_ENV=development
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: simstudio
      POSTGRES_USER: simstudio
      POSTGRES_PASSWORD: simstudio
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
  simstudio-data:
"""

# Create README.md
readme = """# Sim Studio on Render

Successfully deploy Sim Studio on Render using Docker with the latest configurations and best practices.

## Quick Start

1. Fork this repository or use it as a template
2. Open your Render Dashboard and use this repo as a Blueprint
3. Update the `WEBHOOK_URL` and `BETTER_AUTH_URL` environment variables in `render.yaml` to your domain
4. Configure your AI API keys in the Render Dashboard environment variables
5. Deploy and enjoy!

## Important Notes

- **Do not change the storage volume mount path** (`/app/data`) - this is where persistent data is stored
- The `.env.example` file contains examples that can be added manually as Environment Variables in Render
- Always set the `WEBHOOK_URL` and `BETTER_AUTH_URL` to your actual domain to avoid localhost issues
- Uses the latest Sim Studio configuration with multi-service architecture

## What's Included (2025)

- ✅ Multi-service architecture (main app + realtime server)
- ✅ PostgreSQL database with proper connection handling
- ✅ Persistent disk storage for data
- ✅ Environment variable management
- ✅ Docker-based deployment
- ✅ Production-optimized Next.js build
- ✅ Socket.io realtime server
- ✅ Compatible with latest Sim Studio versions

## Services Architecture

This deployment creates multiple interconnected services:

### Main Application (`simstudio`)
- **Type**: Web Service
- **Framework**: Next.js with App Router
- **Port**: 3000
- **Features**: Main UI, API routes, authentication
- **Storage**: 5GB persistent disk mounted at `/app/data`

### Realtime Server (`realtime-server`)
- **Type**: Private Service
- **Framework**: Socket.io server
- **Port**: 3001
- **Purpose**: Real-time collaboration and updates

### Database (`simstudio-db`)
- **Type**: PostgreSQL Database
- **Plan**: Basic 1GB
- **Purpose**: Store workflows, user data, and application state

## Environment Variables

The following variables should be configured in your Render dashboard:

### Required Variables
- `BETTER_AUTH_SECRET` - Generate a secure random string (auto-generated)
- `BETTER_AUTH_URL` - Your Sim Studio domain (e.g., `https://your-app.onrender.com`)
- `WEBHOOK_URL` - Your Sim Studio domain (e.g., `https://your-app.onrender.com/`)

### Optional AI API Keys
- `OPENAI_API_KEY` - For OpenAI models
- `ANTHROPIC_API_KEY` - For Claude models  
- `GOOGLE_API_KEY` - For Google AI models
- `DEEPSEEK_API_KEY` - For DeepSeek models

### System Variables (Auto-configured)
- `DATABASE_URL` - Auto-populated by Render from database connection
- `NODE_ENV` - Set to `production`
- `PORT` - Application port (3000)

## Local Development

To run locally for development:

```bash
# Clone the repository
git clone <your-forked-repo>
cd simstudio-render

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start with Docker Compose
docker compose up -d

# Or start manually
npm install
npm run build
npm start
```

## Deployment Process

1. **Fork this repository** to your GitHub account
2. **Update configuration**:
   - Edit `render.yaml` and change `your-simstudio-app.onrender.com` to your desired domain
   - Commit the changes
3. **Deploy on Render**:
   - Go to Render Dashboard
   - Click "New" → "Blueprint"
   - Connect your forked repository
   - Click "Deploy Blueprint"
4. **Configure environment variables**:
   - Add your AI API keys in the Render Dashboard
   - Update the `BETTER_AUTH_URL` and `WEBHOOK_URL` with your actual domain
5. **Wait for deployment** (5-10 minutes)
6. **Access your application** at your Render domain

## Troubleshooting

### Common Issues

**Authentication not working:**
- Ensure `BETTER_AUTH_URL` matches your actual domain
- Verify `BETTER_AUTH_SECRET` is properly generated

**Realtime features not working:**
- Check that the realtime server is running
- Verify database connections are working

**AI models not responding:**
- Verify your API keys are correctly set
- Check the Render logs for API key validation errors

**Database connection issues:**
- Ensure database service is running
- Check that `DATABASE_URL` is properly configured

### Checking Logs

To view application logs:
1. Go to Render Dashboard
2. Click on your service name
3. Go to "Logs" tab

### Database Access

To access your PostgreSQL database:
1. Go to Render Dashboard  
2. Click on your database service
3. Use the connection details provided

## Scaling and Performance

### Upgrading Plans

For production use, consider upgrading:
- **Web Service**: From Starter to Standard or Pro
- **Database**: From Basic to Standard for better performance
- **Realtime Server**: From Starter to Standard for better performance

### Performance Optimization

- Enable Redis caching (can be added as another service)
- Configure CDN for static assets
- Use database connection pooling
- Monitor resource usage in Render Dashboard

## Support and Community

- **Documentation**: [Sim Studio Docs](https://docs.simstudio.ai)
- **GitHub**: [simstudioai/sim](https://github.com/simstudioai/sim)  
- **Community**: Join the Discord community
- **Issues**: Report bugs on GitHub Issues

## License

This deployment configuration is provided under the same license as Sim Studio (Apache 2.0).

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

Made with ❤️ for the Sim Studio community
"""

# Create deployment script
deploy_script = """#!/bin/bash

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
"""

# Create health check script  
health_check = """#!/bin/bash

# Health check script for Sim Studio
# This script verifies that all services are running properly

echo "🏥 Sim Studio Health Check"
echo "========================="

# Check if main application is responding
echo "🔍 Checking main application..."
if curl -f -s "http://localhost:3000/health" > /dev/null; then
    echo "✅ Main application is healthy"
else
    echo "❌ Main application is not responding"
    exit 1
fi

# Check if realtime server is responding  
echo "🔍 Checking realtime server..."
if curl -f -s "http://localhost:3001/health" > /dev/null; then
    echo "✅ Realtime server is healthy"
else
    echo "❌ Realtime server is not responding"
    exit 1
fi

# Check database connection
echo "🔍 Checking database connection..."
if [ -n "$DATABASE_URL" ]; then
    # Try to connect to database
    if timeout 5 bash -c "</dev/tcp/$(echo $DATABASE_URL | cut -d'@' -f2 | cut -d':' -f1)/$(echo $DATABASE_URL | cut -d':' -f4 | cut -d'/' -f1)" 2>/dev/null; then
        echo "✅ Database connection is healthy"
    else
        echo "❌ Cannot connect to database"
        exit 1
    fi
else
    echo "⚠️ DATABASE_URL not set, skipping database check"
fi

echo ""
echo "🎉 All health checks passed!"
"""

# Save all files
files_to_create = {
    'render.yaml': render_yaml.strip(),
    'Dockerfile': dockerfile.strip(),
    'Dockerfile.realtime': dockerfile_realtime.strip(),
    'package.json': package_json,
    '.env.example': env_example.strip(),
    'docker-compose.yml': docker_compose.strip(),
    'README.md': readme.strip(),
    'deploy.sh': deploy_script.strip(),
    'health-check.sh': health_check.strip()
}

# Create and save each file
for filename, content in files_to_create.items():
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✅ Created {filename}")

print(f"\n🎉 Successfully created {len(files_to_create)} files for Sim Studio deployment on Render!")
print("\nFiles created:")
for filename in files_to_create.keys():
    print(f"  - {filename}")

# Make shell scripts executable
import os
os.chmod('deploy.sh', 0o755)
os.chmod('health-check.sh', 0o755)
print("\n✅ Made shell scripts executable")