#!/bin/bash

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