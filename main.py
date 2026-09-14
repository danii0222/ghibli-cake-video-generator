#!/usr/bin/env python3
"""
Main script to generate complete Ghibli-style cake video
Usage:
    python main.py              # Generate with medium quality (default)
    python main.py low          # Generate with low quality (faster)
    python main.py high         # Generate with high quality (slower, better)
"""

import sys
from video_composer import VideoComposer

def main():
    print("=" * 60)
    print("🎬 Ghibli Cake Video Generator")
    print("=" * 60)
    print()
    
    # Get quality from command line or default to 'medium'
    quality = sys.argv[1] if len(sys.argv) > 1 else 'medium'
    
    if quality not in ['low', 'medium', 'high']:
        print(f"❌ Invalid quality '{quality}'")
        print("Usage: python main.py [low|medium|high]")
        print("  - low: Fast generation (2000k bitrate)")
        print("  - medium: Balanced quality (4000k bitrate)")
        print("  - high: Best quality (8000k bitrate)")
        sys.exit(1)
    
    print(f"📊 Quality Mode: {quality.upper()}")
    print()
    
    # Create video composer
    composer = VideoComposer(quality=quality)
    
    # Generate complete video
    output_path = composer.compose_video()
    
    if output_path:
        print()
        print("=" * 60)
        print("✅ فيديو كعكة الشوكولاتة جاهز!")
        print(f"📁 الملف: {output_path}")
        print("=" * 60)
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("❌ فشل في إنشاء الفيديو")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
