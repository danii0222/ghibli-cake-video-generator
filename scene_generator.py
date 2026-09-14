"""
Scene Generator for Ghibli-inspired Anime Video
Creates hand-drawn style frames with warm lighting and cozy aesthetic
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import os
from config import GHIBLI_COLORS, VIDEO_WIDTH, VIDEO_HEIGHT, RECIPE_STEPS

class GhibliSceneGenerator:
    def __init__(self, width=VIDEO_WIDTH, height=VIDEO_HEIGHT):
        self.width = width
        self.height = height
        self.colors = GHIBLI_COLORS
        self.font = self._load_font()
        
    def _load_font(self, font_size=60):
        """Load font with cross-platform support"""
        font_paths = [
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            # macOS
            "/System/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            # Windows
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\Arial.ttf",
        ]
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except Exception as e:
                continue
        
        # Fallback to default font
        print("⚠️  Could not load system font, using default font")
        return ImageFont.load_default()
        
    def create_base_kitchen(self):
        """Create cozy kitchen background with warm lighting"""
        img = Image.new('RGB', (self.width, self.height), self.colors["warm_bg"])
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Sunbeam effect
        for i in range(0, self.width, 20):
            x_start = i
            y_start = 0
            x_end = i + 200
            y_end = self.height
            
            # Semi-transparent sunbeam
            sunbeam_color = (*self.colors["sunbeam"], 30)
            draw.polygon([
                (x_start, y_start),
                (x_end, y_start),
                (x_end, y_end),
                (x_start, y_end)
            ], fill=sunbeam_color)
        
        # Add soft gradient shadow
        for y in range(self.height):
            alpha = int(20 * (1 - y / self.height))
            shadow_color = (*self.colors["shadow"], alpha)
            draw.line([(0, y), (self.width, y)], fill=shadow_color)
        
        return img
    
    def add_text_overlay(self, img, text, position="center", font_size=60):
        """Add text with soft shadow effect"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Load font with specific size
        font = self._load_font(font_size)
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        if position == "center":
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
        elif position == "bottom":
            x = (self.width - text_width) // 2
            y = self.height - text_height - 50
        else:
            x, y = position
        
        # Add soft shadow
        shadow_color = (100, 80, 60, 150)
        for offset_x, offset_y in [(2, 2), (3, 3)]:
            draw.text((x + offset_x, y + offset_y), text, font=font, fill=shadow_color)
        
        # Draw text
        text_color = (*self.colors["text"], 255)
        draw.text((x, y), text, font=font, fill=text_color)
        
        return img
    
    def add_bowl_and_ingredients(self, img, stage="empty"):
        """Add ceramic bowl and ingredients based on stage"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Bowl position (center-bottom area)
        bowl_x = self.width // 2 - 150
        bowl_y = self.height // 2 + 100
        
        # Draw ceramic bowl (soft hand-drawn style)
        bowl_color = (240, 235, 225, 255)
        bowl_outline = (180, 160, 140, 255)
        
        # Bowl shape
        draw.ellipse(
            [bowl_x, bowl_y, bowl_x + 300, bowl_y + 200],
            fill=bowl_color,
            outline=bowl_outline,
            width=3
        )
        
        # Bowl highlight (soft lighting)
        highlight_color = (255, 250, 240, 120)
        draw.arc(
            [bowl_x + 20, bowl_y + 20, bowl_x + 280, bowl_y + 150],
            0, 180,
            fill=highlight_color,
            width=20
        )
        
        # Add ingredients based on stage
        if stage in ["eggs", "sugar", "liquids", "mixed", "batter", "poured"]:
            # Eggs
            egg_color = (255, 240, 180, 200)
            for i in range(3):
                egg_x = bowl_x + 80 + (i * 60)
                egg_y = bowl_y + 80
                draw.ellipse(
                    [egg_x, egg_y, egg_x + 40, egg_y + 50],
                    fill=egg_color,
                    outline=(200, 180, 100, 200)
                )
        
        if stage in ["sugar", "liquids", "mixed", "batter", "poured"]:
            # Sugar mixture (darker yellow)
            mix_color = (220, 200, 150, 200)
            draw.ellipse(
                [bowl_x + 50, bowl_y + 100, bowl_x + 250, bowl_y + 160],
                fill=mix_color
            )
        
        if stage in ["liquids", "mixed", "batter", "poured"]:
            # Liquids mixed in
            liquid_color = (200, 180, 140, 180)
            draw.ellipse(
                [bowl_x + 40, bowl_y + 110, bowl_x + 260, bowl_y + 170],
                fill=liquid_color
            )
        
        if stage in ["batter", "poured"]:
            # Final batter (smooth and glossy)
            batter_color = (80, 40, 20, 200)
            draw.ellipse(
                [bowl_x + 30, bowl_y + 120, bowl_x + 270, bowl_y + 180],
                fill=batter_color
            )
        
        return img
    
    def add_oven(self, img, glowing=False):
        """Add a warm, glowing oven"""
        draw = ImageDraw.Draw(img, 'RGBA')
        
        # Oven position (right side)
        oven_x = self.width - 400
        oven_y = self.height // 2 - 150
        
        # Oven body
        oven_color = (200, 180, 160, 255)
        draw.rectangle(
            [oven_x, oven_y, oven_x + 300, oven_y + 400],
            fill=oven_color,
            outline=(100, 80, 60, 255),
            width=3
        )
        
        # Oven door
        door_color = (120, 100, 80, 255)
        draw.rectangle(
            [oven_x + 30, oven_y + 50, oven_x + 270, oven_y + 370],
            fill=door_color
        )
        
        # Window glass
        if glowing:
            glass_color = (255, 200, 100, 200)  # Warm glow
        else:
            glass_color = (60, 40, 20, 200)     # Dark
        
        draw.rectangle(
            [oven_x + 50, oven_y + 80, oven_x + 250, oven_y + 350],
            fill=glass_color
        )
        
        # Glow effect around oven when active
        if glowing:
            for i in range(5, 0, -1):
                glow_color = (255, 200, 100, 20 * i)
                draw.rectangle(
                    [oven_x - i*5, oven_y - i*5, oven_x + 300 + i*5, oven_y + 400 + i*5],
                    outline=glow_color,
                    width=i
                )
        
        # Handle
        draw.rectangle(
            [oven_x + 280, oven_y + 200, oven_x + 310, oven_y + 220],
            fill=(100, 80, 60, 255)
        )
        
        return img
    
    def create_intro_frame(self):
        """Create opening frame"""
        img = self.create_base_kitchen()
        img = self.add_text_overlay(img, "Chocolate Cake", position="center", font_size=80)
        img = self.add_text_overlay(img, "A Cozy Recipe", position=(self.width//2 - 150, self.height//2 + 150), font_size=60)
        return img
    
    def create_cooking_frame(self, step_index, progress=0):
        """Create frame for a cooking step
        
        progress: 0-1 indicating progress through the step
        """
        img = self.create_base_kitchen()
        
        if step_index < 2:  # Egg and sugar stage
            stage = "eggs" if step_index == 0 else "sugar"
            img = self.add_bowl_and_ingredients(img, stage)
            text = RECIPE_STEPS[step_index]
        
        elif step_index == 2:  # Pouring liquids
            img = self.add_bowl_and_ingredients(img, "liquids")
            text = RECIPE_STEPS[step_index]
        
        elif step_index in [3, 4]:  # Sifting and whisking
            img = self.add_bowl_and_ingredients(img, "mixed" if step_index == 3 else "batter")
            text = RECIPE_STEPS[step_index]
        
        elif step_index == 5:  # Pouring into mold
            img = self.add_bowl_and_ingredients(img, "poured")
            text = RECIPE_STEPS[step_index]
        
        elif step_index == 6:  # Into oven
            img = self.add_oven(img, glowing=True)
            text = RECIPE_STEPS[step_index]
        
        # Add step text
        img = self.add_text_overlay(img, text, position="bottom", font_size=45)
        
        return img
    
    def create_outro_frame(self):
        """Create closing frame with finished cake"""
        img = self.create_base_kitchen()
        img = self.add_oven(img, glowing=True)
        img = self.add_text_overlay(img, "Ready to Enjoy!", position="center", font_size=80)
        img = self.add_text_overlay(img, "Itadakimasu 🍰", position=(self.width//2 - 150, self.height//2 + 150), font_size=60)
        return img
    
    def save_frame(self, img, filename):
        """Save frame to file"""
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
        img.save(filename, quality=95)
        return filename


if __name__ == "__main__":
    generator = GhibliSceneGenerator()
    
    # Generate sample frames
    frames_dir = "output/frames"
    
    # Intro
    intro = generator.create_intro_frame()
    generator.save_frame(intro, f"{frames_dir}/intro.png")
    
    # Cooking steps
    for i in range(len(RECIPE_STEPS)):
        frame = generator.create_cooking_frame(i)
        generator.save_frame(frame, f"{frames_dir}/step_{i:02d}.png")
    
    # Outro
    outro = generator.create_outro_frame()
    generator.save_frame(outro, f"{frames_dir}/outro.png")
    
    print("✓ Sample frames generated!")
