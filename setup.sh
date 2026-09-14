#!/bin/bash
# Setup script for Ghibli Cake Video Generator
# Handles FFmpeg installation and Python dependencies

echo "🎬 Setting up Ghibli Cake Video Generator..."
echo ""

# Detect OS
OS_TYPE=$(uname -s)

# Install FFmpeg based on OS
echo "📦 Installing FFmpeg..."
if [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        brew install ffmpeg
        echo "✓ FFmpeg installed via Homebrew"
    else
        echo "❌ Homebrew not found. Please install from: https://brew.sh"
        exit 1
    fi
elif [[ "$OS_TYPE" == "Linux" ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
        echo "✓ FFmpeg installed via apt"
    elif command -v yum &> /dev/null; then
        sudo yum install -y ffmpeg
        echo "✓ FFmpeg installed via yum"
    else
        echo "❌ Could not install FFmpeg. Please install manually from: https://ffmpeg.org/download.html"
        exit 1
    fi
elif [[ "$OS_TYPE" == "MINGW64_NT" ]] || [[ "$OS_TYPE" == "MSYS_NT" ]]; then
    # Windows (Git Bash)
    echo "❌ Please install FFmpeg manually from: https://ffmpeg.org/download.html"
    echo "   Add FFmpeg to your PATH environment variable"
    exit 1
fi

# Install Python dependencies
echo ""
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo "🚀 Run: python main.py"
