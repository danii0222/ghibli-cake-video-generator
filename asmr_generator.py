"""
ASMR Sound Generator
Generates authentic cooking sounds: egg cracking, whisking, pouring, sifting
"""

import numpy as np
import scipy.io.wavfile as wavfile
from config import ASMR_CONFIG
import os

class ASMRGenerator:
    def __init__(self):
        self.sample_rate = ASMR_CONFIG["sample_rate"]
        self.duration = ASMR_CONFIG["duration"]
        
    def generate_egg_crack(self, duration=0.5):
        """Generate egg cracking sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Sharp crackling sound with white noise
        crack = np.random.normal(0, 0.3, len(t))
        
        # Add frequency sweep (low to high)
        freq_sweep = np.linspace(400, 2000, len(t))
        freq_envelope = np.sin(2 * np.pi * freq_sweep * t)
        crack = crack * freq_envelope
        
        # Envelope (attack-decay)
        envelope = np.exp(-5 * t)
        crack = crack * envelope
        
        return crack.astype(np.float32) * 0.7
    
    def generate_whisking(self, duration=1.0):
        """Generate whisking sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Repetitive whisking pattern
        whisk_freq = 15  # 15 whisks per second
        whisk_pattern = np.sin(2 * np.pi * whisk_freq * t)
        
        # Add high-frequency noise
        noise = np.random.normal(0, 0.2, len(t))
        
        # Combine with modulation
        whisking = (whisk_pattern * 0.3 + noise * 0.7)
        
        # Add harmonics (2-4 kHz range)
        harmonic = np.sin(2 * np.pi * 2000 * t) * 0.2
        whisking = whisking + harmonic
        
        # Envelope
        envelope = np.hanning(len(t))
        whisking = whisking * envelope
        
        return whisking.astype(np.float32) * 0.6
    
    def generate_pouring(self, duration=1.5):
        """Generate pouring/liquid sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Filtered brown noise for pouring sound
        noise = np.random.normal(0, 0.4, len(t))
        
        # Simple low-pass by averaging
        pouring = noise.copy()
        for i in range(1, len(pouring)):
            pouring[i] = (pouring[i] + pouring[i-1]) * 0.5
        
        # Add rumble (100-300 Hz)
        rumble = np.sin(2 * np.pi * 150 * t) * 0.3
        pouring = pouring + rumble
        
        # Envelope (fade in and out)
        envelope = np.hanning(len(t))
        pouring = pouring * envelope
        
        return pouring.astype(np.float32) * 0.5
    
    def generate_sifting(self, duration=1.0):
        """Generate sifting sound"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # White noise with rhythmic pattern
        noise = np.random.normal(0, 0.3, len(t))
        
        # Sifting pattern (2 Hz oscillation)
        sift_pattern = (np.sin(2 * np.pi * 2 * t) + 1) / 2  # 0-1
        
        # Combine with frequency sweep
        sifting = noise * sift_pattern
        
        # Add mid-range frequency (1000-1500 Hz)
        mid_freq = np.sin(2 * np.pi * 1200 * t) * 0.2
        sifting = sifting + mid_freq
        
        # Envelope
        envelope = np.hanning(len(t))
        sifting = sifting * envelope
        
        return sifting.astype(np.float32) * 0.6
    
    def normalize_audio(self, audio, target_db=-6):
        """Normalize audio to target loudness"""
        # Calculate RMS
        rms = np.sqrt(np.mean(audio ** 2))
        
        if rms == 0:
            return audio
        
        # Convert target dB to linear
        target_linear = 10 ** (target_db / 20)
        
        # Scale audio
        audio_normalized = audio * (target_linear / rms)
        
        # Prevent clipping
        max_val = np.max(np.abs(audio_normalized))
        if max_val > 1.0:
            audio_normalized = audio_normalized / max_val
        
        return audio_normalized.astype(np.float32)
    
    def save_wav(self, audio, path):
        """Save audio to WAV file"""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        
        # Convert to int16
        audio_int16 = np.int16(audio * 32767)
        
        # Write WAV file
        wavfile.write(path, self.sample_rate, audio_int16)
        print(f"✓ Audio saved to {path}")
    
    def create_silence(self, duration):
        """Create silence"""
        return np.zeros(int(self.sample_rate * duration), dtype=np.float32)


if __name__ == "__main__":
    generator = ASMRGenerator()
    
    # Test individual sounds
    print("Generating ASMR sounds...")
    
    # Generate test audio with all sounds
    from config import SOUND_TIMELINE
    total_duration = 120
    total_samples = int(generator.sample_rate * total_duration)
    full_audio = np.zeros(total_samples)
    
    for time_point, sound_name in SOUND_TIMELINE.items():
        if sound_name == "egg_crack":
            sound = generator.generate_egg_crack()
        elif sound_name == "whisking":
            sound = generator.generate_whisking()
        elif sound_name == "pouring":
            sound = generator.generate_pouring()
        elif sound_name == "sifting":
            sound = generator.generate_sifting()
        else:
            continue
        
        start_sample = int(time_point * generator.sample_rate)
        end_sample = start_sample + len(sound)
        
        if end_sample <= len(full_audio):
            full_audio[start_sample:end_sample] += sound
    
    full_audio = generator.normalize_audio(full_audio, target_db=-6)
    
    os.makedirs("output", exist_ok=True)
    generator.save_wav(full_audio, "output/test_asmr.wav")
    print("✓ Test audio generated!")
