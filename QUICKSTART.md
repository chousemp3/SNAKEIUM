# Quick Start Guide

## 🚀 Instant Play (No Installation)

```bash
# 1. Clone the repository
git clone https://github.com/chousemp3/SNAKEIUM.git
cd SNAKEIUM

# 2. Set up environment (one-time setup)
python3 -m venv venv
source venv/bin/activate
pip install pygame numpy mutagen

# 3. Play SNAKEIUM!
python main.py
```

## 🎮 Game Controls

- **Arrow Keys** or **WASD**: Move snake
- **Space**: Pause/Resume
- **ESC**: Main menu
- **M**: Skip music track
- **R**: Restart game
- **F11**: Toggle fullscreen

## 🎯 Game Modes

- **Classic**: Traditional Snake gameplay
- **Time Attack**: Score as much as possible within time limit
- **Zen Mode**: Relaxed gameplay, no death
- **Challenge**: Progressive difficulty with power-ups

## 🔧 Advanced Usage

```bash
# Run original version
python main.py --legacy

# Start in fullscreen
python main.py --fullscreen

# Disable music
python main.py --no-music

# Use custom config
python main.py --config my-config.json

# Enable debug mode
python main.py --debug
```

## 📁 Project Structure

```
SNAKEIUM/
├── main.py              # Main entry point
├── src/snakeium/        # Modern modular package
│   ├── game_engine.py   # Core game logic
│   ├── config_manager.py # Settings management
│   ├── audio_manager.py  # Music and sound effects
│   └── ui_manager.py     # User interface
├── legacy/              # Original SNAKEIUM 1.0
├── docs/                # Documentation
└── tests/               # Test suite
```

## 🐛 Troubleshooting

**No Sound?**
- Check if `mutagen` is installed: `pip install mutagen`
- Verify audio files in music directory

**Game Won't Start?**
- Ensure `pygame` is installed: `pip install pygame`
- Try running with `--debug` flag for more info

**Import Errors?**
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Verify all dependencies: `pip install -r requirements.txt`

## 🎵 Adding Custom Music

1. Create a `music/` directory
2. Add MP3, OGG, WAV, or FLAC files
3. Game will automatically detect and play them

Enjoy SNAKEIUM! 🐍✨
