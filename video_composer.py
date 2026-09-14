"""
Video Composer - Combines scenes, audio, and effects into final video
Generates 4K 9:16 vertical video with ASMR audio
"""

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import os
from config import VIDEO_FPS, VIDEO_WIDTH, VIDEO_HEIGHT, SCENES, RECIPE_STEPS
from scene_generator import GhibliSceneGenerator
from asmr_generator import ASMRGenerator

class VideoComposer:
    def __init__(self):
        self.fps = VIDEO_FPS
        self.width = VIDEO_WIDTH
        self.height = VIDEO_HEIGHT
        self.scene_gen = GhibliSceneGenerator(self.width, self.height)
        self.asmr_gen = ASMRGenerator()
        
    def create_frame_sequence(self):
        """Create all frames needed for the video"""
        frames_dir = "output/frames"
        os.makedirs(frames_dir, exist_ok=True)
        
        frame_files = []
        
        # Intro frame
        intro_frame = self.scene_gen.create_intro_frame()
        intro_path = f"{frames_dir}/intro.png"
        intro_frame.save(intro_path)
        frame_files.append(("intro", intro_path, SCENES["intro"]))
        
        print("✓ Intro frame created")
        
        # Cooking steps
        step_timings = [
            ("crack_eggs", 0),
            ("add_sugar", 1),
            ("pour_liquids", 2),
            ("sift_dry", 3),
            ("whisk_batter", 4),
            ("pour_batter", 5),
            ("oven", 6),
        ]
        
        for step_name, step_index in step_timings:
            frame = self.scene_gen.create_cooking_frame(step_index)
            frame_path = f"{frames_dir}/{step_name}.png"
            frame.save(frame_path)
            frame_files.append((step_name, frame_path, SCENES.get(step_name, 8)))
            print(f"✓ {step_name} frame created")
        
        # Outro frame
        outro_frame = self.scene_gen.create_outro_frame()
        outro_path = f"{frames_dir}/outro.png"
        outro_frame.save(outro_path)
        frame_files.append(("outro", outro_path, SCENES["outro"]))
        
        print("✓ Outro frame created")
        
        return frame_files
    
    def create_audio_track(self):
        """Create ASMR audio track"""
        audio_path = "output/asmr_audio.wav"
        os.makedirs("output", exist_ok=True)
        
        # Timeline for sounds throughout the video
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
        
        # Generate audio with 2-minute duration
        total_duration = 120
        final_audio = np.zeros(int(self.asmr_gen.sample_rate * total_duration))
        
        for time_point, sound_name in timeline.items():
            if sound_name == "egg_crack":
                sound = self.asmr_gen.generate_egg_crack()
            elif sound_name == "whisking":
                sound = self.asmr_gen.generate_whisking()
            elif sound_name == "pouring":
                sound = self.asmr_gen.generate_pouring()
            elif sound_name == "sifting":
                sound = self.asmr_gen.generate_sifting()
            else:
                continue
            
            start_sample = int(time_point * self.asmr_gen.sample_rate)
            end_sample = start_sample + len(sound)
            
            if end_sample <= len(final_audio):
                final_audio[start_sample:end_sample] += sound * 0.7  # Mix at 70% volume
        
        # Normalize
        final_audio = self.asmr_gen.normalize_audio(final_audio, target_db=-6)
        
        # Save
        self.asmr_gen.save_wav(final_audio, audio_path)
        print("✓ ASMR audio track created")
        
        return audio_path
    
    def compose_video(self):
        """Compose final video from frames and audio"""
        print("\n🎬 Starting video composition...\n")
        
        # Create frames
        frame_files = self.create_frame_sequence()
        
        # Create audio
        audio_path = self.create_audio_track()
        
        # Build video clips
        print("\n🎨 Composing video clips...")
        clips = []
        
        for name, frame_path, duration in frame_files:
            clip = ImageClip(frame_path).set_duration(duration)
            clips.append(clip)
            print(f"  ✓ {name}: {duration}s")
        
        # Concatenate clips
        video = concatenate_videoclips(clips, method="chain")
        
        # Set video properties
        video = video.set_fps(self.fps)
        
        # Add audio
        print("\n🔊 Adding ASMR audio...")
        audio = AudioFileClip(audio_path)
        video = video.set_audio(audio)
        
        # Export video
        output_path = "output/ghibli_chocolate_cake.mp4"
        os.makedirs("output", exist_ok=True)
        
        print(f"\n📝 Rendering video to {output_path}...")
        print(f"   Resolution: {self.width}x{self.height} (9:16)")
        print(f"   FPS: {self.fps}")
        print(f"   Quality: 4K")
        
        # Render with high quality settings
        video.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            preset='medium',  # medium preset for better quality
            bitrate="8000k"   # High bitrate for 4K
        )
        
        print(f"\n✅ Video created successfully!")
        print(f"📁 Output: {output_path}")
        
        # Cleanup
        video.close()
        audio.close()
        
        return output_path


if __name__ == "__main__":
    composer = VideoComposer()
    composer.compose_video()
