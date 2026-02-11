# Changelog

All notable changes to SNAKEIUM will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-02-10

### Added
- High score system with JSON persistence (`~/.snakeium/high_scores.json`)
- Input buffering: queues up to 2 direction changes for responsive controls
- F2 toggle for grid overlay
- F3 toggle for FPS counter
- Death animation with screen shake effect
- "NEW HIGH SCORE" notification on game over screen
- Best score display during gameplay
- Default menu selection set to CLASSIC instead of CHILL

### Fixed
- Duplicate `pygame.quit()` call causing shutdown errors
- Duplicate `import os` statement
- Config values immediately overridden by legacy constants
- Hardcoded music path replaced with configurable empty default
- Window size inconsistency (standardized to 1400x900)
- Comments referencing "120Hz" corrected to "60 FPS"
- Double update of visual effects each frame causing performance waste
- Broken emoji characters in print output
- Menu background replaced: removed rainbow block grid in favor of smooth dark gradient with animated stars
- Scan line overlay reduced from heavy alpha to subtle alpha 15
- In-game background cleaned up: replaced pixelated rainbow blocks with smooth gradient bands
- Geometric visual effects (flying triangles, spirals) disabled to prevent gameplay obstruction
- Music scanner restricted to local `music/` folder only (no longer scans system directories)
- Snake movement pre-loaded on game start for immediate input response

### Changed
- Full rewrite of standalone `snakeium.py` (1852 lines reduced to ~1100 clean lines)
- Version bumped across all modules to 2.1.0
- All print output uses plain text (no emoji characters)

### Removed
- Redundant files: `setup_backup.py`, `setup_broken.py`, `add_screenshot.sh`, `screenshot_helper.sh`
- Duplicate documentation: `GITHUB_UPLOAD.md`, `README_v1.md`, `DEVELOPMENT.md`, `PERFORMANCE.md`, `QUICKSTART.md`
- Superseded test scripts: `windows_test.py`, `ci_test.py`
- Duplicate `mutagen` entry in requirements.txt

---

## [2.0.0] - 2025-08-21

### Added
- Modular architecture: `game_engine.py`, `config_manager.py`, `audio_manager.py`, `ui_manager.py`
- Multiple game modes: Classic, Time Attack, Survival, Maze, Challenge
- Comprehensive configuration system with JSON persistence
- Theme system: GHOSTKITTY, Neon, Retro, Minimal, Custom
- Enhanced power-up system with 8 power-up types
- Procedural sound effect generation
- Statistics tracking and achievement framework
- Mouse support for menus and settings
- `main.py` entry point with `--legacy` flag

### Changed
- Project restructured into `src/snakeium/` package
- Setup script updated for package distribution
- CI workflow expanded for Python 3.8-3.11

---

## [1.0.0] - 2025-08-21

### Added
- Core Snake gameplay with 60 FPS movement
- Five speed settings: Chill, Classic, Fast, Insane, Nightmare
- GHOSTKITTY music system with auto-detection and metadata display
- Power-up system: speed boost, score multiplier, rainbow mode, mega food
- Animated backgrounds with rainbow gradients and geometric effects
- Particle effects for food collection
- Scan line overlay for retro CRT aesthetic
- Pause and restart functionality
- Cross-platform support: Windows, macOS, Linux
- Command-line arguments for music folder, resolution, volume, and debug mode
