"""
🐍 SNAKEIUM - GHOSTKITTY Edition 🎵
=================================

A modern retro Snake game with stunning 8-bit visuals, rainbow effects, and epic GHOSTKITTY music.

Version: 2.0.0
Author: GHOSTKITTY APPS
License: MIT
"""

__version__ = "2.0.0"
__author__ = "GHOSTKITTY APPS"
__license__ = "MIT"

from .game_engine import Game
from .config_manager import ConfigManager
from .audio_manager import AudioManager
from .ui_manager import UIManager

__all__ = ['Game', 'ConfigManager', 'AudioManager', 'UIManager']
