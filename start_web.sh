#!/bin/bash
# Simple startup script for the Learning Orchestrator Web Interface

echo "=================================================="
echo "🚀 Starting Learning Orchestrator Web Interface"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip3 install -q -r requirements.txt

echo "✅ Dependencies ready"
echo ""

# Get local IP address
LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP=$(ifconfig 2>/dev/null | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
fi

echo "🌐 Starting server..."
echo ""
echo "📱 Access the interface at:"
echo "   • On this device: http://localhost:5000"
if [ ! -z "$LOCAL_IP" ]; then
    echo "   • On your phone (same WiFi): http://$LOCAL_IP:5000"
fi
echo ""
echo "💡 Tip: On your phone, use 'Add to Home Screen' for an app-like experience!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo ""

# Start the web app
python3 web_app.py
