#!/bin/bash

echo "🧹 Cleaning up Web Panel Manager..."
echo "=================================="

# Stop any running containers
echo "Stopping containers..."
docker-compose down

# Rebuild the image
echo "Rebuilding Docker image..."
docker-compose build

# Start the application
echo "Starting application..."
docker-compose up -d

# Wait a moment
sleep 3

# Check status
echo ""
echo "📊 Status Check:"
if docker-compose ps | grep -q "Up"; then
    echo "✅ Container is running"
    
    if [ -f "data/webpanel_manager.db" ]; then
        echo "✅ Database file created successfully"
        echo "📁 Database location: data/webpanel_manager.db"
        echo "📊 Database size: $(du -h data/webpanel_manager.db 2>/dev/null | cut -f1 || echo 'N/A')"
    else
        echo "⏳ Database file will be created on first use"
    fi
    
    echo ""
    echo "🌐 Application is running at: http://localhost:44553"
    echo "💾 Data will now persist in: ./data/webpanel_manager.db"
    
else
    echo "❌ Container failed to start"
    echo "📋 Logs:"
    docker-compose logs
fi
