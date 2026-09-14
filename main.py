#!/usr/bin/env python3
"""
Main Entry Point - Ghibli Cake Video Generator
Run this script to generate the complete video
"""

import os
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="🎬 Generate Ghibli-inspired anime video from text recipes"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/ghibli_chocolate_cake.mp4",
        help="Output video file path"
    )
    parser.add_argument(
        "--quality",
        type=str,
        choices=["480p", "720p", "1080p", "4k"],
        default="4k",
        help="Video quality"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second (default: 30)"
    )
    parser.add_argument(
        "--frames-only",
        action="store_true",
        help="Only generate frames without video composition"
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Only generate ASMR audio"
    )
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     🎨 Ghibli Cake Video Generator 🍰                     ║
    ║  Transform Recipes into Beautiful Anime Videos            ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Import generators
    try:
        from scene_generator import GhibliSceneGenerator
        from asmr_generator import ASMRGenerator
        from video_composer import VideoComposer
        from config import RECIPE_STEPS
    except ImportError as e:
        print(f"❌ Error importing modules: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    # Create output directory
    output_dir = os.path.dirname(args.output) or "output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    print(f"🎬 Quality: {args.quality.upper()}")
    print(f"⏱️  FPS: {args.fps}")
    
    # Generate frames only
    if args.frames_only:
        print("\n📸 Generating frames only...\n")
        scene_gen = GhibliSceneGenerator()
        frames_dir = os.path.join(output_dir, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        
        # Intro
        intro = scene_gen.create_intro_frame()
        intro.save(f"{frames_dir}/intro.png")
        print("✓ Intro frame")
        
        # Steps
        for i, step in enumerate(RECIPE_STEPS):
            frame = scene_gen.create_cooking_frame(i)
            frame.save(f"{frames_dir}/step_{i:02d}.png")
            print(f"✓ Step {i+1}: {step[:40]}...")
        
        # Outro
        outro = scene_gen.create_outro_frame()
        outro.save(f"{frames_dir}/outro.png")
        print("✓ Outro frame")
        
        print(f"\n✅ Frames saved to: {frames_dir}")
        return
    
    # Generate audio only
    if args.audio_only:
        print("\n🔊 Generating ASMR audio only...\n")
        asmr_gen = ASMRGenerator()
        
        timeline = {
            2: "egg_crack",
            3: "egg_crack",
            4: "egg_crack",
            5: "whisking",
            8: "whisking",
            11: "pouring",
            14: "pouring",
            18: "sifting",
            21: "sifting",
            24: "whisking",
            27: "whisking",
            30: "pouring",
        }
        
        import numpy as np
        total_duration = 120
        final_audio = np.zeros(int(asmr_gen.sample_rate * total_duration))
        
        for time_point, sound_name in timeline.items():
            if sound_name == "egg_crack":
                sound = asmr_gen.generate_egg_crack()
            elif sound_name == "whisking":
                sound = asmr_gen.generate_whisking()
            elif sound_name == "pouring":
                sound = asmr_gen.generate_pouring()
            elif sound_name == "sifting":
                sound = asmr_gen.generate_sifting()
            else:
                continue
            
            start_sample = int(time_point * asmr_gen.sample_rate)
            end_sample = start_sample + len(sound)
            
            if end_sample <= len(final_audio):
                final_audio[start_sample:end_sample] += sound * 0.7
        
        final_audio = asmr_gen.normalize_audio(final_audio, target_db=-6)
        audio_path = os.path.join(output_dir, "asmr_audio.wav")
        asmr_gen.save_wav(final_audio, audio_path)
        
        print(f"✅ Audio saved to: {audio_path}")
        return
    
    # Full video generation
    print("\n🎬 Starting full video generation...\n")
    
    try:
        composer = VideoComposer()
        output_file = composer.compose_video()
        
        # File info
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
            print(f"\n📊 Video Statistics:")
            print(f"   File size: {file_size:.2f} MB")
            print(f"   Format: MP4 (9:16 vertical)")
            print(f"   Resolution: 1080x1920")
            print(f"   Audio: ASMR (44.1kHz, AAC)")
            
            print(f"\n✨ Your video is ready!")
            print(f"📱 Perfect for: TikTok, Instagram Reels, YouTube Shorts")
            print(f"🔗 File: {os.path.abspath(output_file)}")
        
    except Exception as e:
        print(f"\n❌ Error during video generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
