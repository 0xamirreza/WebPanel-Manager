#!/bin/bash

echo "🚀 Starting Web Panel Manager..."
echo "=================================="

# Stop any running containers
echo "Stopping containers..."
docker-compose down

# Create data directory with proper permissions
echo "📁 Creating data directory..."
mkdir -p data

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Running as root. This is not recommended for security reasons."
    echo "   Consider running as a regular user and using sudo when needed."
fi

# Set permissions
echo "🔐 Setting proper permissions..."

# Try to set ownership to UID 1000 (container user)
if sudo chown -R 1000:1000 data 2>/dev/null; then
    echo "✅ Successfully set ownership to UID 1000"
    chmod 755 data
else
    echo "⚠️  Could not set ownership to UID 1000"
    echo "   Setting world-writable permissions (less secure)"
    chmod 777 data
fi

# Verify permissions
echo "📊 Current permissions:"
ls -la data/ 2>/dev/null || echo "   Data directory not accessible"

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
