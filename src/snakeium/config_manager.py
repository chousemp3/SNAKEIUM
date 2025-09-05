"""
Configuration Manager for SNAKEIUM
Handles all game settings, user preferences, and configuration persistence.
"""

import json
import os
import pygame
from pathlib import Path
from typing import Dict, Any, Tuple, List
from dataclasses import dataclass, asdict
from enum import Enum


class GameMode(Enum):
    CLASSIC = "classic"
    TIME_ATTACK = "time_attack"
    SURVIVAL = "survival"
    MAZE = "maze"
    CHALLENGE = "challenge"


class Theme(Enum):
    GHOSTKITTY = "ghostkitty"
    NEON = "neon"
    RETRO = "retro"
    MINIMAL = "minimal"
    CUSTOM = "custom"


@dataclass
class DisplaySettings:
    width: int = 1400
    height: int = 900
    fullscreen: bool = False
    vsync: bool = True
    target_fps: int = 60
    show_fps: bool = False


@dataclass
class GameplaySettings:
    default_speed: int = 4
    wrap_around: bool = True
    power_ups_enabled: bool = True
    particle_effects: bool = True
    visual_effects: bool = True
    max_particles: int = 300


@dataclass
class AudioSettings:
    music_enabled: bool = True
    sound_effects_enabled: bool = True
    music_volume: float = 0.7
    sfx_volume: float = 0.8
    music_folder: str = ""
    shuffle_music: bool = True


@dataclass
class ControlSettings:
    up_keys: List[int] = None
    down_keys: List[int] = None
    left_keys: List[int] = None
    right_keys: List[int] = None
    pause_key: int = pygame.K_SPACE
    restart_key: int = pygame.K_r
    menu_key: int = pygame.K_ESCAPE
    skip_music_key: int = pygame.K_m
    
    def __post_init__(self):
        if self.up_keys is None:
            self.up_keys = [pygame.K_UP, pygame.K_w]
        if self.down_keys is None:
            self.down_keys = [pygame.K_DOWN, pygame.K_s]
        if self.left_keys is None:
            self.left_keys = [pygame.K_LEFT, pygame.K_a]
        if self.right_keys is None:
            self.right_keys = [pygame.K_RIGHT, pygame.K_d]


@dataclass
class ThemeSettings:
    current_theme: Theme = Theme.GHOSTKITTY
    custom_colors: Dict[str, Tuple[int, int, int]] = None
    rainbow_background: bool = True
    scan_lines: bool = True
    
    def __post_init__(self):
        if self.custom_colors is None:
            self.custom_colors = {}


@dataclass
class DeveloperSettings:
    debug_mode: bool = False
    show_collision_boxes: bool = False
    performance_monitor: bool = False
    log_level: str = "INFO"


class ConfigManager:
    """Manages all game configuration and settings."""
    
    DEFAULT_CONFIG_PATH = Path.home() / ".snakeium" / "config.json"
    
    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATH
        
        # Initialize default settings
        self.display = DisplaySettings()
        self.gameplay = GameplaySettings()
        self.audio = AudioSettings()
        self.controls = ControlSettings()
        self.theme = ThemeSettings()
        self.developer = DeveloperSettings()
        
        # High scores and statistics
        self.high_scores = {}
        self.statistics = {
            "total_games": 0,
            "total_playtime": 0,
            "highest_score": 0,
            "longest_snake": 0,
            "favorite_speed": 4,
            "power_ups_collected": 0,
            "achievements": []
        }
        
        # Load existing configuration
        self.load_config()
    
    def load_config(self) -> bool:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load each section
                if 'display' in data:
                    self.display = DisplaySettings(**data['display'])
                if 'gameplay' in data:
                    self.gameplay = GameplaySettings(**data['gameplay'])
                if 'audio' in data:
                    self.audio = AudioSettings(**data['audio'])
                if 'controls' in data:
                    self.controls = ControlSettings(**data['controls'])
                if 'theme' in data:
                    theme_data = data['theme'].copy()
                    if 'current_theme' in theme_data:
                        theme_data['current_theme'] = Theme(theme_data['current_theme'])
                    self.theme = ThemeSettings(**theme_data)
                if 'developer' in data:
                    self.developer = DeveloperSettings(**data['developer'])
                if 'high_scores' in data:
                    self.high_scores = data['high_scores']
                if 'statistics' in data:
                    self.statistics.update(data['statistics'])
                
                print(f"✅ Configuration loaded from {self.config_path}")
                return True
                
        except Exception as e:
            print(f"⚠️  Failed to load config: {e}")
            print("🔧 Using default configuration")
        
        return False
    
    def save_config(self) -> bool:
        """Save configuration to file."""
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for serialization
            config_data = {
                'display': asdict(self.display),
                'gameplay': asdict(self.gameplay),
                'audio': asdict(self.audio),
                'controls': asdict(self.controls),
                'theme': asdict(self.theme),
                'developer': asdict(self.developer),
                'high_scores': self.high_scores,
                'statistics': self.statistics
            }
            
            # Convert enum to string
            config_data['theme']['current_theme'] = self.theme.current_theme.value
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.display = DisplaySettings()
        self.gameplay = GameplaySettings()
        self.audio = AudioSettings()
        self.controls = ControlSettings()
        self.theme = ThemeSettings()
        self.developer = DeveloperSettings()
        print("🔄 Configuration reset to defaults")
    
    def update_high_score(self, mode: str, score: int) -> bool:
        """Update high score for a game mode."""
        if mode not in self.high_scores:
            self.high_scores[mode] = []
        
        # Add score and keep top 10
        self.high_scores[mode].append(score)
        self.high_scores[mode].sort(reverse=True)
        self.high_scores[mode] = self.high_scores[mode][:10]
        
        # Update statistics
        if score > self.statistics['highest_score']:
            self.statistics['highest_score'] = score
            return True  # New personal best!
        
        return False
    
    def get_high_scores(self, mode: str, limit: int = 10) -> List[int]:
        """Get high scores for a game mode."""
        return self.high_scores.get(mode, [])[:limit]
    
    def update_statistics(self, **kwargs):
        """Update game statistics."""
        for key, value in kwargs.items():
            if key in self.statistics:
                if key == "total_playtime":
                    self.statistics[key] += value
                elif key == "total_games":
                    self.statistics[key] += 1
                elif key in ["longest_snake", "power_ups_collected"]:
                    self.statistics[key] += value
                else:
                    self.statistics[key] = value
    
    def get_display_mode(self) -> Tuple[int, int, int]:
        """Get pygame display mode flags."""
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        
        if self.display.fullscreen:
            flags |= pygame.FULLSCREEN
        if self.display.vsync:
            flags |= pygame.SCALED
            
        return self.display.width, self.display.height, flags
    
    def get_theme_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Get color scheme for current theme."""
        themes = {
            Theme.GHOSTKITTY: {
                'background': (0, 0, 0),
                'snake': (0, 255, 0),
                'food': (255, 0, 0),
                'ui_text': (255, 255, 255),
                'neon_blue': (0, 191, 255),
                'neon_pink': (255, 20, 147),
                'neon_green': (50, 205, 50),
                'neon_yellow': (255, 255, 0),
                'neon_purple': (138, 43, 226),
                'neon_orange': (255, 140, 0)
            },
            Theme.NEON: {
                'background': (10, 10, 30),
                'snake': (0, 255, 255),
                'food': (255, 0, 255),
                'ui_text': (255, 255, 255),
                'neon_blue': (0, 255, 255),
                'neon_pink': (255, 0, 255),
                'neon_green': (0, 255, 0),
                'neon_yellow': (255, 255, 0),
                'neon_purple': (128, 0, 255),
                'neon_orange': (255, 128, 0)
            },
            Theme.RETRO: {
                'background': (64, 128, 64),
                'snake': (255, 255, 255),
                'food': (255, 255, 0),
                'ui_text': (255, 255, 255),
                'neon_blue': (128, 128, 255),
                'neon_pink': (255, 128, 128),
                'neon_green': (128, 255, 128),
                'neon_yellow': (255, 255, 128),
                'neon_purple': (255, 128, 255),
                'neon_orange': (255, 192, 128)
            },
            Theme.MINIMAL: {
                'background': (32, 32, 32),
                'snake': (200, 200, 200),
                'food': (150, 150, 150),
                'ui_text': (255, 255, 255),
                'neon_blue': (100, 100, 150),
                'neon_pink': (150, 100, 150),
                'neon_green': (100, 150, 100),
                'neon_yellow': (150, 150, 100),
                'neon_purple': (128, 100, 150),
                'neon_orange': (150, 125, 100)
            }
        }
        
        if self.theme.current_theme == Theme.CUSTOM:
            return self.theme.custom_colors
        
        return themes.get(self.theme.current_theme, themes[Theme.GHOSTKITTY])
    
    def export_config(self, path: str) -> bool:
        """Export configuration to a specific file."""
        try:
            old_path = self.config_path
            self.config_path = Path(path)
            result = self.save_config()
            self.config_path = old_path
            return result
        except Exception as e:
            print(f"❌ Failed to export config: {e}")
            return False
    
    def import_config(self, path: str) -> bool:
        """Import configuration from a specific file."""
        try:
            old_path = self.config_path
            self.config_path = Path(path)
            result = self.load_config()
            self.config_path = old_path
            return result
        except Exception as e:
            print(f"❌ Failed to import config: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get configuration value using dot notation."""
        try:
            keys = key.split('.')
            
            # Get the main section
            if keys[0] == 'app':
                if keys[1] == 'version':
                    return "2.0.0"
                elif keys[1] == 'name':
                    return "SNAKEIUM"
            elif keys[0] == 'display':
                return getattr(self.display, keys[1], default)
            elif keys[0] == 'gameplay':
                return getattr(self.gameplay, keys[1], default)
            elif keys[0] == 'audio':
                return getattr(self.audio, keys[1], default)
            elif keys[0] == 'controls':
                return getattr(self.controls, keys[1], default)
            elif keys[0] == 'theme':
                return getattr(self.theme, keys[1], default)
            elif keys[0] == 'developer':
                return getattr(self.developer, keys[1], default)
            elif keys[0] == 'statistics':
                return self.statistics.get(keys[1], default)
            else:
                return default
        except (AttributeError, IndexError):
            return default
    
    def set(self, key: str, value):
        """Set configuration value using dot notation."""
        try:
            keys = key.split('.')
            
            # Set the value in the appropriate section
            if keys[0] == 'display':
                setattr(self.display, keys[1], value)
            elif keys[0] == 'gameplay':
                setattr(self.gameplay, keys[1], value)
            elif keys[0] == 'audio':
                setattr(self.audio, keys[1], value)
            elif keys[0] == 'controls':
                setattr(self.controls, keys[1], value)
            elif keys[0] == 'theme':
                setattr(self.theme, keys[1], value)
            elif keys[0] == 'developer':
                setattr(self.developer, keys[1], value)
            elif keys[0] == 'statistics':
                self.statistics[keys[1]] = value
                
        except (AttributeError, IndexError) as e:
            print(f"⚠️ Failed to set {key} = {value}: {e}")
