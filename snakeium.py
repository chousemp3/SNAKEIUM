#!/usr/bin/env python3
"""
SNAKEIUM - GHOSTKITTY Edition
=============================

A modern retro Snake game with 8-bit visuals, rainbow effects, and GHOSTKITTY music.
Ultra-smooth 60 FPS gameplay with power-ups, particle effects, and authentic retro aesthetics.

Controls:
    Arrow Keys / WASD: Move snake
    SPACE: Pause game
    M: Skip to next track
    R: Restart (when game over)
    ESC: Return to menu / Quit
    Enter: Select menu option
    F2: Toggle grid overlay
    F3: Toggle FPS counter

Requirements:
    Python 3.8+
    pygame 2.0+

Usage:
    python snakeium.py
    python snakeium.py --fullscreen
    python snakeium.py --no-music

Author: GHOSTKITTY APPS
Version: 2.1.0
License: MIT
"""

import pygame
import random
import math
import os
import glob
import colorsys
import time
import sys
import json
from enum import Enum
from typing import List, Tuple, Optional
from pathlib import Path

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

__version__ = "2.1.0"
__author__ = "GHOSTKITTY APPS"

# ---------------------------------------------------------------------------
# Optional dependencies
# ---------------------------------------------------------------------------

try:
    import mutagen
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ---------------------------------------------------------------------------
# Pygame initialisation
# ---------------------------------------------------------------------------

try:
    if os.environ.get("SDL_VIDEODRIVER") == "dummy":
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

    pygame.init()

    if os.environ.get("SDL_AUDIODRIVER") != "dummy":
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

except pygame.error as exc:
    print(f"Failed to initialise Pygame: {exc}")
    if "--test-mode" not in sys.argv:
        sys.exit(1)
except Exception as exc:
    print(f"Unexpected error during Pygame init: {exc}")
    if "--test-mode" not in sys.argv:
        sys.exit(1)

# ---------------------------------------------------------------------------
# Display constants
# ---------------------------------------------------------------------------

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class Config:
    """Central game configuration."""

    # Display
    GRID_SIZE = 25
    GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
    GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
    TARGET_FPS = 60

    # Visual effects
    SMOOTH_MOVEMENT = True
    INTERPOLATION_STEPS = 15
    EASING_FACTOR = 0.12
    SUB_PIXEL_MOVEMENT = True
    PIXELATED_BACKGROUND = True
    PIXEL_SCALE = 8

    PYRAMID_COUNT = 5
    TRIANGLE_COUNT = 8
    SPIRAL_COUNT = 8
    PYRAMID_SPEED = 1.5
    TRIANGLE_SPEED = 2.0
    SPIRAL_SPEED = 2.0
    SPIRAL_RADIUS_MAX = 100

    # Particles
    MAX_PARTICLES = 200

    # Music
    DEFAULT_MUSIC_FOLDER = ""
    MUSIC_VOLUME = 0.3

    # Performance
    ENABLE_VSYNC = True
    ENABLE_PARTICLES = True
    ENABLE_GEOMETRIC_EFFECTS = True

    # Persistence
    HIGH_SCORE_FILE = str(Path.home() / ".snakeium" / "high_scores.json")


# Module-level aliases (used throughout the file)
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

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_GREEN = (0, 255, 127)
NEON_PINK = (255, 20, 147)
NEON_BLUE = (0, 191, 255)
NEON_PURPLE = (191, 0, 255)
NEON_ORANGE = (255, 165, 0)
NEON_YELLOW = (255, 255, 0)
DARK_GRAY = (40, 40, 40)


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


# ===================================================================
# High Score Manager
# ===================================================================


class HighScoreManager:
    """Persistent high-score storage backed by a JSON file."""

    def __init__(self, filepath: str = None):
        self.filepath = filepath or Config.HIGH_SCORE_FILE
        self.scores: dict = {}
        self._load()

    def _load(self):
        try:
            path = Path(self.filepath)
            if path.exists():
                with open(path, "r", encoding="utf-8") as fh:
                    self.scores = json.load(fh)
        except Exception:
            self.scores = {}

    def _save(self):
        try:
            path = Path(self.filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(self.scores, fh, indent=2)
        except Exception:
            pass

    def add_score(self, speed_name: str, score: int, length: int):
        """Record a score.  Keeps top 10 per speed setting."""
        key = speed_name.strip().upper()
        if key not in self.scores:
            self.scores[key] = []
        entry = {
            "score": score,
            "length": length,
            "date": time.strftime("%Y-%m-%d %H:%M"),
        }
        self.scores[key].append(entry)
        self.scores[key].sort(key=lambda e: e["score"], reverse=True)
        self.scores[key] = self.scores[key][:10]
        self._save()

    def get_top_scores(self, speed_name: str, count: int = 5) -> list:
        key = speed_name.strip().upper()
        return self.scores.get(key, [])[:count]

    def get_best(self, speed_name: str) -> int:
        key = speed_name.strip().upper()
        entries = self.scores.get(key, [])
        return entries[0]["score"] if entries else 0


# ===================================================================
# Sprite helpers
# ===================================================================


def create_snake_head_sprite(size, direction, color):
    """Create an 8-bit style snake head sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
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
        "          ",
    ]
    pixel_size = size // 10
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == "O":
                pygame.draw.rect(surf, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == "*":
                pygame.draw.rect(surf, BLACK, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == "^":
                nostril = (color[0] // 2, color[1] // 2, color[2] // 2)
                pygame.draw.rect(surf, nostril, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

    if direction == Direction.RIGHT:
        surf = pygame.transform.rotate(surf, -90)
    elif direction == Direction.DOWN:
        surf = pygame.transform.rotate(surf, 180)
    elif direction == Direction.LEFT:
        surf = pygame.transform.rotate(surf, 90)
    return surf


def create_snake_body_sprite(size, color, is_tail=False):
    """Create an 8-bit style snake body segment."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    if is_tail:
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
            "          ",
        ]
    else:
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
            "          ",
        ]
    pixel_size = size // 10
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == "O":
                pygame.draw.rect(surf, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == "-":
                sc = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
                pygame.draw.rect(surf, sc, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    return surf


def create_apple_sprite(size):
    """Create an 8-bit style apple sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
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
        "   RRRR   ",
    ]
    pixel_size = size // 10
    for y, row in enumerate(pattern):
        for x, char in enumerate(row):
            if char == "R":
                pygame.draw.rect(surf, (220, 20, 60), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == "g":
                pygame.draw.rect(surf, (34, 139, 34), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
            elif char == "G":
                pygame.draw.rect(surf, (0, 255, 0), (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
    return surf


# ===================================================================
# Visual effect classes
# ===================================================================


class PyramidEffect:
    """Floating geometric pyramid in the background."""

    def __init__(self, pid):
        self.x = random.randint(-200, WINDOW_WIDTH + 200)
        self.y = random.randint(-200, WINDOW_HEIGHT + 200)
        self.size = random.randint(50, 150)
        self.speed_x = random.uniform(-PYRAMID_SPEED, PYRAMID_SPEED)
        self.speed_y = random.uniform(-PYRAMID_SPEED, PYRAMID_SPEED)
        self.rotation = 0.0
        self.rotation_speed = random.uniform(-2, 2)
        self.color_offset = pid * 45

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rotation += self.rotation_speed
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
        if self.x < -500 or self.x > WINDOW_WIDTH + 500 or self.y < -500 or self.y > WINDOW_HEIGHT + 500:
            return
        hue = (time.time() * 30 + self.color_offset) % 360
        rgb = colorsys.hsv_to_rgb(hue / 360, 0.8, 0.9)
        color = tuple(int(c * 255) for c in rgb)
        hs = self.size // 2
        points = [
            (int(self.x), int(self.y - hs)),
            (int(self.x - hs), int(self.y + hs)),
            (int(self.x + hs), int(self.y + hs)),
        ]
        if abs(self.rotation) > 0.1:
            cx, cy = int(self.x), int(self.y)
            cos_r = math.cos(math.radians(self.rotation))
            sin_r = math.sin(math.radians(self.rotation))
            rot = []
            for px, py in points:
                dx, dy = px - cx, py - cy
                rot.append((int(dx * cos_r - dy * sin_r + cx), int(dx * sin_r + dy * cos_r + cy)))
            points = rot
        try:
            if len(points) >= 3:
                pygame.draw.polygon(screen, color, points)
                pygame.draw.polygon(screen, WHITE, points, 1)
        except (ValueError, TypeError):
            pass


class TriangleRipper:
    """Fast triangles ripping across the screen."""

    def __init__(self, tid):
        self.reset_position()
        self.size = random.randint(20, 60)
        self.speed_x = random.uniform(-TRIANGLE_SPEED, TRIANGLE_SPEED)
        self.speed_y = random.uniform(-TRIANGLE_SPEED, TRIANGLE_SPEED)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.color_offset = tid * 20
        self.trail_points: list = []

    def reset_position(self):
        edge = random.randint(0, 3)
        if edge == 0:
            self.x, self.y = random.randint(0, WINDOW_WIDTH), -50
        elif edge == 1:
            self.x, self.y = WINDOW_WIDTH + 50, random.randint(0, WINDOW_HEIGHT)
        elif edge == 2:
            self.x, self.y = random.randint(0, WINDOW_WIDTH), WINDOW_HEIGHT + 50
        else:
            self.x, self.y = -50, random.randint(0, WINDOW_HEIGHT)

    def update(self):
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > 10:
            self.trail_points.pop(0)
        self.x += self.speed_x
        self.y += self.speed_y
        self.rotation += self.rotation_speed
        if self.x < -100 or self.x > WINDOW_WIDTH + 100 or self.y < -100 or self.y > WINDOW_HEIGHT + 100:
            self.reset_position()
            self.trail_points.clear()

    def draw(self, screen):
        if self.x < -200 or self.x > WINDOW_WIDTH + 200 or self.y < -200 or self.y > WINDOW_HEIGHT + 200:
            return
        for i, (tx, ty) in enumerate(self.trail_points):
            if i % 2 == 0:
                af = i / max(1, len(self.trail_points))
                ts = max(1, int(self.size * af * 0.3))
                if ts > 1:
                    hue = (time.time() * 50 + self.color_offset) % 360
                    rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
                    c = tuple(int(v * 255) for v in rgb)
                    try:
                        pygame.draw.circle(screen, c, (int(tx), int(ty)), ts)
                    except (ValueError, TypeError):
                        pass
        hue = (time.time() * 80 + self.color_offset) % 360
        rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
        color = tuple(int(v * 255) for v in rgb)
        hs = self.size // 2
        points = [
            (int(self.x), int(self.y - hs)),
            (int(self.x - hs), int(self.y + hs)),
            (int(self.x + hs), int(self.y + hs)),
        ]
        cx, cy = int(self.x), int(self.y)
        cos_r = math.cos(math.radians(self.rotation))
        sin_r = math.sin(math.radians(self.rotation))
        rot = []
        for px, py in points:
            dx, dy = px - cx, py - cy
            rot.append((int(dx * cos_r - dy * sin_r + cx), int(dx * sin_r + dy * cos_r + cy)))
        try:
            if len(rot) >= 3:
                pygame.draw.polygon(screen, color, rot)
                pygame.draw.polygon(screen, WHITE, rot, 1)
        except (ValueError, TypeError):
            pass


class SpiralEffect:
    """Rainbow spiral in the background."""

    def __init__(self, center_x, center_y, sid):
        self.center_x = center_x
        self.center_y = center_y
        self.angle = sid * (360 / SPIRAL_COUNT) if SPIRAL_COUNT else 0
        self.max_radius = SPIRAL_RADIUS_MAX
        self.time_offset = sid * 0.5
        self.points: list = []

    def update(self):
        self.angle += SPIRAL_SPEED
        t = time.time() + self.time_offset
        self.points = []
        for i in range(50):
            pa = self.angle + i * 15
            pr = (i * 2) % self.max_radius
            wobble = 10 * math.sin(t * 3 + i * 0.2)
            x = self.center_x + (pr + wobble) * math.cos(math.radians(pa))
            y = self.center_y + (pr + wobble) * math.sin(math.radians(pa))
            hue = (pa + t * 50) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
            color = tuple(int(c * 255) for c in rgb)
            self.points.append((x, y, color, pr))

    def draw(self, screen):
        for x, y, color, radius in self.points:
            if 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT:
                sz = max(2, int(4 - radius / 30))
                pygame.draw.rect(screen, color, (int(x), int(y), sz, sz))


# ===================================================================
# Power-ups and Particles
# ===================================================================


class PowerUpType(Enum):
    SPEED_BOOST = "speed"
    SCORE_MULTIPLIER = "score"
    RAINBOW_MODE = "rainbow"
    MEGA_FOOD = "mega"


class Particle:
    """Lightweight particle for visual feedback."""

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
        self.vy += 0.1  # gravity

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.circle(screen, self.color[:3], (int(self.x), int(self.y)), self.size)


class PowerUp:
    """Collectable power-up item on the grid."""

    def __init__(self, x, y, power_type: PowerUpType):
        self.x = x
        self.y = y
        self.type = power_type
        self.spawn_time = time.time()
        self.lifetime = 10
        self.pulse = 0.0

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
            PowerUpType.MEGA_FOOD: NEON_ORANGE,
        }
        color = colors[self.type]
        cx = self.x * GRID_SIZE + GRID_SIZE // 2
        cy = self.y * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(screen, color, (cx, cy), GRID_SIZE // 2 + pulse_size)
        pygame.draw.circle(screen, BLACK, (cx, cy), GRID_SIZE // 2 + pulse_size - 2)


# ===================================================================
# Music Manager
# ===================================================================


class MusicManager:
    """Music playback with metadata support and error handling."""

    def __init__(self, music_folder=None):
        self.music_folder = music_folder or Config.DEFAULT_MUSIC_FOLDER
        self.playlist: list = []
        self.current_song: Optional[str] = None
        self.current_index = 0
        self.shuffle_mode = True
        self._load_playlist()

    def _load_playlist(self):
        """Scan for MP3 files."""
        if self.music_folder and os.path.exists(self.music_folder):
            try:
                self.playlist = glob.glob(os.path.join(self.music_folder, "*.mp3"))
            except Exception:
                pass

        if not self.playlist:
            search_paths = [
                os.path.join(os.path.expanduser("~"), "Music"),
                os.path.join(os.path.expanduser("~"), "Desktop"),
                os.path.join(os.getcwd(), "music"),
            ]
            for path in search_paths:
                if os.path.exists(path):
                    files = glob.glob(os.path.join(path, "**", "*.mp3"), recursive=True)
                    if files:
                        self.playlist = files[:50]
                        break

    def play_random_song(self) -> Optional[str]:
        """Play a song from the playlist."""
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
            return os.path.basename(self.current_song)
        except pygame.error:
            if self.current_song and self.current_song in self.playlist:
                self.playlist.remove(self.current_song)
                return self.play_random_song()
        except Exception:
            pass
        return None

    def check_music(self) -> Optional[str]:
        """Auto-advance when the current track ends."""
        try:
            if not pygame.mixer.music.get_busy() and self.playlist:
                return self.play_random_song()
        except Exception:
            pass
        return None

    def get_current_info(self) -> str:
        if self.current_song:
            return os.path.basename(self.current_song)
        return ""


# ===================================================================
# Snake
# ===================================================================


class Snake:
    """Player-controlled snake with smooth movement and power-up state."""

    def __init__(self, speed=4):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.grow = False
        self.speed = speed
        self.rainbow_mode = False
        self.rainbow_timer = 0
        self.speed_boost_timer = 0
        self.score_multiplier = 1
        self.score_multiplier_timer = 0

        # Smooth movement
        self.move_timer = 0
        self.move_interval = max(1, 60 // self.speed)
        self.smooth_positions: list = []
        self.target_positions: list = []
        self.movement_progress = 0.0
        self.is_moving = False

        # Input buffer (queues up to 2 direction changes for responsiveness)
        self._input_buffer: list = []

        for x, y in self.body:
            self.smooth_positions.append([float(x), float(y)])
            self.target_positions.append((x, y))

    # -- easing --

    @staticmethod
    def ease_out_quart(t):
        return 1 - (1 - t) ** 4

    def update_smooth_positions(self):
        if not SMOOTH_MOVEMENT:
            self.smooth_positions = [[float(x), float(y)] for x, y in self.body]
            return
        if self.is_moving and self.movement_progress < 1.0:
            eased = self.ease_out_quart(self.movement_progress)
            for i in range(len(self.body)):
                if i < len(self.smooth_positions) and i < len(self.target_positions):
                    sx, sy = self.smooth_positions[i]
                    tx, ty = self.target_positions[i]
                    self.smooth_positions[i][0] = sx + (tx - sx) * eased
                    self.smooth_positions[i][1] = sy + (ty - sy) * eased
        else:
            for i in range(len(self.body)):
                if i < len(self.smooth_positions):
                    self.smooth_positions[i][0] = float(self.body[i][0])
                    self.smooth_positions[i][1] = float(self.body[i][1])

    def move(self):
        self.move_timer += 1
        if self.is_moving:
            self.movement_progress = min(1.0, self.move_timer / self.move_interval)
            self.update_smooth_positions()
            if self.movement_progress >= 1.0:
                self.is_moving = False
                self.movement_progress = 0.0
                self.move_timer = 0

        if not self.is_moving and self.move_timer >= self.move_interval:
            # consume buffered input
            if self._input_buffer:
                self._apply_direction(self._input_buffer.pop(0))
            self._start_new_move()

        self.update_smooth_positions()

    def _start_new_move(self):
        self.move_timer = 0
        self.movement_progress = 0.0
        self.is_moving = True

        for i in range(len(self.body)):
            if i >= len(self.smooth_positions):
                self.smooth_positions.append([float(self.body[i][0]), float(self.body[i][1])])

        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        self.target_positions = list(self.body)

        while len(self.smooth_positions) > len(self.body):
            self.smooth_positions.pop()
        while len(self.smooth_positions) < len(self.body):
            bx, by = self.body[len(self.smooth_positions)]
            self.smooth_positions.append([float(bx), float(by)])

    def _apply_direction(self, new_direction: Direction):
        if len(self.body) > 1:
            cdx, cdy = self.direction.value
            ndx, ndy = new_direction.value
            if (cdx, cdy) != (-ndx, -ndy):
                self.direction = new_direction
        else:
            self.direction = new_direction

    def change_direction(self, new_direction: Direction):
        """Queue a direction change (input buffering)."""
        if len(self._input_buffer) < 2:
            self._input_buffer.append(new_direction)
        if not self.is_moving and self._input_buffer:
            self._apply_direction(self._input_buffer.pop(0))

    def eat_food(self):
        self.grow = True

    def eat_powerup(self, powerup: PowerUp):
        if powerup.type == PowerUpType.SPEED_BOOST:
            self.speed_boost_timer = 300
        elif powerup.type == PowerUpType.SCORE_MULTIPLIER:
            self.score_multiplier = 3
            self.score_multiplier_timer = 600
        elif powerup.type == PowerUpType.RAINBOW_MODE:
            self.rainbow_mode = True
            self.rainbow_timer = 900
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
        base = self.speed + len(self.body) // 8
        if self.speed_boost_timer > 0:
            return min(base * 1.8, 20)
        return base

    def update_move_interval(self):
        self.move_interval = max(60 // int(self.get_current_speed()), 1)

    def check_collision(self):
        return self.body[0] in self.body[1:]

    def get_rainbow_color(self, index):
        hue = (time.time() * 100 + index * 30) % 360
        rgb = colorsys.hsv_to_rgb(hue / 360, 1, 1)
        return tuple(int(c * 255) for c in rgb)

    def draw(self, screen, particles):
        if SMOOTH_MOVEMENT and self.smooth_positions:
            positions = [(p[0], p[1]) for p in self.smooth_positions]
        else:
            positions = [(float(x), float(y)) for x, y in self.body]

        for i, (x, y) in enumerate(positions):
            if SUB_PIXEL_MOVEMENT:
                px, py = x * GRID_SIZE, y * GRID_SIZE
            else:
                px, py = int(x) * GRID_SIZE, int(y) * GRID_SIZE

            if self.rainbow_mode:
                color = self.get_rainbow_color(i)
            elif i == 0:
                color = NEON_GREEN
            else:
                grad = 1 - (i / len(positions))
                color = (int(NEON_GREEN[0] * grad), int(NEON_GREEN[1] * grad), int(NEON_GREEN[2] * grad))

            if i == 0:
                sprite = create_snake_head_sprite(GRID_SIZE, self.direction, color)
            elif i == len(positions) - 1:
                sprite = create_snake_body_sprite(GRID_SIZE, color, is_tail=True)
            else:
                sprite = create_snake_body_sprite(GRID_SIZE, color, is_tail=False)
            screen.blit(sprite, (px, py))

            if self.rainbow_mode:
                glow_sz = GRID_SIZE + 6
                glow_surf = pygame.Surface((glow_sz, glow_sz), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, color, (glow_sz // 2, glow_sz // 2), glow_sz // 2)
                glow_surf.set_alpha(100)
                screen.blit(glow_surf, (px - 3, py - 3))

            if self.rainbow_mode and random.random() < 0.4:
                pc = self.get_rainbow_color(i + random.randint(0, 10))
                vel = (random.uniform(-3, 3), random.uniform(-3, 3))
                particles.append(Particle(px + GRID_SIZE // 2, py + GRID_SIZE // 2, pc, vel))


# ===================================================================
# Food
# ===================================================================


class Food:
    """Collectable food item with 8-bit sprite and animation."""

    def __init__(self):
        self.x = random.randint(0, GRID_WIDTH - 1)
        self.y = random.randint(0, GRID_HEIGHT - 1)
        self.pulse = 0.0
        self.apple_sprite = create_apple_sprite(GRID_SIZE)
        self.glow_intensity = 0.0
        self.bob_offset = 0.0
        self.sparkle_timer = 0

    def update(self):
        self.pulse += 0.08
        self.glow_intensity = (self.glow_intensity + 0.05) % (2 * math.pi)
        self.bob_offset += 0.04
        self.sparkle_timer += 1

    def draw(self, screen):
        bob_y = 2 * math.sin(self.bob_offset)
        x_pos = self.x * GRID_SIZE
        y_pos = self.y * GRID_SIZE + bob_y

        glow_size = int(4 + 2 * math.sin(self.glow_intensity))
        glow_surf = pygame.Surface((GRID_SIZE + glow_size * 4, GRID_SIZE + glow_size * 4), pygame.SRCALPHA)
        for layer in range(3):
            ls = glow_size + layer * 2
            la = 60 - layer * 15
            pygame.draw.circle(
                glow_surf, (255, 120, 120, max(0, la)),
                (glow_surf.get_width() // 2, glow_surf.get_height() // 2),
                GRID_SIZE // 2 + ls,
            )
        glow_surf.set_alpha(60)
        screen.blit(glow_surf, (x_pos - glow_size * 2, y_pos - glow_size * 2))
        screen.blit(self.apple_sprite, (x_pos, int(y_pos)))

        if self.sparkle_timer % 30 < 5:
            for _ in range(2):
                sx = x_pos + random.randint(5, GRID_SIZE - 5)
                sy = int(y_pos) + random.randint(5, GRID_SIZE - 5)
                pygame.draw.circle(screen, WHITE, (sx, sy), random.randint(1, 3))


# ===================================================================
# Start Menu
# ===================================================================


class StartMenu:
    """Clean start menu with speed selection."""

    SPEED_OPTIONS = [
        ("CHILL MODE", 2),
        ("CLASSIC", 4),
        ("FAST", 6),
        ("INSANE", 8),
        ("NIGHTMARE", 12),
    ]

    def __init__(self, screen):
        self.screen = screen
        self.selected_option = 1  # default CLASSIC
        self.options = self.SPEED_OPTIONS
        self.title_pulse = 0.0
        self.bg_hue_offset = 0.0
        self.stars = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT),
                       random.uniform(0.5, 2.0), random.randint(1, 3)) for _ in range(80)]
        self.title_font = pygame.font.Font(None, max(80, WINDOW_WIDTH // 14))
        self.menu_font = pygame.font.Font(None, max(44, WINDOW_WIDTH // 28))
        self.subtitle_font = pygame.font.Font(None, max(28, WINDOW_WIDTH // 45))
        self.hint_font = pygame.font.Font(None, max(24, WINDOW_WIDTH // 50))

    def draw_background(self):
        """Draw a smooth dark gradient background with subtle animated stars."""
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.bg_hue_offset += 0.15

        # Smooth vertical gradient (dark top to darker bottom)
        band_height = 8
        for y in range(0, sh, band_height):
            t = y / sh
            r = int(8 + 12 * (1 - t))
            g = int(10 + 18 * (1 - t))
            b = int(30 + 25 * (1 - t))
            # Add subtle hue shift
            hue_shift = math.sin(self.bg_hue_offset * 0.02 + t * 2) * 8
            r = max(0, min(255, r + int(hue_shift)))
            b = max(0, min(255, b + int(hue_shift * 0.5)))
            pygame.draw.rect(self.screen, (r, g, b), (0, y, sw, band_height))

        # Animated stars
        for i, (sx, sy, speed, size) in enumerate(self.stars):
            brightness = int(120 + 80 * math.sin(time.time() * speed + i))
            brightness = max(60, min(220, brightness))
            color = (brightness, brightness, brightness + 30)
            pygame.draw.circle(self.screen, color, (int(sx), int(sy)), size)

        # Subtle scan lines (very faint, every 3rd pixel)
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        for y in range(0, sh, 3):
            pygame.draw.line(overlay, (0, 0, 0, 15), (0, y), (sw, y), 1)
        self.screen.blit(overlay, (0, 0))

    def draw_title(self):
        """Draw the SNAKEIUM title with clean styling."""
        self.title_pulse += 0.06
        title = "SNAKEIUM"
        cw = max(65, WINDOW_WIDTH // 18)
        start_x = WINDOW_WIDTH // 2 - (len(title) * cw) // 2

        for i, ch in enumerate(title):
            hue = (time.time() * 30 + i * 45) % 360
            rgb = colorsys.hsv_to_rgb(hue / 360, 0.85, 1.0)
            color = tuple(int(c * 255) for c in rgb)
            cy = WINDOW_HEIGHT // 5 + int(4 * math.sin(self.title_pulse + i * 0.6))
            cx = start_x + i * cw

            # Dark shadow for depth
            shadow = self.title_font.render(ch, True, (0, 0, 0))
            self.screen.blit(shadow, (cx + 3, cy + 3))

            # Subtle glow
            glow_rgb = tuple(min(255, c + 60) for c in color)
            glow = self.title_font.render(ch, True, glow_rgb)
            glow.set_alpha(40)
            for ox, oy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
                self.screen.blit(glow, (cx + ox, cy + oy))

            # Main letter
            cs = self.title_font.render(ch, True, color)
            self.screen.blit(cs, (cx, cy))

        # Subtitle
        sub = "GHOSTKITTY EDITION"
        sub_surf = self.subtitle_font.render(sub, True, NEON_PINK)
        sub_rect = sub_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5 + 90))
        shadow = self.subtitle_font.render(sub, True, (0, 0, 0))
        self.screen.blit(shadow, (sub_rect.x + 1, sub_rect.y + 1))
        self.screen.blit(sub_surf, sub_rect)

    def draw_menu(self):
        """Draw the speed selection menu."""
        menu_top = WINDOW_HEIGHT // 2 - 20
        item_height = 55
        item_width = WINDOW_WIDTH // 3
        menu_x = WINDOW_WIDTH // 2 - item_width // 2

        for i, (name, _) in enumerate(self.options):
            y = menu_top + i * item_height
            rect = pygame.Rect(menu_x, y, item_width, item_height - 6)

            if i == self.selected_option:
                # Selected item: filled with border
                pygame.draw.rect(self.screen, (0, 40, 0), rect, border_radius=6)
                pygame.draw.rect(self.screen, NEON_GREEN, rect, 2, border_radius=6)
                color = NEON_GREEN
                text = "> " + name
            else:
                # Unselected: subtle background
                pygame.draw.rect(self.screen, (15, 15, 30), rect, border_radius=6)
                pygame.draw.rect(self.screen, (40, 40, 60), rect, 1, border_radius=6)
                color = (180, 180, 190)
                text = name

            surf = self.menu_font.render(text, True, color)
            text_rect = surf.get_rect(center=rect.center)
            shadow = self.menu_font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow, (text_rect.x + 1, text_rect.y + 1))
            self.screen.blit(surf, text_rect)

        # Controls hint
        inst = "ARROW KEYS TO SELECT  |  ENTER TO START  |  ESC TO QUIT"
        inst_surf = self.hint_font.render(inst, True, (80, 160, 200))
        self.screen.blit(inst_surf, inst_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60)))

    def draw(self):
        self.draw_background()
        self.draw_title()
        self.draw_menu()


# ===================================================================
# Main Game
# ===================================================================


class Game:
    """Top-level game controller."""

    def __init__(self, fullscreen=False, disable_music=False):
        self.disable_music = disable_music

        if fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF
            )
        pygame.display.set_caption("SNAKEIUM - GHOSTKITTY Edition")

        self.game_state = "menu"
        self.start_menu = StartMenu(self.screen)
        self.clock = pygame.time.Clock()
        self.target_fps = 60

        # Game objects
        self.snake: Optional[Snake] = None
        self.food: Optional[Food] = None
        self.powerups: list = []
        self.particles: list = []
        self.spirals: list = []
        self.pyramids: list = []
        self.triangles: list = []

        # State
        self.score = 0
        self.game_over = False
        self.paused = False
        self.selected_speed = 4
        self.speed_name = "CLASSIC"

        # HUD toggles
        self.show_grid = False
        self.show_fps = False

        # Death animation
        self._death_timer = 0
        self._screen_shake = 0.0

        # High scores
        self.high_scores = HighScoreManager()

        # Music
        self.music_manager: Optional[MusicManager] = None
        self.current_song_name: Optional[str] = None
        if not disable_music:
            try:
                self.music_manager = MusicManager(Config.DEFAULT_MUSIC_FOLDER or None)
                self.current_song_name = self.music_manager.play_random_song()
            except Exception:
                self.music_manager = None

        # Fonts
        font_size = max(36, WINDOW_WIDTH // 40)
        small_font_size = max(24, WINDOW_WIDTH // 60)
        self.font = pygame.font.Font(None, font_size)
        self.small_font = pygame.font.Font(None, small_font_size)

        # Background
        self.bg_hue = 0.0
        self.max_particles = Config.MAX_PARTICLES

    # ----- lifecycle -----

    def start_game(self, speed_setting, speed_name="CLASSIC"):
        self.game_state = "playing"
        self.selected_speed = speed_setting
        self.speed_name = speed_name
        self.snake = Snake(speed_setting)
        self.food = Food()
        self.powerups = []
        self.particles = []
        self.score = 0
        self.game_over = False
        self.paused = False
        self._death_timer = 0
        self._screen_shake = 0.0

        self.spirals = [
            SpiralEffect(
                (WINDOW_WIDTH // SPIRAL_COUNT) * i + (WINDOW_WIDTH // SPIRAL_COUNT) // 2,
                WINDOW_HEIGHT // 2 + random.randint(-200, 200),
                i,
            )
            for i in range(SPIRAL_COUNT)
        ]
        self.pyramids = [PyramidEffect(i) for i in range(PYRAMID_COUNT)]
        self.triangles = [TriangleRipper(i) for i in range(TRIANGLE_COUNT)]

    def reset_game(self):
        self.game_state = "menu"
        self.snake = None
        self.food = None
        self.powerups = []
        self.particles = []
        self.score = 0
        self.game_over = False
        self.paused = False

    # ----- spawning -----

    def spawn_powerup(self):
        if self.game_state != "playing" or not self.snake or not self.food:
            return
        if len(self.powerups) < 2 and random.random() < 0.003:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake.body and (x, y) != (self.food.x, self.food.y):
                self.powerups.append(PowerUp(x, y, random.choice(list(PowerUpType))))

    # ----- collision -----

    def check_food_collision(self):
        if self.game_state != "playing" or not self.snake or not self.food:
            return False
        head = self.snake.body[0]
        if head == (self.food.x, self.food.y):
            self.snake.eat_food()
            self.score += 10 * self.snake.score_multiplier
            for _ in range(15):
                vel = (random.uniform(-4, 4), random.uniform(-4, 4))
                c = random.choice([(220, 20, 60), (255, 0, 0), (255, 69, 0)])
                self.particles.append(
                    Particle(
                        self.food.x * GRID_SIZE + GRID_SIZE // 2,
                        self.food.y * GRID_SIZE + GRID_SIZE // 2,
                        c, vel,
                    )
                )
            self.food = Food()
            return True
        return False

    def check_powerup_collisions(self):
        if self.game_state != "playing" or not self.snake:
            return
        head = self.snake.body[0]
        for pu in self.powerups[:]:
            if head == (pu.x, pu.y):
                self.snake.eat_powerup(pu)
                pcolors = {
                    PowerUpType.SPEED_BOOST: NEON_BLUE,
                    PowerUpType.SCORE_MULTIPLIER: NEON_YELLOW,
                    PowerUpType.RAINBOW_MODE: NEON_PURPLE,
                    PowerUpType.MEGA_FOOD: NEON_ORANGE,
                }
                for _ in range(15):
                    vel = (random.uniform(-4, 4), random.uniform(-4, 4))
                    self.particles.append(
                        Particle(
                            pu.x * GRID_SIZE + GRID_SIZE // 2,
                            pu.y * GRID_SIZE + GRID_SIZE // 2,
                            pcolors[pu.type], vel, 120,
                        )
                    )
                self.powerups.remove(pu)

    # ----- drawing helpers -----

    def draw_rainbow_background(self):
        self.bg_hue = (self.bg_hue + 0.3) % 360
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        base_rgb = colorsys.hsv_to_rgb(self.bg_hue / 360, 0.25, 0.12)
        self.screen.fill(tuple(int(c * 255) for c in base_rgb))

        if PIXELATED_BACKGROUND:
            # Subtle gradient bands instead of rainbow blocks
            band_height = 12
            for y in range(0, sh, band_height):
                t = y / sh
                hue = (self.bg_hue + t * 40) % 360
                rgb = colorsys.hsv_to_rgb(hue / 360, 0.2, 0.10 + 0.06 * (1 - t))
                color = tuple(int(c * 255) for c in rgb)
                pygame.draw.rect(self.screen, color, (0, y, sw, band_height))

    def draw_grid_overlay(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y), 1)

    def draw_ui(self):
        if self.game_state != "playing" or not self.snake:
            return
        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        self.screen.blit(self.font.render(f"Length: {len(self.snake.body)}", True, WHITE), (10, 50))
        self.screen.blit(self.font.render(f"Speed: {int(self.snake.get_current_speed())}", True, WHITE), (10, 90))

        best = self.high_scores.get_best(self.speed_name)
        if best > 0:
            self.screen.blit(self.small_font.render(f"Best: {best}", True, NEON_YELLOW), (10, 130))

        if self.current_song_name:
            self.screen.blit(self.small_font.render(self.current_song_name, True, NEON_PINK), (10, WINDOW_HEIGHT - 30))

        y_off = 160
        if self.snake.speed_boost_timer > 0:
            self.screen.blit(self.small_font.render("SPEED BOOST!", True, NEON_BLUE), (10, y_off))
            y_off += 25
        if self.snake.score_multiplier > 1:
            self.screen.blit(self.small_font.render(f"{self.snake.score_multiplier}x SCORE!", True, NEON_YELLOW), (10, y_off))
            y_off += 25
        if self.snake.rainbow_mode:
            self.screen.blit(self.small_font.render("RAINBOW MODE!", True, NEON_PURPLE), (10, y_off))

    def draw_fps_counter(self):
        fps = int(self.clock.get_fps())
        self.screen.blit(self.small_font.render(f"FPS: {fps}", True, NEON_GREEN), (WINDOW_WIDTH - 120, 10))

    def draw_pause_screen(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        pt = self.font.render("PAUSED", True, NEON_BLUE)
        ct = self.small_font.render("Press SPACE to continue", True, WHITE)
        self.screen.blit(pt, pt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))
        self.screen.blit(ct, ct.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)))

    def draw_game_over_screen(self):
        if self._death_timer < 20:
            self._death_timer += 1
            self._screen_shake = max(0.0, (20 - self._death_timer) * 0.5)

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        go = self.font.render("GAME OVER", True, NEON_PINK)
        sc = self.font.render(f"Final Score: {self.score}", True, WHITE)
        best = self.high_scores.get_best(self.speed_name)
        if self.score >= best and self.score > 0:
            bl = self.small_font.render("NEW HIGH SCORE!", True, NEON_YELLOW)
        else:
            bl = self.small_font.render(f"Best: {best}", True, NEON_YELLOW)
        rt = self.small_font.render("Press R to return to menu  |  ESC to quit", True, WHITE)

        self.screen.blit(go, go.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)))
        self.screen.blit(sc, sc.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))
        self.screen.blit(bl, bl.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)))
        self.screen.blit(rt, rt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90)))

    # ----- event handling -----

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Global toggles
                if event.key == pygame.K_F2:
                    self.show_grid = not self.show_grid
                    continue
                if event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                    continue

                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "menu"
                    else:
                        return False

                elif self.game_state == "menu":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.start_menu.selected_option = (self.start_menu.selected_option - 1) % len(self.start_menu.options)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.start_menu.selected_option = (self.start_menu.selected_option + 1) % len(self.start_menu.options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        name, spd = self.start_menu.options[self.start_menu.selected_option]
                        self.start_game(spd, name)

                elif self.game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_m and self.music_manager:
                        self.current_song_name = self.music_manager.play_random_song()
                    elif not self.game_over and not self.paused and self.snake:
                        if event.key in (pygame.K_UP, pygame.K_w):
                            self.snake.change_direction(Direction.UP)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.snake.change_direction(Direction.DOWN)
                        elif event.key in (pygame.K_LEFT, pygame.K_a):
                            self.snake.change_direction(Direction.LEFT)
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.snake.change_direction(Direction.RIGHT)

                elif self.game_state == "game_over":
                    if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                        self.game_state = "menu"

        return True

    # ----- update -----

    def update(self):
        for s in self.spirals:
            s.update()
        for p in self.pyramids:
            p.update()
        for t in self.triangles:
            t.update()

        if self.game_state != "playing" or not self.snake or not self.food:
            return
        if self.game_over or self.paused:
            return

        self.snake.update_effects()
        self.snake.update_move_interval()
        self.snake.move()

        if self.snake.check_collision():
            self.game_over = True
            self.game_state = "game_over"
            self._death_timer = 0
            self._screen_shake = 10.0
            self.high_scores.add_score(self.speed_name, self.score, len(self.snake.body))

        self.check_food_collision()
        self.check_powerup_collisions()
        self.food.update()
        self.spawn_powerup()

        for pu in self.powerups[:]:
            pu.update()
            if pu.is_expired():
                self.powerups.remove(pu)

        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]

        if self.music_manager:
            new = self.music_manager.check_music()
            if new:
                self.current_song_name = new

    # ----- draw -----

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_rainbow_background()

        shake_x, shake_y = 0, 0
        if self._screen_shake > 0.5:
            shake_x = int(random.uniform(-self._screen_shake, self._screen_shake))
            shake_y = int(random.uniform(-self._screen_shake, self._screen_shake))
            self._screen_shake *= 0.85

        try:
            for pyramid in self.pyramids[:3]:
                pyramid.draw(self.screen)
            for triangle in self.triangles[:3]:
                triangle.draw(self.screen)
        except Exception:
            pass

        if self.game_state == "menu":
            self.start_menu.draw()

        elif self.game_state == "playing" and self.snake and self.food:
            if self.show_grid:
                self.draw_grid_overlay()
            try:
                self.food.draw(self.screen)
                for pu in self.powerups:
                    pu.draw(self.screen)
                self.snake.draw(self.screen, self.particles)
                for particle in self.particles:
                    particle.draw(self.screen)
            except Exception:
                pygame.draw.rect(
                    self.screen, NEON_GREEN,
                    (self.snake.body[0][0] * GRID_SIZE, self.snake.body[0][1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )
                pygame.draw.rect(
                    self.screen, NEON_PINK,
                    (self.food.x * GRID_SIZE, self.food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )
            self.draw_ui()
            if self.paused:
                self.draw_pause_screen()

        elif self.game_state == "game_over":
            self.draw_game_over_screen()

        if self.show_fps:
            self.draw_fps_counter()

        if shake_x or shake_y:
            shifted = self.screen.copy()
            self.screen.fill(BLACK)
            self.screen.blit(shifted, (shake_x, shake_y))

    # ----- main loop -----

    def run(self):
        print("=" * 50)
        print("SNAKEIUM - GHOSTKITTY Edition")
        print("=" * 50)
        print()
        print("Controls:")
        print("  Arrow Keys / WASD  - Move snake")
        print("  SPACE              - Pause game")
        print("  M                  - Skip to next track")
        print("  R                  - Restart (game over)")
        print("  ESC                - Menu / Quit")
        print("  F2                 - Toggle grid overlay")
        print("  F3                 - Toggle FPS counter")
        print()
        print("Speed Settings:")
        print("  CHILL MODE   - Relaxed gameplay")
        print("  CLASSIC      - Traditional Snake")
        print("  FAST         - Quick-paced action")
        print("  INSANE       - High-speed challenge")
        print("  NIGHTMARE    - Ultimate test")
        print()
        print(f"Running at {self.target_fps} FPS")
        print("=" * 50)

        running = True
        try:
            while running:
                try:
                    running = self.handle_events()
                except Exception:
                    continue
                try:
                    self.update()
                except Exception:
                    continue
                try:
                    self.draw()
                except Exception:
                    self.screen.fill((20, 20, 40))
                try:
                    pygame.display.flip()
                except Exception:
                    pass
                self.clock.tick(self.target_fps)
        except KeyboardInterrupt:
            pass
        finally:
            pygame.quit()


# ===================================================================
# CLI entry point
# ===================================================================


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        description="SNAKEIUM - Modern 8-bit Snake Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python snakeium.py --music-folder ~/Music
  python snakeium.py --no-effects --fps 60
  python snakeium.py --windowed --resolution 1280x720
        """,
    )
    parser.add_argument("--version", action="version", version=f"SNAKEIUM {__version__}")
    parser.add_argument("--music-folder", type=str, help="Path to music folder")
    parser.add_argument("--no-music", action="store_true", help="Disable background music")
    parser.add_argument("--no-effects", action="store_true", help="Disable geometric effects")
    parser.add_argument("--no-particles", action="store_true", help="Disable particle effects")
    parser.add_argument("--fps", type=int, default=60, help="Target FPS (default: 60)")
    parser.add_argument("--windowed", action="store_true", help="Force windowed mode (default)")
    parser.add_argument("--fullscreen", action="store_true", help="Enable fullscreen mode")
    parser.add_argument("--resolution", type=str, help="Window resolution (e.g. 1920x1080)")
    parser.add_argument("--volume", type=float, default=0.3, help="Music volume 0.0-1.0")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--test-mode", action="store_true", help="CI/CD test mode (headless)")
    return parser.parse_args()


def main():
    args = parse_arguments()

    # CI/CD test mode
    if args.test_mode:
        print("Starting test mode...")
        try:
            test_snake = Snake(4)
            test_food = Food()
            test_snake.change_direction(Direction.RIGHT)
            test_snake._start_new_move()
            hsm = HighScoreManager()
            hsm.add_score("TEST", 100, 5)
            assert hsm.get_best("TEST") == 100
            print("All tests passed.")
            sys.exit(0)
        except Exception as e:
            print(f"Test failed: {e}")
            sys.exit(1)

    # Apply CLI overrides
    if args.fps:
        Config.TARGET_FPS = args.fps
    if args.volume is not None:
        Config.MUSIC_VOLUME = max(0.0, min(1.0, args.volume))
    if args.music_folder:
        Config.DEFAULT_MUSIC_FOLDER = args.music_folder
    if args.no_effects:
        Config.ENABLE_GEOMETRIC_EFFECTS = False
    if args.no_particles:
        Config.ENABLE_PARTICLES = False

    if args.resolution:
        try:
            w, h = map(int, args.resolution.split("x"))
            globals()["WINDOW_WIDTH"] = w
            globals()["WINDOW_HEIGHT"] = h
            Config.GRID_WIDTH = w // Config.GRID_SIZE
            Config.GRID_HEIGHT = h // Config.GRID_SIZE
        except ValueError:
            print("Invalid resolution format. Use WIDTHxHEIGHT (e.g. 1920x1080)")
            sys.exit(1)

    try:
        use_fullscreen = args.fullscreen and not args.windowed
        game = Game(fullscreen=use_fullscreen, disable_music=args.no_music)
        game.run()
    except KeyboardInterrupt:
        print("\nThanks for playing SNAKEIUM!")
    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
