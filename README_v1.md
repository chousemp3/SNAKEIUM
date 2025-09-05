# 🐍 SNAKEIUM - GHOSTKITTY Edition 🎵

A modern retro Snake game with stunning 8-bit visuals, rainbow effects, and an epic GHOSTKITTY soundtrack. Experience the classic game reimagined with ultra-smooth 60 FPS gameplay, multiple speed settings, and authentic retro aesthetics.

[![Tests](https://github.com/chousemp3/SNAKEIUM/actions/workflows/minimal-ci.yml/badge.svg)](https://github.com/chousemp3/SNAKEIUM/actions/workflows/minimal-ci.yml)
![Python Version](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
[![Version](https://img.shields.io/badge/Version-1.0.0-red.svg)](https://github.com/chousemp3/SNAKEIUM/releases)

A high-performance, modern Snake game featuring 60 FPS ultra-smooth gameplay, 8-bit pixel art graphics, dynamic music integration, and mind-bending geometric visual effects!

![SNAKEIUM Demo](assets/demo.gif)

## ✨ Features

### 🎮 **Gameplay**
- **120Hz Ultra-Smooth Movement** - Buttery smooth snake movement with interpolation
- **8-bit Pixel Art Style** - Authentic retro snake and apple sprites
- **Wrap-Around Screen** - No death from hitting walls, snake wraps around edges
- **Progressive Difficulty** - Speed increases as snake grows longer
- **Power-up System** - Four unique power-ups with special effects

### 🎵 **Dynamic Music System**
- **Automatic Music Detection** - Scans for MP3 files in multiple locations
- **Random/Sequential Playback** - Shuffle mode with metadata support
- **Volume Control** - Adjustable background music volume
- **Skip Function** - Press 'M' to skip to next track
- **Error Handling** - Graceful fallback when music files unavailable

### 🌈 **Visual Effects**
- **Animated Rainbow Background** - Smooth color-cycling gradient strips
- **Geometric Chaos** - Rotating pyramids and triangles with trails
- **Particle Systems** - Explosions when eating food or power-ups
- **Rainbow Mode** - Snake becomes rainbow with particle trails
- **Smooth Animations** - All effects optimized for 120 FPS

### ⚡ **Power-ups**
- 🔵 **Speed Boost** - Temporary speed increase
- 🟡 **Score Multiplier** - 3x points for 10 seconds
- 🟣 **Rainbow Mode** - Rainbow snake with particle effects
- 🟠 **Mega Food** - Instantly grow by 3 segments

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/snakeium.git
cd snakeium

# Install dependencies
pip install -r requirements.txt

# Run the game
python snakeium.py
```

### Manual Installation
```bash
pip install pygame pygame-menu mutagen numpy
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** / **WASD** | Move snake |
| **SPACE** | Pause/Unpause |
| **M** | Skip to next music track |
| **R** | Restart game (when game over) |
| **ESC** | Quit game |

## ⚙️ Command Line Options

```bash
python snakeium.py [OPTIONS]

Options:
  --help                    Show help message
  --version                 Show version information
  --music-folder PATH       Specify custom music folder
  --no-music                Disable background music
  --no-effects              Disable geometric effects (better performance)
  --no-particles            Disable particle effects
  --fps INTEGER             Set target FPS (default: 120)
  --windowed                Run in windowed mode
  --resolution WIDTHxHEIGHT Set window resolution (e.g., 1920x1080)
  --volume FLOAT            Set music volume (0.0-1.0)
  --debug                   Enable debug output
```

### Examples
```bash
# Run with custom music folder
python snakeium.py --music-folder ~/Music

# Run in windowed mode with 60 FPS
python snakeium.py --windowed --fps 60 --resolution 1280x720

# Performance mode (no effects)
python snakeium.py --no-effects --no-particles --fps 60

# Debug mode with custom settings
python snakeium.py --debug --volume 0.5 --no-music
```

## 🎵 Music Setup

SNAKEIUM automatically searches for MP3 files in these locations:
1. Default: `c:\Users\music2\Desktop\GHOSTKITTY MP3S` (customizable)
2. User's Music folder (`~/Music`)
3. User's Desktop
4. Current directory

**Supported formats:** MP3 files

**Custom music folder:**
```bash
python snakeium.py --music-folder "/path/to/your/music"
```

## 🛠️ Configuration

### Performance Tuning
For older hardware or better performance:
```bash
# Minimal effects mode
python snakeium.py --fps 60 --no-effects --no-particles

# Windowed mode for better performance
python snakeium.py --windowed --resolution 1280x720 --fps 60
```

### Visual Quality
For maximum visual effects:
```bash
# Full effects mode (default)
python snakeium.py --fps 120

# Debug mode to see performance stats
python snakeium.py --debug
```

## 🏗️ Project Structure

```
snakeium/
├── snakeium.py          # Main game file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
├── assets/             # Game assets (if any)
│   └── demo.gif        # Demo animation
└── docs/               # Documentation
    ├── CONTRIBUTING.md
    └── CHANGELOG.md
```

## 🎨 Technical Details

### Performance
- **Target FPS:** 120 (configurable)
- **Smooth Movement:** Sub-pixel interpolation
- **Particle Limit:** 300 particles max
- **Effect Optimization:** Intelligent culling and batching

### Graphics Pipeline
1. Animated rainbow background (40 gradient strips)
2. Geometric effects (pyramids, triangles, spirals)
3. Game objects (food, power-ups)
4. Snake sprites with smooth interpolation
5. Particle effects
6. UI overlay

### Audio System
- **Format Support:** MP3 (via pygame.mixer)
- **Metadata:** mutagen integration (optional)
- **Fallback:** Graceful degradation without music
- **Volume Control:** 0.0-1.0 range

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/yourusername/snakeium.git
cd snakeium
pip install -r requirements.txt
python snakeium.py --debug
```

### Reporting Issues
Please use the [GitHub issue tracker](https://github.com/yourusername/snakeium/issues) to report bugs or request features.

## 📋 Requirements

- **Python:** 3.7+
- **pygame:** 2.0+
- **mutagen:** 1.45+ (optional, for music metadata)
- **numpy:** 1.21+ (optional, for advanced effects)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GHOSTKITTY** - For the epic music collection that inspired this project
- **Pygame Community** - For the amazing game development framework
- **8-bit Art Community** - For inspiration on pixel art aesthetics

## 🔮 Roadmap

- [ ] High score system with leaderboards
- [ ] Multiplayer support
- [ ] Custom themes and color schemes
- [ ] Level editor
- [ ] Mobile version
- [ ] Achievement system
- [ ] Replay system
- [ ] More power-ups and game modes

---

**Made with 💜 for the retro gaming community!**

*"Experience the smoothest snake game ever created!"* 🐍✨
