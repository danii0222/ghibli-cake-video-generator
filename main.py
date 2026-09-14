#!/usr/bin/env python3
"""
Main script to generate complete Ghibli-style cake video
Run: python main.py
"""

from video_composer import VideoComposer

def main():
    print("=" * 60)
    print("🎬 Ghibli Cake Video Generator")
    print("=" * 60)
    print()
    
    # Create video composer
    composer = VideoComposer()
    
    # Generate complete video
    output_path = composer.compose_video()
    
    print()
    print("=" * 60)
    print("✅ فيديو كعكة الشوكولاتة جاهز!")
    print(f"📁 الملف: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
