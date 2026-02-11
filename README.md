# SNAKEIUM 2.1 - GHOSTKITTY Edition

**A Modern Retro Snake Game**

[![Version](https://img.shields.io/badge/Version-2.1.0-brightgreen.svg)](https://github.com/chousemp3/SNAKEIUM/releases)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)

A fully featured Snake game built with Python and Pygame. Features modular architecture, multiple game modes, visual effects, configurable themes, high score tracking, and GHOSTKITTY soundtrack integration.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/chousemp3/SNAKEIUM.git
cd SNAKEIUM

# Install dependencies
pip install -r requirements.txt

# Run the game
python snakeium.py
```

Or use the entry point:

```bash
python main.py            # Enhanced modular version
python main.py --legacy   # Legacy standalone version
```

## Features

### Gameplay
- **Five game modes**: Classic, Time Attack, Survival, Maze, Challenge
- **Eight power-ups**: Speed boost, score multiplier, rainbow mode, mega food, shield, slow time, double score, and teleport
- **Three food types**: Normal, golden, and mega with different point values
- **Progressive difficulty**: Speed scales with score and snake length
- **Input buffering**: Queues up to 2 direction changes for responsive controls
- **High score persistence**: Scores saved to `~/.snakeium/high_scores.json`

### Visuals
- **Multiple themes**: GHOSTKITTY, Neon, Retro, Minimal, Custom
- **Particle effects**: Trails, explosions, and rainbow particle systems
- **Animated backgrounds**: Gradient shifts, geometric shapes, scan lines
- **HUD overlay**: Live score, best score, active power-ups, song info
- **Debug overlays**: F2 for grid, F3 for FPS counter
- **Death animation**: Screen shake effect on game over

### Audio
- **Music support**: Plays MP3, OGG, and WAV files from the local `music/` folder
- **Metadata display**: Shows artist, title, and album via mutagen
- **Playback controls**: Shuffle, skip (M key), volume adjustment
- **Procedural SFX**: Dynamically generated sound effects for game events

### Configuration
- **JSON-based settings**: Saved to `~/.snakeium/config.json`
- **Display**: Resolution, fullscreen, VSync, target FPS
- **Gameplay**: Speed, wrap-around, power-ups, particle limits
- **Audio**: Music/SFX volume, music folder, shuffle mode
- **Controls**: Fully remappable key bindings
- **Themes**: Built-in themes or custom color schemes via JSON

## Controls

| Action         | Keys              |
|----------------|-------------------|
| Movement       | Arrow keys / WASD |
| Pause          | Space             |
| Menu / Back    | Escape            |
| Restart        | R                 |
| Skip Track     | M                 |
| Fullscreen     | F11               |
| Grid Overlay   | F2                |
| FPS Counter    | F3                |
| Debug Info     | F1                |

## Command Line Options

```
python main.py [OPTIONS]

  --legacy          Run the original standalone version
  --fullscreen      Start in fullscreen mode
  --no-music        Disable background music
  --config FILE     Use a custom configuration file
  --debug           Enable debug mode
  --version         Show version information
  --help            Show help message
```

## Project Structure

```
SNAKEIUM/
  main.py                   Entry point (modular or legacy)
  snakeium.py               Standalone game (full-featured)
  setup.py                  Package installation
  install.py                Automated setup script
  requirements.txt          Dependencies
  config/
    default.json            Default settings
    themes/                 Theme definitions (JSON)
  src/snakeium/             Modular package (2.1)
    __init__.py
    game_engine.py          Core game logic
    config_manager.py       Settings and persistence
    audio_manager.py        Music and sound effects
    ui_manager.py           Menus and rendering
  legacy/                   Original version (1.0)
  tests/                    Test suite
  docs/                     Additional documentation
  assets/                   Game assets
```

## Development

```bash
# Install in development mode
pip install -e .[dev]

# Run tests
pytest tests/ -v

# Format code
black src/ tests/

# Type checking
mypy src/
```

### Requirements

- Python 3.8 or higher
- pygame 2.5.0+
- numpy 1.24.0+ (optional, for enhanced visuals)
- mutagen 1.47.0+ (optional, for music metadata)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues, feature requests, and pull requests.

## Version History

- **2.1.0** - High score system, input buffering, F2/F3 overlays, death animation, project cleanup
- **2.0.0** - Complete rewrite with modular architecture, multiple game modes, theme system
- **1.0.0** - Original release with core gameplay, music integration, and visual effects

See [CHANGELOG.md](CHANGELOG.md) for full details.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Credits

- **GHOSTKITTY** - Music collection
- **Pygame** - Game development framework
- **GHOSTKITTY APPS** - Development

---

[Issues](https://github.com/chousemp3/SNAKEIUM/issues) | [Discussions](https://github.com/chousemp3/SNAKEIUM/discussions) | [Releases](https://github.com/chousemp3/SNAKEIUM/releases)
