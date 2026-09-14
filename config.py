"""
Configuration file for Ghibli Cake Video Generator
Define colors, dimensions, timings, and recipe steps
"""

# Video dimensions (9:16 vertical for mobile)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30

# Ghibli-inspired color palette
GHIBLI_COLORS = {
    "warm_bg": (245, 240, 235),        # Warm cream background
    "sunbeam": (255, 250, 200),        # Golden sunlight
    "shadow": (120, 100, 80),          # Warm shadow
    "text": (80, 60, 40),              # Dark brown text
    "accent": (220, 100, 60),          # Warm orange accent
}

# Scene durations (seconds)
SCENES = {
    "intro": 4,
    "crack_eggs": 2,
    "add_sugar": 2,
    "pour_liquids": 2.5,
    "sift_dry": 2,
    "whisk_batter": 3,
    "pour_batter": 2.5,
    "oven": 8,
    "outro": 4,
}

# Recipe steps text
RECIPE_STEPS = [
    "Step 1: Crack the eggs",
    "Step 2: Add sugar, mix well",
    "Step 3: Pour milk and vanilla",
    "Step 4: Sift flour and cocoa",
    "Step 5: Whisk until smooth",
    "Step 6: Pour into mold",
    "Step 7: Bake at 350°F",
]

# ASMR sound configuration
ASMR_CONFIG = {
    "sample_rate": 44100,
    "duration": 120,  # 2 minutes total
    "egg_crack_volume": 0.7,
    "whisking_volume": 0.6,
    "pouring_volume": 0.5,
    "sifting_volume": 0.6,
}

# Timeline for sound effects (time_in_seconds: sound_type)
SOUND_TIMELINE = {
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
