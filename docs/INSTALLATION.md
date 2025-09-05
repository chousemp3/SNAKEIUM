# SNAKEIUM 2.0 Installation Guide

## 🚀 Quick Installation

### Method 1: Direct Run (Recommended)
```bash
# Clone the repository
git clone https://github.com/chousemp3/SNAKEIUM.git
cd SNAKEIUM

# Install dependencies
pip install -r requirements.txt

# Run SNAKEIUM 2.0
python main.py
```

### Method 2: Package Installation
```bash
# Install as package
pip install -e .

# Run from anywhere
snakeium

# Or with options
snakeium --fullscreen
```

### Method 3: Standalone Executable
Download the pre-built executable for your platform:
- **Windows**: `snakeium-windows.exe`
- **macOS**: `snakeium-macos`
- **Linux**: `snakeium-linux`

## 📋 System Requirements

### Minimum
- Python 3.8+
- 512 MB RAM
- 50 MB disk space

### Recommended
- Python 3.11+
- 2 GB RAM
- 200 MB disk space

## 🔧 Development Setup

```bash
# Clone and install development dependencies
git clone https://github.com/chousemp3/SNAKEIUM.git
cd SNAKEIUM
pip install -e .[dev,all]

# Run tests
pytest tests/

# Format code
black src/ tests/
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `pygame.error: No available video device`
**Solution**: Install SDL2 libraries or run with `SDL_VIDEODRIVER=dummy`

**Issue**: `ModuleNotFoundError: No module named 'snakeium'`
**Solution**: Run `pip install -e .` or use `python main.py`

**Issue**: No sound/music
**Solution**: Check audio settings and install `mutagen` for music support

## 🎮 First Run

1. Run `python main.py`
2. Use arrow keys or WASD to move
3. Press ESC to access settings
4. Press M to skip music tracks
5. Press F11 for fullscreen

## ⚙️ Configuration

Settings are saved to `~/.snakeium/config.json` automatically.
You can also create custom configuration files and load them with:
```bash
python main.py --config my-config.json
```
