# SNAKEIUM API Reference

## Core Classes

### ConfigManager

Handles all configuration and settings for SNAKEIUM.

```python
from snakeium.config_manager import ConfigManager

config = ConfigManager()
```

#### Methods

##### `load_config(config_path=None)`
Load configuration from file or create default.

**Parameters:**
- `config_path` (str, optional): Path to config file

**Returns:** Configuration dictionary

##### `save_config()`
Save current configuration to file.

##### `get(key, default=None)`
Get configuration value.

**Parameters:**
- `key` (str): Configuration key
- `default` (any): Default value if key not found

**Returns:** Configuration value

##### `set(key, value)`
Set configuration value.

**Parameters:**
- `key` (str): Configuration key  
- `value` (any): Value to set

##### `reset_to_defaults()`
Reset all settings to default values.

#### Configuration Keys

```python
# Display settings
config.get('display.width', 800)
config.get('display.height', 600)
config.get('display.fullscreen', False)
config.get('display.fps', 60)

# Audio settings  
config.get('audio.music_volume', 0.7)
config.get('audio.effects_volume', 0.8)
config.get('audio.enabled', True)

# Game settings
config.get('game.difficulty', 'normal')
config.get('game.start_speed', 5)
config.get('game.theme', 'classic')
```

---

### AudioManager

Manages music and sound effects with advanced features.

```python
from snakeium.audio_manager import AudioManager

audio = AudioManager(config_manager)
```

#### Methods

##### `load_music_directory(directory_path)`
Load all music files from directory.

**Parameters:**
- `directory_path` (str): Path to music directory

##### `play_music(track_name=None)`
Play music track with crossfading.

**Parameters:**
- `track_name` (str, optional): Specific track to play

##### `next_track()`
Skip to next music track.

##### `play_effect(effect_name, **kwargs)`
Play sound effect.

**Parameters:**
- `effect_name` (str): Name of effect ('eat', 'crash', 'powerup')
- `**kwargs`: Effect parameters (pitch, duration, etc.)

##### `set_music_volume(volume)`
Set music volume.

**Parameters:**
- `volume` (float): Volume level (0.0 to 1.0)

##### `set_effects_volume(volume)`
Set effects volume.

**Parameters:**
- `volume` (float): Volume level (0.0 to 1.0)

---

### UIManager

Handles all user interface elements and menus.

```python
from snakeium.ui_manager import UIManager

ui = UIManager(config_manager, audio_manager)
```

#### Methods

##### `handle_event(event)`
Process pygame events for UI.

**Parameters:**
- `event` (pygame.Event): Event to handle

**Returns:** Action string or None

##### `update(dt)`
Update UI animations and state.

**Parameters:**
- `dt` (float): Delta time in seconds

##### `draw(screen)`
Render UI elements to screen.

**Parameters:**
- `screen` (pygame.Surface): Surface to draw on

##### `show_menu(menu_name)`
Display specific menu.

**Parameters:**
- `menu_name` (str): Menu name ('main', 'settings', 'pause')

---

### Game

Main game engine and logic controller.

```python
from snakeium.game_engine import Game

game = Game(config_manager, audio_manager, ui_manager)
```

#### Methods

##### `run()`
Start the main game loop.

##### `handle_input(keys)`
Process player input.

**Parameters:**
- `keys` (pygame.key): Pressed keys

##### `update(dt)`
Update game state.

**Parameters:**
- `dt` (float): Delta time in seconds

##### `draw(screen)`
Render game to screen.

**Parameters:**
- `screen` (pygame.Surface): Surface to draw on

##### `reset_game()`
Reset game to initial state.

##### `pause_game()`
Pause/unpause game.

---

## Game Objects

### Snake

Player-controlled snake entity.

#### Properties
- `body` (list): Snake segments as (x, y) tuples
- `direction` (tuple): Current movement direction
- `length` (int): Current snake length
- `alive` (bool): Snake status

#### Methods
- `move()`: Move snake forward
- `grow()`: Increase snake length
- `check_collision(walls, self_collision=True)`: Check for collisions

### Food

Food items for the snake to collect.

#### Properties
- `position` (tuple): Food position (x, y)
- `type` (str): Food type ('normal', 'special')
- `points` (int): Points awarded

### PowerUp

Special items with temporary effects.

#### Properties
- `position` (tuple): PowerUp position
- `type` (str): PowerUp type
- `duration` (float): Effect duration
- `active` (bool): Whether effect is active

#### Types
- `speed_boost`: Increases snake speed
- `shield`: Temporary invincibility  
- `double_points`: Double scoring
- `size_reduction`: Temporarily smaller snake
- `multi_food`: Multiple food items

---

## Constants

### Game Modes
```python
CLASSIC_MODE = "classic"        # Traditional Snake
TIME_ATTACK_MODE = "time"       # Score within time limit  
ZEN_MODE = "zen"               # Relaxed, no death
CHALLENGE_MODE = "challenge"    # Progressive difficulty
```

### Directions
```python
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
```

### Colors
```python
# Theme colors are configurable
SNAKE_COLOR = config.get('theme.snake_color', (0, 255, 0))
FOOD_COLOR = config.get('theme.food_color', (255, 0, 0))
BACKGROUND_COLOR = config.get('theme.background_color', (0, 0, 0))
```

---

## Events

### Custom Events
SNAKEIUM generates custom pygame events for game state changes:

```python
# Event types
SNAKE_ATE_FOOD = pygame.USEREVENT + 1
SNAKE_CRASHED = pygame.USEREVENT + 2  
POWERUP_ACTIVATED = pygame.USEREVENT + 3
LEVEL_COMPLETED = pygame.USEREVENT + 4
```

---

## Configuration Files

### Default Config Location
- **Windows**: `%USERPROFILE%\.snakeium\config.json`
- **macOS**: `~/.snakeium/config.json`
- **Linux**: `~/.snakeium/config.json`

### Custom Config
```python
# Load custom configuration
config = ConfigManager('my-custom-config.json')

# Or set via environment
import os
os.environ['SNAKEIUM_CONFIG'] = '/path/to/config.json'
```

---

## Examples

### Basic Game Setup
```python
from snakeium import ConfigManager, AudioManager, UIManager, Game

# Initialize components
config = ConfigManager()
audio = AudioManager(config)
ui = UIManager(config, audio)
game = Game(config, audio, ui)

# Run game
game.run()
```

### Custom Theme
```python
# Create custom theme
custom_theme = {
    'snake_color': (255, 100, 0),    # Orange snake
    'food_color': (0, 255, 255),     # Cyan food  
    'background_color': (20, 20, 20), # Dark gray background
    'grid_color': (40, 40, 40)       # Grid lines
}

config.set('theme', custom_theme)
config.save_config()
```

### Adding Custom Music
```python
# Add music directory
audio.load_music_directory('/path/to/my/music')

# Play specific track
audio.play_music('my-favorite-song.mp3')
```
