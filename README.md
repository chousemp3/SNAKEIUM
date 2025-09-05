# 🐍 SNAKEIUM 2.0 - GHOSTKITTY Edition 🎵

**The Ultimate Modern Retro Snake Game Experience**

[![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen.svg)](https://github.com/chousemp3/SNAKEIUM/releases)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)

A completely rewritten and enhanced Snake game featuring modular architecture, advanced visual effects, multiple game modes, comprehensive configuration system, and an epic GHOSTKITTY soundtrack.

![SNAKEIUM Demo](assets/demo.gif)

## 🌟 What's New in 2.0

### 🏗️ **Complete Architectural Overhaul**
- **Modular Design**: Clean separation of concerns with dedicated managers
- **Configuration System**: Comprehensive settings with JSON persistence
- **Enhanced Audio Engine**: Advanced music and sound effect management
- **Improved UI Framework**: Modern menu system with mouse and keyboard support

### 🎮 **Advanced Gameplay Features**
- **Multiple Game Modes**: Classic, Time Attack, Survival, Maze, and Challenge modes
- **Enhanced Power-up System**: 8 different power-ups with unique effects
- **Smart Food Types**: Normal, Golden, and Mega food with different values
- **Progressive Difficulty**: Intelligent speed scaling and challenge progression

### 🎨 **Visual & Audio Enhancements**
- **Multiple Themes**: GHOSTKITTY, Neon, Retro, Minimal, and Custom themes
- **Advanced Particle Systems**: Enhanced visual effects with trails and explosions
- **Procedural Sound Effects**: Dynamically generated audio feedback
- **High Score System**: Persistent leaderboards with statistics tracking

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/chousemp3/SNAKEIUM.git
cd SNAKEIUM

# Install dependencies
pip install -r requirements.txt

# Run SNAKEIUM 2.0
python main.py

# Or run legacy version
python main.py --legacy
```

### Alternative Installation Methods

```bash
# Install as package (development mode)
pip install -e .

# Then run from anywhere
snakeium

# Or with specific options
snakeium --fullscreen --no-music
```

## 🎮 Game Modes

### 🎯 **Classic Mode**
The traditional Snake experience with modern enhancements. Eat food, grow longer, avoid collisions, and achieve the highest score possible.

### ⏱️ **Time Attack**
Race against the clock! Survive for as long as possible within a time limit while collecting bonus points for speed and efficiency.

### 🛡️ **Survival Mode**
The playfield gradually shrinks over time. Adapt your strategy and survive in an ever-decreasing space with increasing difficulty.

### 🌟 **Maze Mode**
Navigate through procedurally generated mazes with obstacles and barriers. Find the optimal path while avoiding dead ends.

### 🏆 **Challenge Mode**
Complete specific objectives and achievements. Perfect for players who want structured goals and progression rewards.

## ⚡ Power-ups System

| Power-up | Effect | Duration | Description |
|----------|--------|----------|-------------|
| ⚡ **Speed Boost** | +100% speed | 5 seconds | Move twice as fast |
| 💎 **Score Multiplier** | 3x points | 10 seconds | Triple your score gains |
| 🌈 **Rainbow Mode** | Visual effects | 15 seconds | Psychedelic snake with particles |
| 🍎 **Mega Food** | Instant growth | N/A | Grow by 5 segments immediately |
| 🛡️ **Shield** | Collision immunity | 10 seconds | Pass through your own body |
| ⏰ **Slow Time** | 50% game speed | 8 seconds | Slow motion gameplay |
| 💰 **Double Score** | 2x base points | 7.5 seconds | Double all score gains |
| 🌀 **Teleport** | Random position | N/A | Instantly move to safe location |

## 🎵 Enhanced Audio System

### 🎶 **Dynamic Music Management**
- **Auto-Detection**: Automatically finds music in common folders
- **Metadata Support**: Displays song information with artist and title
- **Multiple Formats**: Support for MP3, OGG, and WAV files
- **Smart Playback**: Shuffle and sequential modes with fade transitions

### 🔊 **Procedural Sound Effects**
- **Dynamic Generation**: Real-time audio synthesis for game events
- **Contextual Audio**: Different sounds for different power-ups and actions
- **Volume Control**: Separate controls for music and sound effects
- **Performance Optimized**: Efficient audio processing with minimal latency

## ⚙️ Configuration System

### 📁 **Configuration Files**
Settings are automatically saved to `~/.snakeium/config.json` with the following categories:

- **Display Settings**: Resolution, fullscreen, FPS, themes
- **Gameplay Settings**: Speed, power-ups, particle effects
- **Audio Settings**: Music/SFX volume, folders, playback mode
- **Control Settings**: Customizable key bindings for all actions
- **Developer Settings**: Debug mode, performance monitoring

### 🎨 **Theme System**
Choose from multiple built-in themes or create your own:
- **GHOSTKITTY**: Original neon rainbow aesthetic
- **Neon**: Bright cyberpunk colors
- **Retro**: Classic green-on-black terminal style
- **Minimal**: Clean, modern interface
- **Custom**: Define your own color schemes

## 🏆 Statistics & High Scores

### 📊 **Comprehensive Tracking**
- **High Score Leaderboards**: Top 10 scores per game mode
- **Detailed Statistics**: Play time, games played, longest snake, power-ups collected
- **Achievement System**: Unlockable achievements for various milestones
- **Performance Metrics**: Average score, improvement trends, favorite game modes

## 🎯 Controls

### ⌨️ **Keyboard Controls**
| Action | Keys | Description |
|--------|------|-------------|
| **Movement** | ↑↓←→ or WASD | Control snake direction |
| **Pause** | Space | Pause/resume game |
| **Menu** | Escape | Return to menu/settings |
| **Restart** | R | Restart current game (when game over) |
| **Skip Music** | M | Skip to next track |
| **Fullscreen** | F11 | Toggle fullscreen mode |
| **Debug Mode** | F1 | Toggle debug information |

### 🖱️ **Mouse Support**
- **Menu Navigation**: Click buttons and UI elements
- **Slider Controls**: Drag to adjust volume and settings
- **Resolution Selection**: Click to change display modes

## 🛠️ Command Line Options

```bash
python main.py [OPTIONS]

Options:
  --legacy          Run original SNAKEIUM 1.0
  --fullscreen      Start in fullscreen mode
  --no-music       Disable background music
  --config FILE    Use custom configuration file
  --debug          Enable debug mode and performance monitoring
  --help           Show help message
  --version        Show version information
```

## 📁 Project Structure

```
SNAKEIUM/
├── src/snakeium/           # Main package
│   ├── __init__.py         # Package initialization
│   ├── game_engine.py      # Core game logic and main loop
│   ├── config_manager.py   # Configuration and settings
│   ├── audio_manager.py    # Music and sound effects
│   └── ui_manager.py       # User interface and menus
├── legacy/                 # Original SNAKEIUM 1.0 files
├── tests/                  # Unit tests and test files
├── assets/                 # Game assets and resources
├── docs/                   # Documentation files
├── config/                 # Default configuration files
├── main.py                 # Main entry point
├── setup.py               # Package installation
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🧪 Development & Testing

### 🔧 **Development Setup**
```bash
# Clone repository
git clone https://github.com/chousemp3/SNAKEIUM.git
cd SNAKEIUM

# Install in development mode with all extras
pip install -e .[dev,all]

# Run tests
pytest tests/

# Format code
black src/ tests/

# Type checking
mypy src/
```

### 🐛 **Testing**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_game_engine.py -v

# Test with coverage
python -m pytest --cov=snakeium tests/
```

## 🚚 Distribution & Packaging

### 📦 **Creating Executables**
```bash
# Install packaging dependencies
pip install .[packaging]

# Create standalone executable
pyinstaller --onefile --windowed main.py

# Cross-platform packaging
cx_Freeze setup.py build
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### 🔄 **Development Workflow**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to your branch: `git push origin feature/amazing-feature`
7. Create a Pull Request

### 🐛 **Bug Reports**
Please use the [GitHub Issues](https://github.com/chousemp3/SNAKEIUM/issues) page to report bugs with:
- Detailed description of the issue
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, etc.)

## 📜 Version History

### 🔥 **Version 2.0.0** (Current)
- Complete rewrite with modular architecture
- Multiple game modes and enhanced features
- Advanced configuration and theme systems
- Comprehensive audio engine overhaul
- Improved performance and stability

### 🎮 **Version 1.0.0** (Legacy)
- Original single-file implementation
- Basic Snake gameplay with GHOSTKITTY music
- Rainbow visual effects and particle systems
- Simple power-up system

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

## 📋 System Requirements

### 🖥️ **Minimum Requirements**
- **OS**: Windows 7+, macOS 10.12+, Linux (Ubuntu 16.04+)
- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Storage**: 50 MB free space
- **Audio**: Sound card (optional, for music)

### ⚡ **Recommended Requirements**
- **OS**: Windows 10+, macOS 12+, Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **RAM**: 2 GB
- **Storage**: 200 MB free space (for music files)
- **Display**: 1920x1080 resolution
- **Audio**: Dedicated sound card or high-quality audio

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GHOSTKITTY** - For the incredible music collection that inspired this project
- **Pygame Community** - For the amazing game development framework
- **Python Community** - For the excellent language and ecosystem
- **8-bit Art Community** - For inspiration on pixel art and retro aesthetics
- **All Contributors** - Thank you for making SNAKEIUM even better!

## 🔗 Links

- **Homepage**: [SNAKEIUM Official](https://github.com/chousemp3/SNAKEIUM)
- **Documentation**: [GitHub Wiki](https://github.com/chousemp3/SNAKEIUM/wiki)
- **Issue Tracker**: [GitHub Issues](https://github.com/chousemp3/SNAKEIUM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/chousemp3/SNAKEIUM/discussions)
- **Releases**: [GitHub Releases](https://github.com/chousemp3/SNAKEIUM/releases)

---

**Made with 💜 for the retro gaming community!**

*"Experience the smoothest and most feature-rich Snake game ever created!"* 🐍✨
