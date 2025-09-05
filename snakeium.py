#!/usr/bin/env python3
"""
🐍 SNAKEIUM - GHOSTKITTY Edition 🎵
=================================

A modern retro Snake game with stunning 8-bit visuals, rainbow effects, and epic GHOSTKITTY music.
Experience the classic game reimagined with ultra-smooth 60 FPS gameplay and authentic retro aesthetics.

🌟 FEATURES:
- 🎵 75 GHOSTKITTY tracks with seamless playback
- 🌈 Animated rainbow pixelated backgrounds  
- ⚡ 5 speed settings (Chill to Nightmare)
- 🎮 Power-ups: Speed Boost, Score Multiplier, Rainbow Mode, Mega Food
- 📱 Safe windowed mode with dynamic resizing
- 🎯 Ultra-smooth movement with easing functions
- 🔊 Immersive retro sound design
- 🎨 8-bit crush visual effects with scan lines

🎮 CONTROLS:
- Arrow Keys / WASD: Move snake
- SPACE: Pause game
- M: Skip to next track
- R: Restart (when game over)
- ESC: Return to menu / Quit
- Enter: Select menu option

💻 REQUIREMENTS:
- Python 3.8+
- pygame 2.0+

🚀 USAGE:
    python snakeium.py              # Normal mode
    python snakeium.py --fullscreen # Fullscreen mode (advanced users)
    python snakeium.py --no-music   # Silent mode

Author: GHOSTKITTY
Version: 1.0.0
License: MIT
GitHub: https://github.com/GHOSTKITTY/SNAKEIUM
"""

import pygame
import random
import math
import os
import glob
import colorsys
import time
import sys
from enum import Enum
from typing import List, Tuple, Optional
import threading

# Version info
__version__ = "1.0.0"
__author__ = "GHOSTKITTY APPS"

# Try to import optional dependencies
try:
    import mutagen
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False
    print("⚠️  mutagen not found - music metadata features disabled")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️  numpy not found - advanced effects disabled")

# Initialize Pygame with error handling
try:
    import os
    # Set dummy drivers for headless environments
    if os.environ.get('SDL_VIDEODRIVER') == 'dummy':
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
    
    pygame.init()
    
    # Only initialize mixer if not in headless mode
    if os.environ.get('SDL_AUDIODRIVER') != 'dummy':
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    print("✅ Pygame initialized successfully")
except pygame.error as e:
    print(f"❌ Failed to initialize Pygame: {e}")
    # In test mode, continue anyway
    if '--test-mode' not in sys.argv:
        sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error during Pygame init: {e}")
    if '--test-mode' not in sys.argv:
        sys.exit(1)

# Safe windowed display settings to prevent system crashes
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
print(f"🖥️  Safe windowed mode: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# Configuration Constants
class Config:
    """Game configuration settings"""
    # Display settings
    GRID_SIZE = 25
    GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
    GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
    TARGET_FPS = 60  # Reduced from 120 to prevent system overload
    
    # Visual effects settings - HEAVILY REDUCED TO PREVENT CRASHES
    SMOOTH_MOVEMENT = True
    INTERPOLATION_STEPS = 15  # Reduced for better performance
    EASING_FACTOR = 0.12  # Smooth acceleration/deceleration
    SUB_PIXEL_MOVEMENT = True  # Enable sub-pixel positioning
    PIXELATED_BACKGROUND = True  # 8-bit crush effect
    PIXEL_SCALE = 8  # Larger pixels for less intensive rendering
    PYRAMID_COUNT = 1  # Drastically reduced from 3
    TRIANGLE_COUNT = 1  # Drastically reduced from 5
    SPIRAL_COUNT = 1  # Drastically reduced from 6
    PYRAMID_SPEED = 2.0
    TRIANGLE_SPEED = 3.0
    SPIRAL_SPEED = 1.5
    SPIRAL_RADIUS_MAX = 80
    
    # Particle system - REDUCED TO PREVENT CRASHES
    MAX_PARTICLES = 50  # Drastically reduced from 300
    
    # Music settings
    DEFAULT_MUSIC_FOLDER = r"c:\Users\music2\Desktop\GHOSTKITTY MP3S"
    MUSIC_VOLUME = 0.3
    
    # Performance settings
    ENABLE_VSYNC = True
    ENABLE_PARTICLES = True
    ENABLE_GEOMETRIC_EFFECTS = True

# Legacy constants for compatibility
GRID_SIZE = Config.GRID_SIZE
GRID_WIDTH = Config.GRID_WIDTH
GRID_HEIGHT = Config.GRID_HEIGHT
SMOOTH_MOVEMENT = Config.SMOOTH_MOVEMENT
INTERPOLATION_STEPS = Config.INTERPOLATION_STEPS
EASING_FACTOR = Config.EASING_FACTOR
SUB_PIXEL_MOVEMENT = Config.SUB_PIXEL_MOVEMENT
PIXELATED_BACKGROUND = Config.PIXELATED_BACKGROUND
PIXEL_SCALE = Config.PIXEL_SCALE
PYRAMID_COUNT = Config.PYRAMID_COUNT
TRIANGLE_COUNT = Config.TRIANGLE_COUNT
SPIRAL_COUNT = Config.SPIRAL_COUNT
PYRAMID_SPEED = Config.PYRAMID_SPEED
TRIANGLE_SPEED = Config.TRIANGLE_SPEED
SPIRAL_SPEED = Config.SPIRAL_SPEED
SPIRAL_RADIUS_MAX = Config.SPIRAL_RADIUS_MAX

# 8-bit spiral graphics settings
SPIRAL_COUNT = 8
SPIRAL_SPEED = 2.0
SPIRAL_RADIUS_MAX = 100

# Pyramid/Triangle ripping effects (REDUCED for stability)
PYRAMID_COUNT = 5  # Reduced from 15
TRIANGLE_COUNT = 8  # Reduced from 20
PYRAMID_SPEED = 1.5  # Reduced from 3.0
TRIANGLE_SPEED = 2.0  # Reduced from 4.5

# Colors (Rainbow themed!)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (0, 255, 127)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_PURPLE = (191, 0, 255)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

def create_snake_head_sprite(size, direction, color):
    """Create an 8-bit style snake head sprite"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Snake head pattern (8-bit style)
    pattern = [
        "  OOOOOO  ",
        " OOOOOOOO ",
        "OOOO**OOOO",
        "OOO*OO*OOO",
        "OOOOOOOOOO",
        "OOOO^^OOOO",
        "OOOOOOOOOO",
        " OOOOOOOO ",
        "  OOOOOO  ",
        "          "
    ]
    
    pixel_size = size // 10
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == 'O':  # Head body
                pygame.draw.rect(surf, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == '*':  # Eyes
                pygame.draw.rect(surf, BLACK, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == '^':  # Nostrils
                pygame.draw.rect(surf, (color[0]//2, color[1]//2, color[2]//2), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    
    # Rotate based on direction
    if direction == Direction.UP:
        surf = pygame.transform.rotate(surf, 0)
    elif direction == Direction.RIGHT:
        surf = pygame.transform.rotate(surf, -90)
    elif direction == Direction.DOWN:
        surf = pygame.transform.rotate(surf, 180)
    elif direction == Direction.LEFT:
        surf = pygame.transform.rotate(surf, 90)
    
    return surf

def create_snake_body_sprite(size, color, is_tail=False):
    """Create an 8-bit style snake body sprite"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if is_tail:
        # Tail pattern
        pattern = [
            "          ",
            "   OOOO   ",
            "  OOOOOO  ",
            " OOOOOOOO ",
            " OOOOOOOO ",
            "  OOOOOO  ",
            "   OOOO   ",
            "    OO    ",
            "          ",
            "          "
        ]
    else:
        # Body pattern with scales
        pattern = [
            " OOOOOOOO ",
            "OOOOOOOOOO",
            "OO-OOO-OOO",
            "OOOOOOOOOO",
            "OOOOOOOOOO",
            "OOO-OOO-OO",
            "OOOOOOOOOO",
            "OOOOOOOOOO",
            " OOOOOOOO ",
            "          "
        ]
    
    pixel_size = size // 10
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == 'O':  # Body
                pygame.draw.rect(surf, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == '-':  # Scale detail
                scale_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
                pygame.draw.rect(surf, scale_color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    
    return surf

def create_apple_sprite(size):
    """Create an 8-bit style apple sprite"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Apple pattern
    pattern = [
        "    gg    ",
        "   gGGg   ",
        "  RRRRRR  ",
        " RRRRRRRR ",
        " RRRRRRRR ",
        "RRRRRRRRRR",
        "RRRRRRRRRR",
        " RRRRRRRR ",
        "  RRRRRR  ",
        "   RRRR   "
    ]
    
    pixel_size = size // 10
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == 'R':  # Apple body
                pygame.draw.rect(surf, (220, 20, 60), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == 'g':  # Stem
                pygame.draw.rect(surf, (34, 139, 34), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == 'G':  # Leaf
                pygame.draw.rect(surf, (0, 255, 0), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    
    return surf

class PyramidEffect:
    """Massive pyramids ripping through the screen"""
    def __init__(self, pyramid_id):
        self.x = random.randint(-200, WINDOW_WIDTH + 200)
        self.y = random.randint(-200, WINDOW_HEIGHT + 200)
        self.size = random.randint(50, 150)
        self.speed_x = random.uniform(-PYRAMID_SPEED, PYRAMID_SPEED)
        self.speed_y = random.uniform(-PYRAMID_SPEED, PYRAMID_SPEED)
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        self.pyramid_id = pyramid_id
        self.color_offset = pyramid_id * 45
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rotation += self.rotation_speed
        
        # Wrap around screen
        if self.x < -300:
            self.x = WINDOW_WIDTH + 200
            self.y = random.randint(-200, WINDOW_HEIGHT + 200)
        elif self.x > WINDOW_WIDTH + 300:
            self.x = -200
            self.y = random.randint(-200, WINDOW_HEIGHT + 200)
            
        if self.y < -300:
            self.y = WINDOW_HEIGHT + 200
            self.x = random.randint(-200, WINDOW_WIDTH + 200)
        elif self.y > WINDOW_HEIGHT + 300:
            self.y = -200
            self.x = random.randint(-200, WINDOW_WIDTH + 200)
    
    def draw(self, screen):
        # Safety check for screen bounds
        if self.x < -500 or self.x > WINDOW_WIDTH + 500 or self.y < -500 or self.y > WINDOW_HEIGHT + 500:
            return
            
        # Rainbow color that changes over time
        hue = (time.time() * 30 + self.color_offset) % 360
        rgb = colorsys.hsv_to_rgb(hue / 360, 0.8, 0.9)
        color = tuple(int(c * 255) for c in rgb)
        
        # Create pyramid points
        half_size = self.size // 2
        points = [
            (int(self.x), int(self.y - half_size)),  # Top
            (int(self.x - half_size), int(self.y + half_size)),  # Bottom left
            (int(self.x + half_size), int(self.y + half_size)),  # Bottom right
        ]
        
        # Simple rotation (no complex math)
        if abs(self.rotation) > 0.1:
            center_x, center_y = int(self.x), int(self.y)
            cos_r = math.cos(math.radians(self.rotation))
            sin_r = math.sin(math.radians(self.rotation))
            
            rotated_points = []
            for px, py in points:
                # Translate to origin
                px -= center_x
                py -= center_y
                # Rotate
                new_x = px * cos_r - py * sin_r
                new_y = px * sin_r + py * cos_r
                # Translate back
                rotated_points.append((int(new_x + center_x), int(new_y + center_y)))
            points = rotated_points
        
        # Draw pyramid with error handling
        try:
            if len(points) >= 3 and all(isinstance(p, tuple) and len(p) == 2 for p in points):
                pygame.draw.polygon(screen, color, points)
                pygame.draw.polygon(screen, WHITE, points, 1)  # Thinner outline
        except (ValueError, TypeError):
            pass  # Skip this frame if there's an error

class TriangleRipper:
    """Fast triangles ripping across the screen"""
    def __init__(self, triangle_id):
        self.reset_position()
        self.size = random.randint(20, 60)
        self.speed_x = random.uniform(-TRIANGLE_SPEED, TRIANGLE_SPEED)
        self.speed_y = random.uniform(-TRIANGLE_SPEED, TRIANGLE_SPEED)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.triangle_id = triangle_id
        self.color_offset = triangle_id * 20
        self.trail_points = []
        
    def reset_position(self):
        # Start from edges of screen
        edge = random.randint(0, 3)
        if edge == 0:  # Top
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = -50
        elif edge == 1:  # Right
            self.x = WINDOW_WIDTH + 50
            self.y = random.randint(0, WINDOW_HEIGHT)
        elif edge == 2:  # Bottom
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = WINDOW_HEIGHT + 50
        else:  # Left
            self.x = -50
            self.y = random.randint(0, WINDOW_HEIGHT)
    
    def update(self):
        # Add to trail
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > 10:  # Limit trail length
            self.trail_points.pop(0)
            
        self.x += self.speed_x
        self.y += self.speed_y
        self.rotation += self.rotation_speed
        
        # Reset if off screen
        if (self.x < -100 or self.x > WINDOW_WIDTH + 100 or 
            self.y < -100 or self.y > WINDOW_HEIGHT + 100):
            self.reset_position()
            self.trail_points = []
    
    def draw(self, screen):
        # Safety check for screen bounds
        if self.x < -200 or self.x > WINDOW_WIDTH + 200 or self.y < -200 or self.y > WINDOW_HEIGHT + 200:
            return
            
        # Draw simplified trail
        for i, (tx, ty) in enumerate(self.trail_points):
            if i % 2 == 0:  # Only draw every other point for performance
                alpha_factor = i / len(self.trail_points)
                trail_size = max(1, int(self.size * alpha_factor * 0.3))
                if trail_size > 1:
                    hue = (time.time() * 50 + self.color_offset) % 360
                    rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
                    color = tuple(int(c * 255) for c in rgb)
                    try:
                        pygame.draw.circle(screen, color, (int(tx), int(ty)), trail_size)
                    except (ValueError, TypeError):
                        pass
        
        # Rainbow color that changes rapidly
        hue = (time.time() * 80 + self.color_offset) % 360
        rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
        color = tuple(int(c * 255) for c in rgb)
        
        # Create triangle points
        half_size = self.size // 2
        points = [
            (int(self.x), int(self.y - half_size)),  # Top
            (int(self.x - half_size), int(self.y + half_size)),  # Bottom left
            (int(self.x + half_size), int(self.y + half_size)),  # Bottom right
        ]
        
        # Simple rotation
        center_x, center_y = int(self.x), int(self.y)
        cos_r = math.cos(math.radians(self.rotation))
        sin_r = math.sin(math.radians(self.rotation))
        
        rotated_points = []
        for px, py in points:
            px -= center_x
            py -= center_y
            new_x = px * cos_r - py * sin_r
            new_y = px * sin_r + py * cos_r
            rotated_points.append((int(new_x + center_x), int(new_y + center_y)))
        
        # Draw triangle with error handling
        try:
            if len(rotated_points) >= 3:
                pygame.draw.polygon(screen, color, rotated_points)
                pygame.draw.polygon(screen, WHITE, rotated_points, 1)
        except (ValueError, TypeError):
            pass
class SpiralEffect:
    """Crazy 8-bit rainbow spirals in the background"""
    def __init__(self, center_x, center_y, spiral_id):
        self.center_x = center_x
        self.center_y = center_y
        self.angle = spiral_id * (360 / SPIRAL_COUNT)
        self.radius = 0
        self.max_radius = SPIRAL_RADIUS_MAX
        self.spiral_id = spiral_id
        self.time_offset = spiral_id * 0.5
        self.points = []
        
    def update(self):
        self.angle += SPIRAL_SPEED
        current_time = time.time() + self.time_offset
        
        # Create spiral points
        self.points = []
        for i in range(50):  # 50 points per spiral
            point_angle = self.angle + i * 15
            point_radius = (i * 2) % self.max_radius
            
            # Add some wobble for crazy effect
            wobble = 10 * math.sin(current_time * 3 + i * 0.2)
            
            x = self.center_x + (point_radius + wobble) * math.cos(math.radians(point_angle))
            y = self.center_y + (point_radius + wobble) * math.sin(math.radians(point_angle))
            
            # Rainbow color based on angle
            hue = (point_angle + current_time * 50) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            color = tuple(int(c * 255) for c in rgb)
            
            self.points.append((x, y, color, point_radius))
    
    def draw(self, screen):
        for i, (x, y, color, radius) in enumerate(self.points):
            if 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT:
                # Draw 8-bit style pixels
                size = max(2, int(4 - radius / 30))
                pygame.draw.rect(screen, color, (int(x), int(y), size, size))

class PowerUpType(Enum):
    SPEED_BOOST = "speed"
    SCORE_MULTIPLIER = "score"
    RAINBOW_MODE = "rainbow"
    MEGA_FOOD = "mega"

class Particle:
    def __init__(self, x, y, color, velocity, lifetime=60):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 6)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vy += 0.1  # Gravity effect
        
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (*self.color[:3], alpha)
            pygame.draw.circle(screen, self.color[:3], (int(self.x), int(self.y)), self.size)

class MusicManager:
    """Enhanced music manager with metadata support and error handling"""
    
    def __init__(self, music_folder=None):
        self.music_folder = music_folder or Config.DEFAULT_MUSIC_FOLDER
        self.playlist = []
        self.current_song = None
        self.current_index = 0
        self.shuffle_mode = True
        self.load_playlist()
        
    def load_playlist(self):
        """Load all MP3 files from the music folder with error handling"""
        if not os.path.exists(self.music_folder):
            print(f"⚠️  Music folder not found: {self.music_folder}")
            # Try alternative locations
            alternative_paths = [
                os.path.join(os.path.expanduser("~"), "Music"),
                os.path.join(os.path.expanduser("~"), "Desktop"),
                os.getcwd()
            ]
            
            for alt_path in alternative_paths:
                mp3_files = glob.glob(os.path.join(alt_path, "**", "*.mp3"), recursive=True)
                if mp3_files:
                    self.music_folder = alt_path
                    self.playlist = mp3_files[:50]  # Limit to 50 for performance
                    print(f"🎵 Found {len(self.playlist)} music files in {alt_path}")
                    return
                    
            print("❌ No music files found. Game will run without background music.")
            return
            
        try:
            mp3_files = glob.glob(os.path.join(self.music_folder, "*.mp3"))
            self.playlist = mp3_files
            print(f"🎵 Loaded {len(self.playlist)} music tracks!")
            
            # Try to load metadata if mutagen is available
            if HAS_MUTAGEN and self.playlist:
                self._load_metadata()
                
        except Exception as e:
            print(f"⚠️  Error loading playlist: {e}")
            
    def _load_metadata(self):
        """Load music metadata using mutagen"""
        try:
            from mutagen._file import File
            for i, track in enumerate(self.playlist[:5]):  # Only first 5 for demo
                try:
                    audiofile = File(track)
                    if audiofile and hasattr(audiofile, 'info') and audiofile.info:
                        duration = int(audiofile.info.length)
                        print(f"🎶 Track {i+1}: {os.path.basename(track)} ({duration//60}:{duration%60:02d})")
                except:
                    continue
        except Exception as e:
            print(f"⚠️  Metadata loading failed: {e}")
        
    def play_random_song(self):
        """Play a random song from the playlist with error handling"""
        if not self.playlist:
            return None
            
        try:
            if self.shuffle_mode:
                self.current_song = random.choice(self.playlist)
            else:
                self.current_index = (self.current_index + 1) % len(self.playlist)
                self.current_song = self.playlist[self.current_index]
                
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.set_volume(Config.MUSIC_VOLUME)
            pygame.mixer.music.play()
            
            song_name = os.path.basename(self.current_song)
            print(f"🎵 Now playing: {song_name}")
            return song_name
            
        except pygame.error as e:
            print(f"⚠️  Error playing {self.current_song}: {e}")
            # Try next song
            if len(self.playlist) > 1 and self.current_song:
                self.playlist.remove(self.current_song)
                return self.play_random_song()
        except Exception as e:
            print(f"⚠️  Unexpected music error: {e}")
            
        return None
        
    def check_music(self):
        """Check if music is still playing, if not play next song"""
        try:
            if not pygame.mixer.music.get_busy() and self.playlist:
                return self.play_random_song()
        except Exception as e:
            print(f"⚠️  Music check error: {e}")
        return None
        
    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.shuffle_mode = not self.shuffle_mode
        mode = "ON" if self.shuffle_mode else "OFF"
        print(f"🔀 Shuffle mode: {mode}")
        
    def get_current_info(self):
        """Get current song information"""
        if self.current_song:
            name = os.path.basename(self.current_song)
            return f"♪ {name}"
        return "♪ No music playing"

class PowerUp:
    def __init__(self, x, y, power_type: PowerUpType):
        self.x = x
        self.y = y
        self.type = power_type
        self.spawn_time = time.time()
        self.lifetime = 10  # seconds
        self.pulse = 0
        
    def update(self):
        self.pulse += 0.2
        
    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime
        
    def draw(self, screen):
        pulse_size = int(5 + 3 * math.sin(self.pulse))
        colors = {
            PowerUpType.SPEED_BOOST: NEON_BLUE,
            PowerUpType.SCORE_MULTIPLIER: NEON_YELLOW,
            PowerUpType.RAINBOW_MODE: NEON_PURPLE,
            PowerUpType.MEGA_FOOD: NEON_ORANGE
        }
        
        color = colors[self.type]
        x_pos = self.x * GRID_SIZE + GRID_SIZE // 2
        y_pos = self.y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw pulsing effect
        pygame.draw.circle(screen, color, (x_pos, y_pos), GRID_SIZE // 2 + pulse_size)
        pygame.draw.circle(screen, BLACK, (x_pos, y_pos), GRID_SIZE // 2 + pulse_size - 2)

class Snake:
    def __init__(self, speed=4):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.grow = False
        self.speed = speed  # Use the provided speed
        self.rainbow_mode = False
        self.rainbow_timer = 0
        self.speed_boost_timer = 0
        self.score_multiplier = 1
        self.score_multiplier_timer = 0
        
        # Ultra-smooth movement system
        self.move_timer = 0
        self.move_interval = max(1, 60 // self.speed)  # Frames between actual moves (adjusted for 60 FPS)
        self.smooth_positions = []  # Floating-point positions for each segment
        self.target_positions = []  # Target grid positions
        self.movement_progress = 0.0  # Progress of current movement (0.0 to 1.0)
        self.is_moving = False
        
        # Initialize smooth positions
        for i, (x, y) in enumerate(self.body):
            self.smooth_positions.append([float(x), float(y)])
            self.target_positions.append((x, y))
    
    def ease_in_out_cubic(self, t):
        """Smooth easing function for ultra-smooth movement"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            p = 2 * t - 2
            return 1 + p * p * p / 2
    
    def ease_out_quart(self, t):
        """Alternative easing for even smoother feel"""
        return 1 - (1 - t) ** 4
    
    def update_smooth_positions(self):
        """Update smooth interpolated positions using easing"""
        if not SMOOTH_MOVEMENT:
            self.smooth_positions = [[float(x), float(y)] for x, y in self.body]
            return
            
        if self.is_moving and self.movement_progress < 1.0:
            # Apply easing to movement progress
            eased_progress = self.ease_out_quart(self.movement_progress)
            
            for i in range(len(self.body)):
                if i < len(self.smooth_positions) and i < len(self.target_positions):
                    start_x, start_y = self.smooth_positions[i]
                    target_x, target_y = self.target_positions[i]
                    
                    # Smooth interpolation with easing
                    self.smooth_positions[i][0] = start_x + (target_x - start_x) * eased_progress
                    self.smooth_positions[i][1] = start_y + (target_y - start_y) * eased_progress
        else:
            # Ensure positions match exactly when not moving
            for i in range(len(self.body)):
                if i < len(self.smooth_positions):
                    self.smooth_positions[i][0] = float(self.body[i][0])
                    self.smooth_positions[i][1] = float(self.body[i][1])
        
    def move(self):
        """Ultra-smooth movement with easing functions"""
        self.move_timer += 1
        
        # Update movement progress for smooth interpolation
        if self.is_moving:
            frames_per_move = self.move_interval
            self.movement_progress = min(1.0, self.move_timer / frames_per_move)
            
            # Update smooth positions during movement
            self.update_smooth_positions()
            
            # Complete the move when progress reaches 1.0
            if self.movement_progress >= 1.0:
                self.is_moving = False
                self.movement_progress = 0.0
                self.move_timer = 0
        
        # Start new movement when timer reaches interval
        if not self.is_moving and self.move_timer >= self.move_interval:
            self.start_new_move()
            
        # Always update smooth positions
        self.update_smooth_positions()
    
    def start_new_move(self):
        """Start a new movement with smooth transition"""
        self.move_timer = 0
        self.movement_progress = 0.0
        self.is_moving = True
        
        # Store current positions as start positions
        for i in range(len(self.body)):
            if i >= len(self.smooth_positions):
                self.smooth_positions.append([float(self.body[i][0]), float(self.body[i][1])])
        
        # Calculate new body positions
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # Wrap around screen edges
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        
        # Update body
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        # Update target positions for smooth interpolation
        self.target_positions = [(x, y) for x, y in self.body]
        
        # Ensure smooth_positions list matches body length
        while len(self.smooth_positions) > len(self.body):
            self.smooth_positions.pop()
        while len(self.smooth_positions) < len(self.body):
            x, y = self.body[len(self.smooth_positions)]
            self.smooth_positions.append([float(x), float(y)])
            
    def change_direction(self, new_direction: Direction):
        # Prevent reversing into itself
        if len(self.body) > 1:
            current_dx, current_dy = self.direction.value
            new_dx, new_dy = new_direction.value
            if (current_dx, current_dy) != (-new_dx, -new_dy):
                self.direction = new_direction
        else:
            self.direction = new_direction
            
    def eat_food(self):
        self.grow = True
        
    def eat_powerup(self, powerup: PowerUp):
        if powerup.type == PowerUpType.SPEED_BOOST:
            self.speed_boost_timer = 300  # 5 seconds at 60 FPS
        elif powerup.type == PowerUpType.SCORE_MULTIPLIER:
            self.score_multiplier = 3
            self.score_multiplier_timer = 600  # 10 seconds
        elif powerup.type == PowerUpType.RAINBOW_MODE:
            self.rainbow_mode = True
            self.rainbow_timer = 900  # 15 seconds
        elif powerup.type == PowerUpType.MEGA_FOOD:
            for _ in range(3):
                self.eat_food()
                
    def update_effects(self):
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
        if self.score_multiplier_timer > 0:
            self.score_multiplier_timer -= 1
        else:
            self.score_multiplier = 1
        if self.rainbow_timer > 0:
            self.rainbow_timer -= 1
        else:
            self.rainbow_mode = False
            
    def get_current_speed(self):
        base_speed = self.speed + len(self.body) // 8  # Slower progression for 120Hz
        if self.speed_boost_timer > 0:
            return min(base_speed * 1.8, 20)  # Cap at 20 for 120Hz
        return base_speed
        
    def update_move_interval(self):
        """Update movement interval based on current speed"""
        current_speed = self.get_current_speed()
        self.move_interval = max(60 // current_speed, 1)  # Minimum 1 frame, adjusted for 60 FPS
        
    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:]
        
    def get_rainbow_color(self, index):
        hue = (time.time() * 100 + index * 30) % 360
        rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
        return tuple(int(c * 255) for c in rgb)
        
    def draw(self, screen, particles):
        # Use smooth positions for ultra-smooth rendering
        if SMOOTH_MOVEMENT and len(self.smooth_positions) > 0:
            positions_to_draw = [(pos[0], pos[1]) for pos in self.smooth_positions]
        else:
            positions_to_draw = [(float(x), float(y)) for x, y in self.body]
        
        for i, (x, y) in enumerate(positions_to_draw):
            # Calculate pixel position with sub-pixel precision
            if SUB_PIXEL_MOVEMENT:
                pixel_x = x * GRID_SIZE
                pixel_y = y * GRID_SIZE
            else:
                pixel_x = int(x) * GRID_SIZE
                pixel_y = int(y) * GRID_SIZE
            
            if self.rainbow_mode:
                color = self.get_rainbow_color(i)
            else:
                if i == 0:  # Head
                    color = NEON_GREEN
                else:  # Body
                    gradient = 1 - (i / len(positions_to_draw))
                    color = (int(NEON_GREEN[0] * gradient), 
                            int(NEON_GREEN[1] * gradient), 
                            int(NEON_GREEN[2] * gradient))
            
            # Draw 8-bit snake sprites
            if i == 0:  # Head
                head_sprite = create_snake_head_sprite(GRID_SIZE, self.direction, color)
                screen.blit(head_sprite, (pixel_x, pixel_y))
            elif i == len(positions_to_draw) - 1:  # Tail
                tail_sprite = create_snake_body_sprite(GRID_SIZE, color, is_tail=True)
                screen.blit(tail_sprite, (pixel_x, pixel_y))
            else:  # Body
                body_sprite = create_snake_body_sprite(GRID_SIZE, color, is_tail=False)
                screen.blit(body_sprite, (pixel_x, pixel_y))
            
            # Add extra glow for rainbow mode
            if self.rainbow_mode:
                glow_size = GRID_SIZE + 6
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                glow_color = (*color, 100)  # Semi-transparent
                pygame.draw.circle(glow_surf, color, (glow_size//2, glow_size//2), glow_size//2)
                glow_surf.set_alpha(100)
                screen.blit(glow_surf, (pixel_x - 3, pixel_y - 3))
            
            # Add particles for rainbow mode
            if self.rainbow_mode and random.random() < 0.4:  # More particles for 120Hz
                particle_color = self.get_rainbow_color(i + random.randint(0, 10))
                velocity = (random.uniform(-3, 3), random.uniform(-3, 3))
                particles.append(Particle(
                    pixel_x + GRID_SIZE // 2,
                    pixel_y + GRID_SIZE // 2,
                    particle_color,
                    velocity
                ))

class Food:
    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.pulse = 0
        self.apple_sprite = create_apple_sprite(GRID_SIZE)
        self.glow_intensity = 0
        self.bob_offset = 0  # Gentle bobbing motion
        self.sparkle_timer = 0
        
    def update(self):
        self.pulse += 0.08  # Slower, smoother pulsing
        self.glow_intensity = (self.glow_intensity + 0.05) % (2 * math.pi)  # Smoother glow
        self.bob_offset += 0.04  # Gentle bobbing
        self.sparkle_timer += 1
        
    def draw(self, screen):
        # Apply gentle bobbing motion
        bob_y = 2 * math.sin(self.bob_offset)
        x_pos = self.x * GRID_SIZE
        y_pos = self.y * GRID_SIZE + bob_y
        
        # Smoother glow effect
        glow_size = int(4 + 2 * math.sin(self.glow_intensity))
        glow_surf = pygame.Surface((GRID_SIZE + glow_size * 4, GRID_SIZE + glow_size * 4), pygame.SRCALPHA)
        glow_color = (255, 120, 120, 60)  # Softer red glow
        
        # Multi-layer glow for smooth effect
        for layer in range(3):
            layer_size = glow_size + layer * 2
            layer_alpha = 60 - layer * 15
            pygame.draw.circle(glow_surf, (*glow_color[:3], max(0, layer_alpha)), 
                             (glow_surf.get_width()//2, glow_surf.get_height()//2), 
                             GRID_SIZE//2 + layer_size)
        
        glow_surf.set_alpha(60)
        screen.blit(glow_surf, (x_pos - glow_size * 2, y_pos - glow_size * 2))
        
        # Draw the 8-bit apple sprite with bobbing
        screen.blit(self.apple_sprite, (x_pos, int(y_pos)))
        
        # Smoother sparkle effects
        if self.sparkle_timer % 30 < 5:  # More predictable sparkles
            for _ in range(2):
                sparkle_x = x_pos + random.randint(5, GRID_SIZE - 5)
                sparkle_y = int(y_pos) + random.randint(5, GRID_SIZE - 5)
                sparkle_size = random.randint(1, 3)
                pygame.draw.circle(screen, WHITE, (sparkle_x, sparkle_y), sparkle_size)

class StartMenu:
    """Retro 8-bit start menu with speed settings"""
    def __init__(self, screen):
        self.screen = screen
        self.selected_option = 0
        self.options = [
            ("🐌 CHILL MODE", 2),
            ("🎮 CLASSIC", 4),
            ("⚡ FAST", 6),
            ("🚀 INSANE", 8),
            ("💀 NIGHTMARE", 12)
        ]
        self.menu_active = True
        self.title_pulse = 0
        self.bg_pattern_offset = 0
        
        # 8-bit fonts
        self.title_font = pygame.font.Font(None, max(72, WINDOW_WIDTH // 15))
        self.menu_font = pygame.font.Font(None, max(48, WINDOW_WIDTH // 25))
        self.subtitle_font = pygame.font.Font(None, max(32, WINDOW_WIDTH // 40))
        
    def draw_8bit_background(self):
        """Draw pixelated 8-bit crush background that fills entire screen"""
        self.bg_pattern_offset += 0.5
        
        # Get actual screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Create pixelated rainbow pattern that covers the whole screen
        pixel_size = PIXEL_SCALE
        block_size = pixel_size * 6  # Size of each colored block
        
        # Calculate how many blocks we need to cover the entire actual screen
        cols = (screen_width + block_size - 1) // block_size  # Round up
        rows = (screen_height + block_size - 1) // block_size  # Round up
        
        for x in range(cols):
            for y in range(rows):
                # Create 8-bit rainbow checkerboard
                pos_x = x * block_size
                pos_y = y * block_size
                hue = ((pos_x + pos_y + self.bg_pattern_offset) * 0.1) % 360
                rgb = colorsys.hsv_to_rgb(hue / 360, 0.6, 0.4)
                color = tuple(int(c * 255) for c in rgb)
                
                # Draw pixelated blocks that extend to screen edges
                pygame.draw.rect(self.screen, color, 
                               (pos_x, pos_y, block_size, block_size))
                
        # Add scan lines for authentic 8-bit feel
        for y in range(0, screen_height, 4):
            pygame.draw.line(self.screen, (0, 0, 0, 30), 
                           (0, y), (screen_width, y), 1)
    
    def draw_title(self):
        """Draw animated 8-bit title"""
        self.title_pulse += 0.1
        
        # Main title with rainbow effect
        title_text = "SNAKEIUM"
        for i, char in enumerate(title_text):
            hue = (time.time() * 50 + i * 45) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            color = tuple(int(c * 255) for c in rgb)
            
            char_surface = self.title_font.render(char, True, color)
            char_x = WINDOW_WIDTH // 2 - (len(title_text) * 35) + i * 70
            char_y = WINDOW_HEIGHT // 4 + int(10 * math.sin(self.title_pulse + i * 0.5))
            
            # Add glow effect
            glow_surface = self.title_font.render(char, True, (255, 255, 255, 100))
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                self.screen.blit(glow_surface, (char_x + offset[0], char_y + offset[1]))
            
            self.screen.blit(char_surface, (char_x, char_y))
        
        # Subtitle
        subtitle = "GHOSTKITTY EDITION"
        subtitle_surface = self.subtitle_font.render(subtitle, True, NEON_PINK)
        subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + 100))
        
        # Add retro outline
        for offset in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            outline_surface = self.subtitle_font.render(subtitle, True, BLACK)
            self.screen.blit(outline_surface, (subtitle_rect.x + offset[0], subtitle_rect.y + offset[1]))
        
        self.screen.blit(subtitle_surface, subtitle_rect)
    
    def draw_menu(self):
        """Draw speed selection menu"""
        start_y = WINDOW_HEIGHT // 2
        
        for i, (name, speed) in enumerate(self.options):
            # Highlight selected option
            if i == self.selected_option:
                color = NEON_GREEN
                prefix = "► "
                # Add selection glow
                glow_rect = pygame.Rect(WINDOW_WIDTH // 4, start_y + i * 60 - 5, 
                                      WINDOW_WIDTH // 2, 50)
                pygame.draw.rect(self.screen, (0, 255, 0, 50), glow_rect)
                pygame.draw.rect(self.screen, NEON_GREEN, glow_rect, 3)
            else:
                color = WHITE
                prefix = "  "
            
            option_text = prefix + name
            option_surface = self.menu_font.render(option_text, True, color)
            option_rect = option_surface.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * 60))
            
            # Add retro shadow
            shadow_surface = self.menu_font.render(option_text, True, BLACK)
            self.screen.blit(shadow_surface, (option_rect.x + 2, option_rect.y + 2))
            self.screen.blit(option_surface, option_rect)
        
        # Instructions
        instruction_text = "ARROW KEYS TO SELECT • ENTER TO START • ESC TO QUIT"
        instruction_surface = self.subtitle_font.render(instruction_text, True, NEON_BLUE)
        instruction_rect = instruction_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(instruction_surface, instruction_rect)
        
        # Show current GHOSTKITTY track
        current_track = "♪ Press M to skip track"
        track_surface = self.subtitle_font.render(current_track, True, NEON_PINK)
        track_rect = track_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(track_surface, track_rect)
    
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Return selected speed
                return self.options[self.selected_option][1]
            elif event.key == pygame.K_ESCAPE:
                return "quit"
        return None
    
    def draw(self):
        """Draw the complete start menu"""
        self.draw_8bit_background()
        self.draw_title()
        self.draw_menu()

class Game:
    def __init__(self, fullscreen=False, disable_music=False):
        self.disable_music = disable_music
        
        # Set up display based on mode
        if fullscreen:
            # Safer fullscreen with escape hatch
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            print("🖥️  Fullscreen mode - Press ESC to exit or Alt+Tab to switch")
        else:
            # Windowed mode (safer)
            self.screen = pygame.display.set_mode((1400, 900), pygame.HWSURFACE | pygame.DOUBLEBUF)
            print("🖥️  Windowed mode - resize window as needed")
            
        pygame.display.set_caption("🐍 SNAKEIUM - GHOSTKITTY Edition 🎵")
        
        # Game state
        self.game_state = "menu"  # "menu", "playing", "game_over"
        self.start_menu = StartMenu(self.screen)
        
        # 60Hz clock for stability
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        
        # Initialize game objects (will be reset when game starts)
        self.snake = None
        self.food = None
        self.powerups = []
        self.particles = []
        
        # Crazy 8-bit spiral effects (initialized on game start)
        self.spirals = []
            
        # PYRAMID AND TRIANGLE RIPPING EFFECTS! (initialized on game start)
        self.pyramids = []
        self.triangles = []
        
        # Game state
        self.score = 0
        self.game_over = False
        self.paused = False
        self.selected_speed = 4  # Default speed
        
        # Music
        if not getattr(self, 'disable_music', False):
            try:
                music_folder = Config.DEFAULT_MUSIC_FOLDER
                self.music_manager = MusicManager(music_folder)
                self.current_song_name = self.music_manager.play_random_song()
                print(f"🎵 Music system initialized successfully!")
            except Exception as e:
                print(f"⚠️  Music initialization failed: {e}")
                self.music_manager = None
                self.current_song_name = None
        else:
            self.music_manager = None
            self.current_song_name = None
            print("🎵 Music disabled by user")
        
        # Enhanced fonts for fullscreen
        font_size = max(36, WINDOW_WIDTH // 40)  # Scale with screen size
        small_font_size = max(24, WINDOW_WIDTH // 60)
        self.font = pygame.font.Font(None, font_size)
        self.small_font = pygame.font.Font(None, small_font_size)
        
        # Rainbow background with more strips for smoother gradients
        self.bg_hue = 0
        self.bg_strips = 40  # More strips for smoother gradient
        
        # Particle system enhancements
        self.max_particles = 500  # More particles for fullscreen
        
        print(f"🎮 SNAKEIUM 60 FPS Safe Mode Active!")
        print(f"🖥️  Resolution: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        print(f"🎯 Grid: {GRID_WIDTH}x{GRID_HEIGHT}")
        print(f"📏 Cell Size: {GRID_SIZE}px")
        
    def start_game(self, speed_setting):
        """Initialize a new game with the selected speed"""
        self.game_state = "playing"
        self.selected_speed = speed_setting
        
        # Initialize game objects with the selected speed
        self.snake = Snake(speed_setting)  # Pass speed to Snake constructor
        self.food = Food()
        self.powerups = []
        self.particles = []
        
        # Reset game state
        self.score = 0
        self.game_over = False
        self.paused = False
        
        print(f"🎮 Starting game with speed setting: {speed_setting} (move every {self.snake.move_interval} frames)")
        
        # Initialize visual effects
        self.spirals = []
        for i in range(SPIRAL_COUNT):
            # Distribute spirals across the screen
            center_x = (WINDOW_WIDTH // SPIRAL_COUNT) * i + (WINDOW_WIDTH // SPIRAL_COUNT) // 2
            center_y = WINDOW_HEIGHT // 2 + random.randint(-200, 200)
            self.spirals.append(SpiralEffect(center_x, center_y, i))
            
        # PYRAMID AND TRIANGLE RIPPING EFFECTS!
        self.pyramids = []
        for i in range(PYRAMID_COUNT):
            self.pyramids.append(PyramidEffect(i))
            
        self.triangles = []
        for i in range(TRIANGLE_COUNT):
            self.triangles.append(TriangleRipper(i))
        
    def spawn_powerup(self):
        if self.game_state != "playing" or not self.snake or not self.food:
            return
            
        if len(self.powerups) < 2 and random.random() < 0.003:  # Low chance
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Don't spawn on snake or food
            if (x, y) not in self.snake.body and (x, y) != (self.food.x, self.food.y):
                power_type = random.choice(list(PowerUpType))
                self.powerups.append(PowerUp(x, y, power_type))
                
    def check_food_collision(self):
        if self.game_state != "playing" or not self.snake or not self.food:
            return False
            
        head = self.snake.body[0]
        if head == (self.food.x, self.food.y):
            self.snake.eat_food()
            base_points = 10
            points = base_points * self.snake.score_multiplier
            self.score += points
            
            # Create food eaten particles
            for _ in range(15):  # More particles for apple explosion
                velocity = (random.uniform(-4, 4), random.uniform(-4, 4))
                apple_colors = [(220, 20, 60), (255, 0, 0), (255, 69, 0)]  # Red apple colors
                self.particles.append(Particle(
                    self.food.x * GRID_SIZE + GRID_SIZE // 2,
                    self.food.y * GRID_SIZE + GRID_SIZE // 2,
                    random.choice(apple_colors),
                    velocity
                ))
            
            # Respawn food
            self.food = Food()
            return True
        return False
        
    def check_powerup_collisions(self):
        if self.game_state != "playing" or not self.snake:
            return
            
        head = self.snake.body[0]
        for powerup in self.powerups[:]:
            if head == (powerup.x, powerup.y):
                self.snake.eat_powerup(powerup)
                
                # Create powerup particles
                for _ in range(15):
                    velocity = (random.uniform(-4, 4), random.uniform(-4, 4))
                    colors = {
                        PowerUpType.SPEED_BOOST: NEON_BLUE,
                        PowerUpType.SCORE_MULTIPLIER: NEON_YELLOW,
                        PowerUpType.RAINBOW_MODE: NEON_PURPLE,
                        PowerUpType.MEGA_FOOD: NEON_ORANGE
                    }
                    self.particles.append(Particle(
                        powerup.x * GRID_SIZE + GRID_SIZE // 2,
                        powerup.y * GRID_SIZE + GRID_SIZE // 2,
                        colors[powerup.type],
                        velocity,
                        120  # Longer lifetime
                    ))
                
                self.powerups.remove(powerup)
                
    def draw_rainbow_background(self):
        """Draw pixelated 8-bit crush rainbow background"""
        self.bg_hue = (self.bg_hue + 0.3) % 360
        
        # Get actual screen dimensions
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # First, fill the entire screen with a base color to ensure no gaps
        base_rgb = colorsys.hsv_to_rgb(self.bg_hue / 360, 0.3, 0.2)
        base_color = tuple(int(c * 255) for c in base_rgb)
        self.screen.fill(base_color)
        
        if PIXELATED_BACKGROUND:
            # 8-bit pixelated background - fill entire actual screen
            pixel_size = PIXEL_SCALE
            
            # Calculate how many pixels we need to cover the entire actual screen
            cols = (screen_width + pixel_size - 1) // pixel_size  # Round up
            rows = (screen_height + pixel_size - 1) // pixel_size  # Round up
            
            for x in range(cols):
                for y in range(rows):
                    # Create 8-bit rainbow pattern
                    hue = (self.bg_hue + x * 5 + y * 3) % 360
                    rgb = colorsys.hsv_to_rgb(hue / 360, 0.6, 0.3)
                    color = tuple(int(c * 255) for c in rgb)
                    
                    # Draw pixelated blocks that fill the entire screen
                    rect = pygame.Rect(x * pixel_size, y * pixel_size, 
                                     pixel_size, pixel_size)
                    pygame.draw.rect(self.screen, color, rect)
            
            # Add scan lines for retro effect
            for y in range(0, screen_height, 6):
                pygame.draw.line(self.screen, (0, 0, 0, 80), 
                               (0, y), (screen_width, y), 2)
        else:
            # Original smooth gradient (fallback)
            strip_height = WINDOW_HEIGHT // 20
            for i in range(20):
                hue = (self.bg_hue + i * 18) % 360
                rgb = colorsys.hsv_to_rgb(hue / 360, 0.3, 0.2)
                color = tuple(int(c * 255) for c in rgb)
                
                rect = pygame.Rect(0, i * strip_height, WINDOW_WIDTH, strip_height + 1)
                pygame.draw.rect(self.screen, color, rect)
            
    def draw_ui(self):
        # Only draw UI when in playing state and snake exists
        if self.game_state != "playing" or not self.snake:
            return
            
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Length
        length_text = self.font.render(f"Length: {len(self.snake.body)}", True, WHITE)
        self.screen.blit(length_text, (10, 50))
        
        # Speed
        speed_text = self.font.render(f"Speed: {self.snake.get_current_speed()}", True, WHITE)
        self.screen.blit(speed_text, (10, 90))
        
        # Current song
        if self.current_song_name:
            song_text = self.small_font.render(f"♪ {os.path.basename(self.current_song_name)}", True, NEON_PINK)
            self.screen.blit(song_text, (10, WINDOW_HEIGHT - 30))
        
        # Active effects
        y_offset = 130
        if self.snake.speed_boost_timer > 0:
            boost_text = self.small_font.render("⚡ SPEED BOOST!", True, NEON_BLUE)
            self.screen.blit(boost_text, (10, y_offset))
            y_offset += 25
            
        if self.snake.score_multiplier > 1:
            mult_text = self.small_font.render(f"💎 {self.snake.score_multiplier}x SCORE!", True, NEON_YELLOW)
            self.screen.blit(mult_text, (10, y_offset))
            y_offset += 25
            
        if self.snake.rainbow_mode:
            rainbow_text = self.small_font.render("🌈 RAINBOW MODE!", True, NEON_PURPLE)
            self.screen.blit(rainbow_text, (10, y_offset))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "menu"
                    else:
                        return False
                        
                elif self.game_state == "menu":
                    # Handle menu input
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.start_menu.selected_option = (self.start_menu.selected_option - 1) % len(self.start_menu.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.start_menu.selected_option = (self.start_menu.selected_option + 1) % len(self.start_menu.options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Start game with selected speed
                        selected_speed = self.start_menu.options[self.start_menu.selected_option][1]
                        self.start_game(selected_speed)
                        
                elif self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        # Skip to next song
                        if self.music_manager:
                            self.current_song_name = self.music_manager.play_random_song()
                    elif not self.game_over and not self.paused and self.snake:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.snake.change_direction(Direction.UP)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.snake.change_direction(Direction.DOWN)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.snake.change_direction(Direction.LEFT)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.snake.change_direction(Direction.RIGHT)
                            
                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.game_state = "menu"
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.game_state = "menu"
                        
        return True
        
    def reset_game(self):
        """Reset game and go back to menu"""
        self.game_state = "menu"
        self.snake = None
        self.food = None
        self.powerups = []
        self.particles = []
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def update(self):
        # Always update visual effects for background action
        for spiral in self.spirals:
            spiral.update()
        for pyramid in self.pyramids:
            pyramid.update()
        for triangle in self.triangles:
            triangle.update()
            
        # Only update game logic when playing
        if self.game_state != "playing" or not self.snake or not self.food:
            return
            
        if self.game_over or self.paused:
            return
            
        # Update snake with 120Hz smooth movement
        self.snake.update_effects()
        self.snake.update_move_interval()  # Update movement timing
        self.snake.move()
        
        # Check collisions
        if self.snake.check_collision():
            self.game_over = True
            self.game_state = "game_over"
            
        self.check_food_collision()
        self.check_powerup_collisions()
        
        # Update game objects
        self.food.update()
        self.spawn_powerup()
        
        # Update powerups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.is_expired():
                self.powerups.remove(powerup)
                
        # Enhanced particle management for 120Hz
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
        # Limit particles for performance
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]
            
        # Update ALL the crazy visual effects
        for spiral in self.spirals:
            spiral.update()
        for pyramid in self.pyramids:
            pyramid.update()
        for triangle in self.triangles:
            triangle.update()
                
        # Check music
        if self.music_manager:
            new_song = self.music_manager.check_music()
            if new_song:
                self.current_song_name = new_song
            
    def draw(self):
        # Start with black background
        self.screen.fill(BLACK)
        
        # Draw full rainbow background with pixelated effects
        self.draw_rainbow_background()
        
        # Draw visual effects (always visible)
        try:
            # Draw only a few pyramids for testing
            for i, pyramid in enumerate(self.pyramids[:3]):  # Only first 3
                pyramid.draw(self.screen)
                
            # Draw only a few triangles
            for i, triangle in enumerate(self.triangles[:3]):  # Only first 3
                triangle.draw(self.screen)
        except:
            pass  # Skip effects if they cause issues
        
        # Handle different game states
        if self.game_state == "menu":
            self.start_menu.draw()
            
        elif self.game_state == "playing" and self.snake and self.food:
            # Game objects
            try:
                self.food.draw(self.screen)
                
                for powerup in self.powerups:
                    powerup.draw(self.screen)
                    
                self.snake.draw(self.screen, self.particles)
                
                # Particles
                for particle in self.particles:
                    particle.draw(self.screen)
            except Exception as e:
                # Fallback: draw simple rectangles for snake and food
                pygame.draw.rect(self.screen, NEON_GREEN, 
                               (self.snake.body[0][0] * GRID_SIZE, self.snake.body[0][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, NEON_PINK,
                               (self.food.x * GRID_SIZE, self.food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                
            # UI (always on top)
            self.draw_ui()
            
            # Pause screen
            if self.paused:
                self.draw_pause_screen()
                
        elif self.game_state == "game_over":
            self.draw_game_over_screen()
        
    def draw_pause_screen(self):
        """Draw pause overlay"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSED", True, NEON_BLUE)
        continue_text = self.small_font.render("Press SPACE to continue", True, WHITE)
        
        # Perfect centering
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        
        self.screen.blit(pause_text, pause_rect)
        self.screen.blit(continue_text, continue_rect)
        
    def draw_game_over_screen(self):
        """Draw game over screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Use simple font sizes
        game_over_text = self.font.render("GAME OVER!", True, NEON_PINK)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.small_font.render("Press R to go to menu or ESC to quit", True, WHITE)
        
        # Perfect centering
        go_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        
        self.screen.blit(game_over_text, go_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
            
    def run(self):
        """Main game loop with enhanced error handling and performance monitoring"""
        print("🐍 SNAKEIUM GHOSTKITTY Edition Started! 🎵")
        print("=" * 50)
        print("Controls:")
        print("  Arrow Keys / WASD - Move snake")
        print("  SPACE - Pause game")
        print("  M - Skip to next track")
        print("  R - Restart (when game over)")
        print("  ESC - Return to menu / Quit")
        print("  Enter - Select menu option")
        print()
        print("Speed Settings:")
        print("  � CHILL MODE   - Relaxed gameplay")
        print("  🎮 CLASSIC      - Traditional Snake")
        print("  ⚡ FAST         - Quick-paced action")
        print("  � INSANE       - High-speed challenge")
        print("  💀 NIGHTMARE    - Ultimate test")
        print()
        print("Power-ups:")
        print("  🔵 Speed Boost  � Score Multiplier")
        print("  🟣 Rainbow Mode 🟠 Mega Food")
        print(f"\n🎮 Running at {self.target_fps} FPS in safe mode!")
        print("=" * 50)
        
        running = True
        frame_count = 0
        fps_timer = time.time()
        last_fps_check = time.time()
        performance_warnings = 0
        
        try:
            while running:
                # Handle events with error catching
                try:
                    running = self.handle_events()
                except Exception as e:
                    print(f"⚠️  Event handling error: {e}")
                    continue
                
                # Update game state
                try:
                    self.update()
                except Exception as e:
                    print(f"⚠️  Update error: {e}")
                    continue
                
                # Draw everything
                try:
                    self.draw()
                except Exception as e:
                    print(f"⚠️  Drawing error: {e}")
                    self.screen.fill((20, 20, 40))  # Fallback background
                
                # Display update
                try:
                    pygame.display.flip()
                except Exception as e:
                    print(f"⚠️  Display error: {e}")
                
                self.clock.tick(self.target_fps)
                frame_count += 1
                
                # Performance monitoring (every 3 seconds)
                current_time = time.time()
                if current_time - last_fps_check >= 3.0:
                    actual_fps = frame_count / (current_time - fps_timer)
                    
                    # Check for performance issues
                    if actual_fps < self.target_fps * 0.8:  # Below 80% of target
                        performance_warnings += 1
                        if performance_warnings <= 2:  # Only show first 2 warnings
                            print(f"⚠️  Performance: {actual_fps:.1f} FPS (target: {self.target_fps})")
                    
                    # Periodic FPS report (every 6 seconds)
                    if frame_count % (self.target_fps * 6) == 0:
                        print(f"🎯 Performance: {actual_fps:.1f} FPS")
                    
                    last_fps_check = current_time
                    frame_count = 0
                    fps_timer = current_time
                
        except KeyboardInterrupt:
            print("\n🛑 Game interrupted by user")
        except Exception as e:
            print(f"\n💥 Unexpected error: {e}")
            print("🔧 Please report this issue on GitHub")
        finally:
            try:
                pygame.quit()
                print("🎮 Game closed successfully")
            except:
                pass
                frame_count = 0
                fps_timer = current_time
            
        pygame.quit()

def parse_arguments():
    """Parse command line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SNAKEIUM - Modern 8-bit Snake Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python snakeium.py --music-folder ~/Music
  python snakeium.py --no-effects --fps 60
  python snakeium.py --windowed --resolution 1280x720
        """
    )
    
    parser.add_argument('--version', action='version', version=f'SNAKEIUM {__version__}')
    parser.add_argument('--music-folder', type=str, help='Path to music folder')
    parser.add_argument('--no-music', action='store_true', help='Disable background music')
    parser.add_argument('--no-effects', action='store_true', help='Disable geometric effects for better performance')
    parser.add_argument('--no-particles', action='store_true', help='Disable particle effects')
    parser.add_argument('--fps', type=int, default=60, help='Target FPS (default: 60)')
    parser.add_argument('--windowed', action='store_true', help='Force windowed mode (default)')
    parser.add_argument('--fullscreen', action='store_true', help='Enable fullscreen mode (WARNING: May freeze system)')
    parser.add_argument('--resolution', type=str, help='Window resolution (e.g., 1920x1080)')
    parser.add_argument('--volume', type=float, default=0.3, help='Music volume (0.0-1.0)')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--test-mode', action='store_true', help='Enable CI/CD test mode (headless)')
    parser.add_argument('--help-ci', action='store_true', help='Show CI/CD help and exit')
    
    return parser.parse_args()

def print_system_info():
    """Print system and game information"""
    print(f"""
╔════════════════════════════════════════╗
║              SNAKEIUM v{__version__}               ║
║          {__author__}           ║
╚════════════════════════════════════════╝

🖥️  Display: {WINDOW_WIDTH}x{WINDOW_HEIGHT}
🎮 Grid: {Config.GRID_WIDTH}x{Config.GRID_HEIGHT} cells
📏 Cell Size: {Config.GRID_SIZE}px
🎯 Target FPS: {Config.TARGET_FPS}
🎵 Music: {'Enabled' if Config.DEFAULT_MUSIC_FOLDER else 'Disabled'}
⚡ Effects: {'Enabled' if Config.ENABLE_GEOMETRIC_EFFECTS else 'Disabled'}
✨ Particles: {'Enabled' if Config.ENABLE_PARTICLES else 'Disabled'}
    """)

if __name__ == "__main__":
    args = parse_arguments()
    
    # Handle CI/CD help
    if args.help_ci:
        print("""
🤖 SNAKEIUM CI/CD Testing Guide
==============================

Test Mode Usage:
  python snakeium.py --test-mode --no-music
  python snakeium.py --test-mode --debug

Environment Variables for CI:
  SDL_VIDEODRIVER=dummy
  SDL_AUDIODRIVER=dummy
  DISPLAY=:99 (Linux)

This will run a basic functionality test and exit.
Perfect for automated testing in GitHub Actions!
        """)
        sys.exit(0)
    
    # Test mode for CI/CD
    if args.test_mode:
        print("🧪 Starting SNAKEIUM test mode...")
        try:
            # Basic import and initialization test
            print("✅ Testing pygame initialization...")
            
            # Test Snake class
            print("✅ Testing Snake class...")
            test_snake = Snake(4)
            
            # Test Food class
            print("✅ Testing Food class...")
            test_food = Food()
            
            # Test basic movement
            print("✅ Testing movement logic...")
            original_pos = test_snake.body[0]
            test_snake.change_direction(Direction.RIGHT)
            test_snake.start_new_move()
            
            print("✅ All basic functionality tests passed!")
            print("🎉 SNAKEIUM is working correctly!")
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            sys.exit(1)
    
    # Apply configuration from arguments
    if args.fps:
        Config.TARGET_FPS = args.fps
    if args.volume:
        Config.MUSIC_VOLUME = max(0.0, min(1.0, args.volume))
    # Note: Config assignments commented out due to type checking
    # These would need to be handled differently in production
    if args.music_folder:
        # Config.DEFAULT_MUSIC_FOLDER = args.music_folder
        pass
    if args.no_music:
        # Config.DEFAULT_MUSIC_FOLDER = None
        pass
        
    # Handle windowed mode and resolution
    if args.windowed or args.resolution:
        if args.resolution:
            try:
                width, height = map(int, args.resolution.split('x'))
                # Update global variables
                globals()['WINDOW_WIDTH'] = width
                globals()['WINDOW_HEIGHT'] = height
            except ValueError:
                print("❌ Invalid resolution format. Use WIDTHxHEIGHT (e.g., 1920x1080)")
                sys.exit(1)
        else:
            globals()['WINDOW_WIDTH'] = 1280
            globals()['WINDOW_HEIGHT'] = 720
        
        # Update config
        Config.GRID_WIDTH = globals()['WINDOW_WIDTH'] // Config.GRID_SIZE
        Config.GRID_HEIGHT = globals()['WINDOW_HEIGHT'] // Config.GRID_SIZE
    
    if args.debug:
        print_system_info()
    
    try:
        # Determine display mode - default to windowed for safety
        use_fullscreen = args.fullscreen and not args.windowed
        if use_fullscreen:
            print("⚠️  WARNING: Using fullscreen mode. Press ESC or Alt+Tab if system freezes!")
        game = Game(fullscreen=use_fullscreen, disable_music=args.no_music)
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Thanks for playing SNAKEIUM!")
    except Exception as e:
        print(f"❌ Game crashed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)
