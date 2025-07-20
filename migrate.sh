#!/bin/bash

# Database migration script for Sim Studio
# This script handles database setup and migrations

set -e

echo "🗄️ Sim Studio Database Migration"
echo "================================="

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL environment variable is not set"
    exit 1
fi

echo "✅ DATABASE_URL is configured"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    if [ -f "yarn.lock" ]; then
        yarn install
    elif [ -f "package-lock.json" ]; then
        npm ci
    else
        npm install
    fi
fi

# Run database migrations
echo "🔄 Running database migrations..."

# Check if we're using Drizzle (Sim Studio's ORM)
if [ -f "apps/sim/drizzle.config.ts" ]; then
    cd apps/sim
    echo "Running Drizzle migrations..."
    npx drizzle-kit push
    cd ../..
else
    echo "⚠️ No Drizzle configuration found, skipping migrations"
fi

# Seed database if needed
echo "🌱 Seeding database (if needed)..."

# Add any seed data commands here
# For example:
# npx tsx scripts/seed.ts

echo "✅ Database migration completed successfully!"
