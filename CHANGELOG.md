# 📜 SNAKEIUM Changelog

All notable changes to SNAKEIUM - GHOSTKITTY Edition will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-08-21 🎉

### 🎵 **GHOSTKITTY Edition Release**

#### ✨ Added
- **Retro Start Menu**: 8-bit styled menu with 5 speed settings
  - 🐌 CHILL MODE (2 moves/sec)
  - 🎮 CLASSIC (4 moves/sec) 
  - ⚡ FAST (6 moves/sec)
  - 🚀 INSANE (8 moves/sec)
  - 💀 NIGHTMARE (12 moves/sec)

- **Music System**: Complete GHOSTKITTY soundtrack integration
  - 75 original GHOSTKITTY tracks
  - Seamless looping and track switching
  - Music metadata display
  - Skip track functionality (M key)

- **Enhanced Visuals**: 
  - Pixelated 8-bit backgrounds with rainbow effects
  - Scan line effects for authentic CRT feel
  - Animated geometric backgrounds (pyramids, triangles)
  - Particle effects for food consumption
  - Dynamic color palettes

- **Power-up System**:
  - 🔵 Speed Boost (5 seconds)
  - 🟡 Score Multiplier (2x for 10 seconds)
  - 🟣 Rainbow Mode (psychedelic colors)
  - 🟠 Mega Food (extra large food pieces)

- **Ultra-smooth Movement**: 
  - 60 FPS locked gameplay
  - Easing functions for professional feel
  - Sub-pixel positioning
  - Interpolated movement animations

#### 🔧 Technical Improvements
- **Safe Mode**: Windowed mode prevents system freezing
- **Dynamic Background**: Fills entire window regardless of size
- **Error Handling**: Comprehensive error catching and recovery
- **Performance Monitoring**: Real-time FPS tracking and warnings
- **Memory Optimization**: Reduced particle counts and effect complexity

#### 🎮 Gameplay Features
- **Progressive Scoring**: Points scale with snake length and speed
- **Game States**: Menu → Playing → Game Over flow
- **Pause System**: Space to pause/resume with overlay
- **Restart Functionality**: Quick restart from game over

#### 🐛 Fixed
- Background not filling entire window
- Speed settings not affecting snake movement
- Music not playing in safe mode
- Window freezing issues in fullscreen
- Performance drops with visual effects

#### 📱 Compatibility
- **Cross-platform**: Windows, macOS, Linux support
- **Python 3.8+**: Modern Python compatibility
- **Dynamic Sizing**: Works with any window resolution
- **Graceful Degradation**: Fallbacks for missing features
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-21

### Added
- 🎮 **Core Game Features**
  - Modern Snake game with 120Hz ultra-smooth movement
  - 8-bit pixel art snake and apple sprites
  - Wrap-around screen edges (no wall deaths)
  - Progressive difficulty scaling
  - Score system with visual feedback

- 🎵 **Dynamic Music System**
  - Automatic MP3 file detection and playback
  - Support for custom music folders
  - Shuffle and sequential playback modes
  - Volume control and skip functionality
  - Graceful fallback when music unavailable

- ⚡ **Power-up System**
  - Speed Boost: Temporary speed increase
  - Score Multiplier: 3x points for 10 seconds
  - Rainbow Mode: Rainbow snake with particle trails
  - Mega Food: Instant growth by 3 segments

- 🌈 **Visual Effects**
  - Animated rainbow gradient background
  - Geometric effects: rotating pyramids and triangles
  - Particle explosion systems
  - Smooth sprite animations and interpolation
  - Fullscreen experience with adaptive UI

- 🛠️ **Technical Features**
  - Command-line argument support
  - Configurable performance settings
  - Error handling and graceful degradation
  - Cross-platform compatibility
  - Comprehensive documentation

### Technical Details
- **Performance**: Optimized for 120 FPS with configurable target
- **Graphics**: Hardware-accelerated rendering with pygame
- **Audio**: MP3 support via pygame.mixer
- **Dependencies**: pygame, mutagen (optional), numpy (optional)

### Command Line Options
```bash
--music-folder PATH      # Custom music directory
--no-music              # Disable background music
--no-effects            # Disable geometric effects
--fps INTEGER           # Set target FPS
--windowed              # Run in windowed mode
--resolution WxH        # Set window resolution
--volume FLOAT          # Set music volume
--debug                 # Enable debug output
```

### Known Issues
- None reported

### Credits
- Inspired by classic Snake games
- Music integration designed for GHOSTKITTY collection
- Built with pygame and modern Python practices
