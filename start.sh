#!/bin/bash

# Building Safety Risk Analyzer - Python/Streamlit Version
# Startup script

echo "🏢 Building Safety Risk Analyzer - Python Version"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the python/ directory."
    exit 1
fi

# Check if .env file exists and has required variables
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found."
    echo "Please create .env file with your Azure OpenAI configuration:"
    echo "4.1_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/"
    echo "4.1_OPENAI_API_KEY=your-api-key-here"
    echo "4.1_OPENAI_DEPLOYMENT_NAME=gpt-4-vision"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, openai, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing required packages..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please install manually:"
        echo "pip install -r requirements.txt"
        exit 1
    fi
fi

echo "✅ Dependencies verified"

# Check environment variables
echo "🔧 Checking configuration..."
source .env

if [ -z "$4.1_OPENAI_ENDPOINT" ] || [ -z "$4.1_OPENAI_API_KEY" ] || [ -z "$4.1_OPENAI_DEPLOYMENT_NAME" ]; then
    echo "⚠️  Warning: Some environment variables are not set."
    echo "Please update your .env file with proper Azure OpenAI configuration."
    echo ""
    echo "Required variables:"
    echo "- 4.1_OPENAI_ENDPOINT"
    echo "- 4.1_OPENAI_API_KEY"  
    echo "- 4.1_OPENAI_DEPLOYMENT_NAME"
    echo ""
    echo "The application will start but may not function properly without proper configuration."
fi

echo "🚀 Starting Building Safety Risk Analyzer..."
echo "📊 The application will open in your default browser"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Streamlit application
streamlit run app.py --server.port 8501 --server.address localhost