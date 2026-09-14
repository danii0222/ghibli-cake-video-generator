"""
Video Composer - Combines scenes, audio, and effects into final video
Generates 4K 9:16 vertical video with ASMR audio
Improved version with better error handling and optimization
"""

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import os
import sys
from config import VIDEO_FPS, VIDEO_WIDTH, VIDEO_HEIGHT, SCENES, RECIPE_STEPS
from scene_generator import GhibliSceneGenerator
from asmr_generator import ASMRGenerator

class VideoComposer:
    def __init__(self, quality="medium"):
        """
        Initialize video composer
        quality: 'low' (fast, smaller file), 'medium' (balanced), 'high' (better quality, slower)
        """
        self.fps = VIDEO_FPS
        self.width = VIDEO_WIDTH
        self.height = VIDEO_HEIGHT
        self.quality = quality
        self.scene_gen = GhibliSceneGenerator(self.width, self.height)
        self.asmr_gen = ASMRGenerator()
        
        # Quality presets
        self.quality_settings = {
            'low': {
                'preset': 'ultrafast',
                'bitrate': '2000k',
                'crf': 28
            },
            'medium': {
                'preset': 'fast',
                'bitrate': '4000k',
                'crf': 23
            },
            'high': {
                'preset': 'medium',
                'bitrate': '8000k',
                'crf': 18
            }
        }
        
    def create_frame_sequence(self):
        """Create all frames needed for the video"""
        try:
            frames_dir = "output/frames"
            os.makedirs(frames_dir, exist_ok=True)
            
            frame_files = []
            
            # Intro frame
            print("🎨 Creating intro frame...")
            intro_frame = self.scene_gen.create_intro_frame()
            intro_path = f"{frames_dir}/intro.png"
            intro_frame.save(intro_path, quality=95)
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
                print(f"🎨 Creating {step_name} frame...")
                frame = self.scene_gen.create_cooking_frame(step_index)
                frame_path = f"{frames_dir}/{step_name}.png"
                frame.save(frame_path, quality=95)
                frame_files.append((step_name, frame_path, SCENES.get(step_name, 8)))
                print(f"✓ {step_name} frame created")
            
            # Outro frame
            print("🎨 Creating outro frame...")
            outro_frame = self.scene_gen.create_outro_frame()
            outro_path = f"{frames_dir}/outro.png"
            outro_frame.save(outro_path, quality=95)
            frame_files.append(("outro", outro_path, SCENES["outro"]))
            print("✓ Outro frame created")
            
            return frame_files
            
        except Exception as e:
            print(f"✗ خطأ في إنشاء الإطارات: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def create_audio_track(self):
        """Create ASMR audio track"""
        try:
            audio_path = "output/asmr_audio.wav"
            os.makedirs("output", exist_ok=True)
            
            print("🎵 Generating ASMR audio...")
            
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
                try:
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
                except Exception as e:
                    print(f"⚠️  خطأ في إنشاء {sound_name}: {str(e)}")
                    continue
            
            # Normalize
            final_audio = self.asmr_gen.normalize_audio(final_audio, target_db=-6)
            
            # Save
            self.asmr_gen.save_wav(final_audio, audio_path)
            print("✓ ASMR audio track created")
            
            return audio_path
            
        except Exception as e:
            print(f"✗ خطأ في إنشاء الصوت: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def compose_video(self):
        """Compose final video from frames and audio"""
        print("\n" + "="*60)
        print("🎬 Starting video composition...")
        print("="*60 + "\n")
        
        try:
            # Create frames
            frame_files = self.create_frame_sequence()
            
            if not frame_files:
                print("✗ Failed to create frames")
                return None
            
            # Create audio
            audio_path = self.create_audio_track()
            
            if not audio_path or not os.path.exists(audio_path):
                print("✗ Failed to create audio")
                return None
            
            # Build video clips
            print("\n🎨 Composing video clips...")
            clips = []
            
            for name, frame_path, duration in frame_files:
                try:
                    if not os.path.exists(frame_path):
                        print(f"  ✗ Frame file not found: {frame_path}")
                        continue
                    
                    clip = ImageClip(frame_path).set_duration(duration)
                    clips.append(clip)
                    print(f"  ✓ {name}: {duration}s")
                    
                except Exception as e:
                    print(f"  ✗ Error loading frame {name}: {str(e)}")
                    continue
            
            if not clips:
                print("✗ No valid clips created")
                return None
            
            print(f"\n✓ Total clips: {len(clips)}")
            
            # Concatenate clips
            print("\n⚙️  Concatenating video clips...")
            try:
                video = concatenate_videoclips(clips, method="chain")
            except Exception as e:
                print(f"✗ Error concatenating clips: {str(e)}")
                return None
            
            # Set video properties
            video = video.set_fps(self.fps)
            
            # Add audio
            print("🔊 Adding ASMR audio...")
            try:
                audio = AudioFileClip(audio_path)
                video = video.set_audio(audio)
            except Exception as e:
                print(f"⚠️  Warning: Could not add audio: {str(e)}")
            
            # Export video
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = f"{output_dir}/ghibli_chocolate_cake.mp4"
            
            print(f"\n📝 Rendering video...")
            print(f"   Resolution: {self.width}x{self.height} (9:16)")
            print(f"   FPS: {self.fps}")
            print(f"   Quality: {self.quality}")
            print(f"   Output: {output_path}\n")
            
            # Get quality settings
            settings = self.quality_settings.get(self.quality, self.quality_settings['medium'])
            
            # Render with quality settings
            try:
                video.write_videofile(
                    output_path,
                    fps=self.fps,
                    codec='libx264',
                    audio_codec='aac',
                    preset=settings['preset'],
                    bitrate=settings['bitrate'],
                    verbose=False,
                    logger=None,
                    temp_audiofile='temp_audio.m4a',
                    remove_temp=True
                )
                
                print(f"\n{'='*60}")
                print(f"✅ Video created successfully!")
                print(f"📁 Output: {os.path.abspath(output_path)}")
                print(f"{'='*60}\n")
                
                # Cleanup
                try:
                    video.close()
                    audio.close()
                except:
                    pass
                
                return output_path
                
            except Exception as e:
                print(f"✗ Error during video rendering: {str(e)}")
                import traceback
                traceback.print_exc()
                return None
            
        except Exception as e:
            print(f"\n✗ خطأ في إنشاء الفيديو: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    # Get quality from command line or default to 'medium'
    quality = sys.argv[1] if len(sys.argv) > 1 else 'medium'
    
    if quality not in ['low', 'medium', 'high']:
        print(f"Invalid quality '{quality}'. Using 'medium'")
        quality = 'medium'
    
    composer = VideoComposer(quality=quality)
    result = composer.compose_video()
    
    if result:
        print("✓ Done!")
    else:
        print("✗ Failed to create video")
        sys.exit(1)
