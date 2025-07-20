# Sim Studio on Render

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