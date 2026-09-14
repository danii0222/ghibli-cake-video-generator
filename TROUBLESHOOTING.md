# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### ❌ "Module not found" errors

**Solution:** Install all dependencies:
```bash
pip install -r requirements.txt
```

---

### ❌ FFmpeg not found

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from: https://ffmpeg.org/download.html
- Add to PATH environment variable

**Verify installation:**
```bash
ffmpeg -version
```

---

### ❌ "Font not found" warning

The script will automatically find system fonts. If it fails:
- Linux: Install fonts: `sudo apt-get install fonts-dejavu`
- macOS: Fonts are pre-installed
- Windows: Arial should be available by default

---

### ❌ "Out of memory" error

The 4K video generation requires significant RAM:
- Minimum: 4GB RAM
- Recommended: 8GB+ RAM

**Workaround - Reduce quality temporarily:**
Edit `config.py`:
```python
VIDEO_WIDTH = 540  # Half resolution
VIDEO_HEIGHT = 960
VIDEO_FPS = 15     # Lower FPS
```

---

### ❌ Video file is corrupted or won't play

1. Check output file size:
   ```bash
   ls -lh output/ghibli_chocolate_cake.mp4
   ```
   Should be > 100MB for 2-minute video

2. Verify with ffprobe:
   ```bash
   ffprobe output/ghibli_chocolate_cake.mp4
   ```

3. Try re-generating:
   ```bash
   rm -rf output/
   python main.py
   ```

---

### ❌ "ImageClip" or "AudioFileClip" errors

**Solution:** Update moviepy:
```bash
pip install --upgrade moviepy imageio imageio-ffmpeg
```

---

### ❌ Slow video generation

- Reduce resolution in `config.py`
- Lower FPS (e.g., 24 instead of 30)
- Close other applications
- Use SSD for faster I/O

---

### ⚠️ Script takes too long

Normal timings:
- Scene generation: 10-20 seconds
- Audio generation: 5-10 seconds
- Video composition: 2-5 minutes (depends on system specs)

Total: ~3-6 minutes for 2-minute video

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 4GB | 8GB+ |
| Storage | 5GB free | 10GB+ |
| CPU | 2 cores | 4+ cores |
| FFmpeg | Latest | Latest |

---

## Getting Help

1. Check error messages carefully
2. Verify system requirements
3. Try the troubleshooting steps above
4. Check GitHub Issues
5. Open a new issue with:
   - OS and Python version
   - Full error message
   - Steps to reproduce
