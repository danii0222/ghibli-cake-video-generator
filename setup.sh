#!/bin/bash
# Setup script for Ghibli Cake Video Generator

echo "╔════════════════════════════════════════════════╗"
echo "║   🎨 Ghibli Cake Video Generator Setup 🍰      ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check FFmpeg
echo ""
echo "🎬 Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg not found."
    echo "Please install FFmpeg:"
    echo ""
    echo "  macOS:     brew install ffmpeg"
    echo "  Ubuntu:    sudo apt-get install ffmpeg"
    echo "  Windows:   choco install ffmpeg (or download from ffmpeg.org)"
    echo ""
    read -p "Continue without FFmpeg? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n 1)
    echo "   ✓ $ffmpeg_version"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create output directory
echo ""
echo "📁 Creating output directory..."
mkdir -p output/frames
echo "✓ Output directory ready"

# Summary
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║          ✅ Setup Complete! 🎉                 ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "🚀 Ready to generate videos!"
echo ""
echo "Quick start commands:"
echo ""
echo "  # Generate full video"
echo "  python3 main.py"
echo ""
echo "  # Generate with custom output"
echo "  python3 main.py --output my_video.mp4"
echo ""
echo "  # Generate only frames"
echo "  python3 main.py --frames-only"
echo ""
echo "  # Generate only audio"
echo "  python3 main.py --audio-only"
echo ""
echo "📖 For more options, run:"
echo "  python3 main.py --help"
echo ""
