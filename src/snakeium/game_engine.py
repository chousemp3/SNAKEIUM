"""
Enhanced Game Engine for SNAKEIUM 2.0
Main game logic, entities, and game loop management.
"""

import pygame
import random
import math
import time
import sys
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
import threading
from pathlib import Path

from .config_manager import ConfigManager, GameMode, Theme
from .audio_manager import AudioManager, AudioEvent
from .ui_manager import UIManager


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class PowerUpType(Enum):
    SPEED_BOOST = "speed"
    SCORE_MULTIPLIER = "score"
    RAINBOW_MODE = "rainbow"
    MEGA_FOOD = "mega"
    SHIELD = "shield"
    SLOW_TIME = "slow_time"
    DOUBLE_SCORE = "double_score"
    TELEPORT = "teleport"


class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


@dataclass
class Position:
    x: int
    y: int
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def to_tuple(self):
        return (self.x, self.y)


class Particle:
    """Enhanced particle system for visual effects."""
    
    def __init__(self, x: float, y: float, velocity: Tuple[float, float], 
                 color: Tuple[int, int, int], lifetime: int = 60, size: int = 3):
        self.x = x
        self.y = y
        self.vx, self.vy = velocity
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = 0.1
        self.fade = True
        self.trail = []
        
    def update(self):
        """Update particle physics."""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.lifetime -= 1
        
        # Add to trail
        if len(self.trail) > 5:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))
        
        # Reduce velocity over time
        self.vx *= 0.98
        self.vy *= 0.98
    
    def draw(self, screen: pygame.Surface):
        """Draw particle with trail effect."""
        if self.lifetime <= 0:
            return
        
        alpha = 1.0 if not self.fade else (self.lifetime / self.max_lifetime)
        
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            trail_alpha = alpha * (i / len(self.trail))
            trail_size = max(1, int(self.size * trail_alpha))
            trail_color = tuple(int(c * trail_alpha) for c in self.color)
            pygame.draw.circle(screen, trail_color, (int(tx), int(ty)), trail_size)
        
        # Draw main particle
        main_size = max(1, int(self.size * alpha))
        main_color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(screen, main_color, (int(self.x), int(self.y)), main_size)
    
    def is_alive(self) -> bool:
        return self.lifetime > 0


class Food:
    """Enhanced food with different types and effects."""
    
    def __init__(self, grid_width: int, grid_height: int, snake_body: List[Position]):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self._generate_position(snake_body)
        self.type = random.choice(['normal', 'golden', 'mega'])
        self.pulse = 0.0
        self.spawn_time = time.time()
        
        # Type-specific properties
        self.properties = {
            'normal': {'score': 10, 'color': (255, 0, 0), 'size': 1},
            'golden': {'score': 50, 'color': (255, 215, 0), 'size': 1.2},
            'mega': {'score': 100, 'color': (255, 140, 0), 'size': 1.5}
        }
    
    def _generate_position(self, snake_body: List[Position]) -> Position:
        """Generate a valid position for food."""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            pos = Position(x, y)
            
            if pos not in snake_body:
                return pos
        
        # Fallback: find first empty position
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                pos = Position(x, y)
                if pos not in snake_body:
                    return pos
        
        return Position(0, 0)  # Last resort
    
    def update(self):
        """Update food animation."""
        self.pulse += 0.2
    
    def draw(self, screen: pygame.Surface, grid_size: int):
        """Draw food with pulsing effect."""
        props = self.properties[self.type]
        pulse_factor = 1 + 0.2 * math.sin(self.pulse)
        size = int(grid_size * props['size'] * pulse_factor)
        
        center_x = self.position.x * grid_size + grid_size // 2
        center_y = self.position.y * grid_size + grid_size // 2
        
        # Draw glow effect for special food
        if self.type != 'normal':
            glow_size = size + 10
            glow_color = tuple(c // 3 for c in props['color'])
            pygame.draw.circle(screen, glow_color, (center_x, center_y), glow_size)
        
        pygame.draw.circle(screen, props['color'], (center_x, center_y), size // 2)
        
        # Draw shine effect
        shine_color = tuple(min(255, c + 100) for c in props['color'])
        pygame.draw.circle(screen, shine_color, 
                          (center_x - size // 4, center_y - size // 4), 
                          max(1, size // 6))
    
    def get_score_value(self) -> int:
        return self.properties[self.type]['score']


class PowerUp:
    """Enhanced power-up system."""
    
    def __init__(self, grid_width: int, grid_height: int, snake_body: List[Position]):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self._generate_position(snake_body)
        self.type = random.choice(list(PowerUpType))
        self.spawn_time = time.time()
        self.lifetime = 15  # seconds
        self.pulse = 0.0
        self.rotation = 0.0
        
        # Type-specific properties
        self.properties = {
            PowerUpType.SPEED_BOOST: {'color': (0, 191, 255), 'symbol': 'S'},
            PowerUpType.SCORE_MULTIPLIER: {'color': (255, 255, 0), 'symbol': 'x'},
            PowerUpType.RAINBOW_MODE: {'color': (138, 43, 226), 'symbol': 'R'},
            PowerUpType.MEGA_FOOD: {'color': (255, 140, 0), 'symbol': 'M'},
            PowerUpType.SHIELD: {'color': (0, 255, 0), 'symbol': '+'},
            PowerUpType.SLOW_TIME: {'color': (128, 0, 128), 'symbol': 'T'},
            PowerUpType.DOUBLE_SCORE: {'color': (255, 69, 0), 'symbol': 'D'},
            PowerUpType.TELEPORT: {'color': (0, 255, 255), 'symbol': 'W'}
        }
    
    def _generate_position(self, snake_body: List[Position]) -> Position:
        """Generate a valid position for power-up."""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            pos = Position(x, y)
            
            if pos not in snake_body:
                return pos
        
        return Position(0, 0)
    
    def update(self):
        """Update power-up animation."""
        self.pulse += 0.3
        self.rotation += 5
    
    def is_expired(self) -> bool:
        return time.time() - self.spawn_time > self.lifetime
    
    def draw(self, screen: pygame.Surface, grid_size: int, font: pygame.font.Font):
        """Draw power-up with animated effects."""
        props = self.properties[self.type]
        pulse_factor = 1 + 0.4 * math.sin(self.pulse)
        
        center_x = self.position.x * grid_size + grid_size // 2
        center_y = self.position.y * grid_size + grid_size // 2
        
        # Draw rotating glow
        glow_radius = int(grid_size * 0.6 * pulse_factor)
        for i in range(3):
            alpha = 100 - i * 30
            glow_color = (*props['color'], alpha)
            # Note: pygame doesn't support alpha in draw functions, so we'll skip advanced blending
        
        # Draw main circle
        main_radius = grid_size // 2
        pygame.draw.circle(screen, props['color'], (center_x, center_y), main_radius)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), main_radius, 2)
        
        # Draw symbol
        symbol_surface = font.render(props['symbol'], True, (255, 255, 255))
        symbol_rect = symbol_surface.get_rect(center=(center_x, center_y))
        screen.blit(symbol_surface, symbol_rect)


class Snake:
    """Enhanced snake with smooth movement and effects."""
    
    def __init__(self, grid_width: int, grid_height: int, initial_speed: int = 5):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.body = [Position(grid_width // 2, grid_height // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.speed = initial_speed
        self.grow_pending = 0
        
        # Smooth movement
        self.move_timer = 0
        self.move_interval = 60 // self.speed  # frames between moves
        
        # Effects
        self.effects = {
            'speed_boost': 0,
            'score_multiplier': 1,
            'score_multiplier_timer': 0,
            'rainbow_mode': 0,
            'shield': 0,
            'slow_time': 0,
            'double_score': 0
        }
        
        # Visual properties
        self.rainbow_hue = 0.0
        self.skin_pattern = 'default'
        
    def update(self):
        """Update snake logic."""
        # Update effects
        for effect in ['speed_boost', 'rainbow_mode', 'shield', 'slow_time', 'double_score']:
            if self.effects[effect] > 0:
                self.effects[effect] -= 1
        
        if self.effects['score_multiplier_timer'] > 0:
            self.effects['score_multiplier_timer'] -= 1
        else:
            self.effects['score_multiplier'] = 1
        
        # Update rainbow effect
        self.rainbow_hue = (self.rainbow_hue + 0.05) % 1.0
        
        # Update movement timing
        current_speed = self.get_current_speed()
        time_factor = 0.5 if self.effects['slow_time'] > 0 else 1.0
        self.move_interval = max(1, int(60 // (current_speed * time_factor)))
        
        # Move snake
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move()
    
    def move(self):
        """Move the snake one step."""
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        dx, dy = self.direction.value
        new_head = Position(
            (self.body[0].x + dx) % self.grid_width,
            (self.body[0].y + dy) % self.grid_height
        )
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Handle growth
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def change_direction(self, new_direction: Direction):
        """Change snake direction with collision prevention."""
        # Prevent 180-degree turns
        if len(self.body) > 1:
            current_dx, current_dy = self.direction.value
            new_dx, new_dy = new_direction.value
            
            if (current_dx + new_dx == 0 and current_dy + new_dy == 0):
                return  # Invalid direction
        
        self.next_direction = new_direction
    
    def check_self_collision(self) -> bool:
        """Check if snake has collided with itself."""
        if self.effects['shield'] > 0:
            return False  # Shield protects from self-collision
        
        head = self.body[0]
        return head in self.body[1:]
    
    def eat_food(self, food: Food):
        """Handle eating food."""
        base_growth = 1
        if food.type == 'mega':
            base_growth = 3
        elif food.type == 'golden':
            base_growth = 2
        
        self.grow_pending += base_growth
    
    def eat_powerup(self, powerup: PowerUp):
        """Handle eating power-up."""
        effect_type = powerup.type
        
        if effect_type == PowerUpType.SPEED_BOOST:
            self.effects['speed_boost'] = 300  # 5 seconds at 60 FPS
        elif effect_type == PowerUpType.SCORE_MULTIPLIER:
            self.effects['score_multiplier'] = 3
            self.effects['score_multiplier_timer'] = 600  # 10 seconds
        elif effect_type == PowerUpType.RAINBOW_MODE:
            self.effects['rainbow_mode'] = 900  # 15 seconds
        elif effect_type == PowerUpType.MEGA_FOOD:
            self.grow_pending += 5
        elif effect_type == PowerUpType.SHIELD:
            self.effects['shield'] = 600  # 10 seconds
        elif effect_type == PowerUpType.SLOW_TIME:
            self.effects['slow_time'] = 480  # 8 seconds
        elif effect_type == PowerUpType.DOUBLE_SCORE:
            self.effects['double_score'] = 450  # 7.5 seconds
    
    def get_current_speed(self) -> int:
        """Get current speed including effects."""
        base_speed = self.speed + len(self.body) // 10
        
        if self.effects['speed_boost'] > 0:
            return min(base_speed * 2, 30)
        
        return base_speed
    
    def get_score_multiplier(self) -> int:
        """Get current score multiplier."""
        multiplier = self.effects['score_multiplier']
        if self.effects['double_score'] > 0:
            multiplier *= 2
        return multiplier
    
    def draw(self, screen: pygame.Surface, grid_size: int, particles: List[Particle]):
        """Draw snake with enhanced visuals."""
        if not self.body:
            return
        
        # Generate rainbow colors if in rainbow mode
        if self.effects['rainbow_mode'] > 0:
            head_color = self._get_rainbow_color(0)
            body_color = self._get_rainbow_color(0.1)
        else:
            head_color = (0, 255, 0)
            body_color = (0, 200, 0)
        
        # Draw body segments
        for i, segment in enumerate(self.body):
            x = segment.x * grid_size
            y = segment.y * grid_size
            
            if i == 0:  # Head
                # Shield effect
                if self.effects['shield'] > 0:
                    shield_color = (0, 255, 255, 100)
                    pygame.draw.circle(screen, (0, 255, 255), 
                                     (x + grid_size // 2, y + grid_size // 2), 
                                     grid_size // 2 + 5)
                
                pygame.draw.rect(screen, head_color, (x, y, grid_size, grid_size))
                pygame.draw.rect(screen, (255, 255, 255), (x, y, grid_size, grid_size), 2)
                
                # Draw eyes
                eye_size = max(2, grid_size // 8)
                eye_offset = grid_size // 4
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (x + eye_offset, y + eye_offset), eye_size)
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (x + grid_size - eye_offset, y + eye_offset), eye_size)
                pygame.draw.circle(screen, (0, 0, 0), 
                                 (x + eye_offset, y + eye_offset), eye_size // 2)
                pygame.draw.circle(screen, (0, 0, 0), 
                                 (x + grid_size - eye_offset, y + eye_offset), eye_size // 2)
            else:  # Body
                # Vary color slightly for each segment
                if self.effects['rainbow_mode'] > 0:
                    segment_color = self._get_rainbow_color(i * 0.05)
                else:
                    darkness = min(50, i * 2)
                    segment_color = (max(0, body_color[0] - darkness), 
                                   max(0, body_color[1] - darkness), 
                                   max(0, body_color[2] - darkness))
                
                pygame.draw.rect(screen, segment_color, (x, y, grid_size, grid_size))
                pygame.draw.rect(screen, (0, 100, 0), (x, y, grid_size, grid_size), 1)
        
        # Generate particle effects
        if self.effects['rainbow_mode'] > 0 and random.random() < 0.3:
            head = self.body[0]
            particles.append(Particle(
                head.x * grid_size + grid_size // 2 + random.randint(-10, 10),
                head.y * grid_size + grid_size // 2 + random.randint(-10, 10),
                (random.uniform(-2, 2), random.uniform(-2, 2)),
                self._get_rainbow_color(random.random()),
                30
            ))
    
    def _get_rainbow_color(self, offset: float) -> Tuple[int, int, int]:
        """Get rainbow color with offset."""
        hue = (self.rainbow_hue + offset) % 1.0
        # Convert HSV to RGB
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return (int(r * 255), int(g * 255), int(b * 255))


class GameStats:
    """Track game statistics and achievements."""
    
    def __init__(self):
        self.start_time = time.time()
        self.food_eaten = 0
        self.powerups_collected = 0
        self.max_length = 1
        self.distance_traveled = 0
        self.effects_used = {}
    
    def update(self, snake: Snake):
        """Update statistics."""
        self.max_length = max(self.max_length, len(snake.body))
        
        # Track effect usage
        for effect, timer in snake.effects.items():
            if timer > 0 and effect not in ['score_multiplier', 'score_multiplier_timer']:
                self.effects_used[effect] = self.effects_used.get(effect, 0) + 1
    
    def get_play_time(self) -> float:
        return time.time() - self.start_time


class Game:
    """Main game engine with enhanced features."""
    
    def __init__(self, config_manager: ConfigManager = None):
        # Initialize pygame
        pygame.init()
        
        # Configuration
        self.config = config_manager or ConfigManager()
        
        # Display setup
        width, height, flags = self.config.get_display_mode()
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("SNAKEIUM 2.1 - GHOSTKITTY Edition")
        
        # Game clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = GameState.MENU
        self.current_mode = GameMode.CLASSIC
        
        # Grid system
        self.grid_size = 20
        self.grid_width = width // self.grid_size
        self.grid_height = height // self.grid_size
        
        # Game objects
        self.snake = None
        self.food = None
        self.powerups = []
        self.particles = []
        self.obstacles = []  # For maze mode
        
        # Game variables
        self.score = 0
        self.level = 1
        self.game_stats = None
        
        # Managers
        self.audio = AudioManager(self.config)
        self.ui = UIManager(self.screen, self.config, self.audio)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Background effects
        self.bg_hue = 0.0
        self.bg_effects = []
        
        print("SNAKEIUM 2.1 initialized successfully")
    
    def run(self):
        """Main game loop."""
        # Start background music
        if self.audio:
            self.audio.play_music()
        
        while self.running:
            dt = self.clock.tick(self.config.display.target_fps)
            
            # Handle events
            self.handle_events()
            
            # Update game
            self.update(dt)
            
            # Draw everything
            self.draw()
            
            # Check music
            if self.audio:
                new_song = self.audio.check_music()
                if new_song:
                    print(f"Now playing: {new_song}")
        
        # Cleanup
        self.cleanup()
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_F1:
                    self.config.developer.debug_mode = not self.config.developer.debug_mode
                
                # Handle state-specific events
                if self.state == GameState.MENU:
                    action = self.ui.handle_event(event)
                    if action:
                        self.handle_menu_action(action)
                
                elif self.state == GameState.PLAYING:
                    self.handle_game_input(event.key)
                
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_SPACE:
                        self.resume_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.return_to_menu()
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.return_to_menu()
            
            # Let UI handle events
            if self.state == GameState.MENU:
                self.ui.handle_event(event)
    
    def handle_menu_action(self, action: str):
        """Handle menu actions."""
        if action.startswith("start_game"):
            parts = action.split(":")
            if len(parts) > 1:
                mode_name = parts[1]
                self.current_mode = GameMode(mode_name)
            else:
                self.current_mode = GameMode.CLASSIC
            self.start_game()
        elif action == "quit":
            self.running = False
    
    def handle_game_input(self, key: int):
        """Handle game input during play."""
        # Movement
        if key in self.config.controls.up_keys:
            self.snake.change_direction(Direction.UP)
        elif key in self.config.controls.down_keys:
            self.snake.change_direction(Direction.DOWN)
        elif key in self.config.controls.left_keys:
            self.snake.change_direction(Direction.LEFT)
        elif key in self.config.controls.right_keys:
            self.snake.change_direction(Direction.RIGHT)
        
        # Game controls
        elif key == self.config.controls.pause_key:
            self.pause_game()
        elif key == self.config.controls.skip_music_key:
            if self.audio:
                new_song = self.audio.skip_track()
                if new_song:
                    print(f"Skipped to: {new_song}")
        elif key == self.config.controls.menu_key:
            self.pause_game()
    
    def start_game(self):
        """Start a new game."""
        self.state = GameState.PLAYING
        self.ui.set_state("game")
        
        # Initialize game objects
        self.snake = Snake(self.grid_width, self.grid_height, self.config.gameplay.default_speed)
        self.food = Food(self.grid_width, self.grid_height, self.snake.body)
        self.powerups = []
        self.particles = []
        self.obstacles = []
        
        # Reset game variables
        self.score = 0
        self.level = 1
        self.game_stats = GameStats()
        
        # Mode-specific setup
        if self.current_mode == GameMode.MAZE:
            self.generate_maze()
        
        # Play start sound
        if self.audio:
            self.audio.play_sound(AudioEvent.MENU_SELECT)
        
        print(f"Started {self.current_mode.value} mode")
    
    def pause_game(self):
        """Pause the game."""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
            self.ui.set_state("pause")
            if self.audio:
                self.audio.pause_music()
                self.audio.play_sound(AudioEvent.PAUSE)
    
    def resume_game(self):
        """Resume the game."""
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
            self.ui.set_state("game")
            if self.audio:
                self.audio.resume_music()
                self.audio.play_sound(AudioEvent.RESUME)
    
    def game_over(self):
        """Handle game over."""
        self.state = GameState.GAME_OVER
        self.ui.set_state("game_over")
        
        # Update statistics
        play_time = self.game_stats.get_play_time()
        self.config.update_statistics(
            total_games=1,
            total_playtime=play_time,
            longest_snake=self.game_stats.max_length,
            power_ups_collected=self.game_stats.powerups_collected
        )
        
        # Check for high score
        is_high_score = self.config.update_high_score(self.current_mode.value, self.score)
        
        # Save configuration
        self.config.save_config()
        
        # Play sound
        if self.audio:
            self.audio.play_sound(AudioEvent.GAME_OVER)
        
        print(f"Game Over! Score: {self.score:,}, Length: {len(self.snake.body)}")
        if is_high_score:
            print("NEW HIGH SCORE!")
    
    def restart_game(self):
        """Restart the current game."""
        self.start_game()
    
    def return_to_menu(self):
        """Return to the main menu."""
        self.state = GameState.MENU
        self.ui.set_state("menu")
    
    def update(self, dt: int):
        """Update game logic."""
        # Update UI
        self.ui.update()
        
        # Update background effects
        self.bg_hue = (self.bg_hue + 0.01) % 1.0
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
        
        # Limit particles for performance
        if len(self.particles) > self.config.gameplay.max_particles:
            self.particles = self.particles[-self.config.gameplay.max_particles:]
        
        # Game-specific updates
        if self.state == GameState.PLAYING:
            self.update_gameplay()
    
    def update_gameplay(self):
        """Update gameplay logic."""
        if not self.snake:
            return
        
        # Update snake
        self.snake.update()
        
        # Check collisions
        if self.snake.check_self_collision():
            self.game_over()
            return
        
        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.eat_food()
        
        # Check power-up collisions
        for powerup in self.powerups[:]:
            if self.snake.body[0] == powerup.position:
                self.eat_powerup(powerup)
                self.powerups.remove(powerup)
        
        # Remove expired power-ups
        for powerup in self.powerups[:]:
            if powerup.is_expired():
                self.powerups.remove(powerup)
        
        # Spawn power-ups
        self.spawn_powerup()
        
        # Update food
        self.food.update()
        
        # Update power-ups
        for powerup in self.powerups:
            powerup.update()
        
        # Update statistics
        if self.game_stats:
            self.game_stats.update(self.snake)
    
    def eat_food(self):
        """Handle eating food."""
        if not self.food or not self.snake:
            return
        
        # Snake grows
        self.snake.eat_food(self.food)
        
        # Update score
        base_score = self.food.get_score_value()
        multiplier = self.snake.get_score_multiplier()
        self.score += base_score * multiplier
        
        # Create particles
        self.create_food_particles()
        
        # Update statistics
        if self.game_stats:
            self.game_stats.food_eaten += 1
        
        # Spawn new food
        self.food = Food(self.grid_width, self.grid_height, self.snake.body)
        
        # Play sound
        if self.audio:
            self.audio.play_sound(AudioEvent.FOOD_EATEN)
    
    def eat_powerup(self, powerup: PowerUp):
        """Handle eating power-up."""
        self.snake.eat_powerup(powerup)
        
        # Create particles
        self.create_powerup_particles(powerup)
        
        # Update statistics
        if self.game_stats:
            self.game_stats.powerups_collected += 1
        
        # Play sound
        if self.audio:
            self.audio.play_sound(AudioEvent.POWER_UP_COLLECTED)
    
    def spawn_powerup(self):
        """Spawn power-ups randomly."""
        if not self.config.gameplay.power_ups_enabled:
            return
        
        if len(self.powerups) < 2 and random.random() < 0.005:
            powerup = PowerUp(self.grid_width, self.grid_height, self.snake.body)
            self.powerups.append(powerup)
    
    def create_food_particles(self):
        """Create particles when food is eaten."""
        if not self.food:
            return
        
        center_x = self.food.position.x * self.grid_size + self.grid_size // 2
        center_y = self.food.position.y * self.grid_size + self.grid_size // 2
        
        colors = [(255, 0, 0), (255, 100, 0), (255, 200, 0)]
        
        for _ in range(15):
            velocity = (random.uniform(-4, 4), random.uniform(-6, 2))
            color = random.choice(colors)
            particle = Particle(center_x, center_y, velocity, color, 45)
            self.particles.append(particle)
    
    def create_powerup_particles(self, powerup: PowerUp):
        """Create particles when power-up is collected."""
        center_x = powerup.position.x * self.grid_size + self.grid_size // 2
        center_y = powerup.position.y * self.grid_size + self.grid_size // 2
        
        color = powerup.properties[powerup.type]['color']
        
        for _ in range(20):
            velocity = (random.uniform(-5, 5), random.uniform(-7, 3))
            particle = Particle(center_x, center_y, velocity, color, 60, size=4)
            self.particles.append(particle)
    
    def generate_maze(self):
        """Generate maze for maze mode."""
        # Simple maze generation - add obstacles around the edges and some internal walls
        self.obstacles = []
        
        # Border obstacles (leaving some gaps)
        for x in range(self.grid_width):
            if x % 4 != 0:  # Leave gaps
                self.obstacles.append(Position(x, 0))
                self.obstacles.append(Position(x, self.grid_height - 1))
        
        for y in range(self.grid_height):
            if y % 4 != 0:
                self.obstacles.append(Position(0, y))
                self.obstacles.append(Position(self.grid_width - 1, y))
        
        # Internal obstacles
        for _ in range(self.grid_width * self.grid_height // 20):
            x = random.randint(2, self.grid_width - 3)
            y = random.randint(2, self.grid_height - 3)
            pos = Position(x, y)
            if pos not in self.snake.body and pos != self.food.position:
                self.obstacles.append(pos)
    
    def draw(self):
        """Draw everything."""
        # Clear screen
        self.screen.fill(self.config.get_theme_colors()['background'])
        
        # Draw background effects
        if self.config.theme.rainbow_background:
            self.draw_rainbow_background()
        
        # Draw game elements
        if self.state in [GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER]:
            self.draw_game()
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw UI
        game_state_data = None
        if self.snake and self.state != GameState.MENU:
            current_song = None
            if self.audio:
                song_info = self.audio.get_current_song_info()
                if song_info:
                    current_song = song_info.get('title', 'Unknown')
            
            effects = {}
            for effect, timer in self.snake.effects.items():
                if timer > 0 and effect != 'score_multiplier_timer':
                    effects[effect] = timer
            
            game_state_data = {
                'score': self.score,
                'length': len(self.snake.body),
                'speed': self.snake.get_current_speed(),
                'effects': effects,
                'current_song': current_song,
                'is_high_score': False  # Updated in game_over
            }
        
        self.ui.draw(game_state_data)
        
        # Debug info
        if self.config.developer.debug_mode:
            self.draw_debug_info()
        
        pygame.display.flip()
    
    def draw_rainbow_background(self):
        """Draw animated rainbow background."""
        strip_height = self.screen.get_height() // 30
        
        for i in range(30):
            hue = (self.bg_hue + i * 0.03) % 1.0
            # Simple color cycling
            r = int(127 + 127 * math.sin(hue * 2 * math.pi))
            g = int(127 + 127 * math.sin((hue + 0.33) * 2 * math.pi))
            b = int(127 + 127 * math.sin((hue + 0.66) * 2 * math.pi))
            
            # Make it darker for background
            color = (r // 8, g // 8, b // 8)
            
            pygame.draw.rect(self.screen, color, 
                           (0, i * strip_height, self.screen.get_width(), strip_height))
    
    def draw_game(self):
        """Draw game elements."""
        # Draw obstacles (maze mode)
        for obstacle in self.obstacles:
            x = obstacle.x * self.grid_size
            y = obstacle.y * self.grid_size
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (x, y, self.grid_size, self.grid_size))
        
        # Draw food
        if self.food:
            self.food.draw(self.screen, self.grid_size)
        
        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(self.screen, self.grid_size, self.small_font)
        
        # Draw snake
        if self.snake:
            self.snake.draw(self.screen, self.grid_size, self.particles)
    
    def draw_debug_info(self):
        """Draw debug information."""
        debug_info = [
            f"FPS: {self.clock.get_fps():.1f}",
            f"State: {self.state.value}",
            f"Snake Length: {len(self.snake.body) if self.snake else 0}",
            f"Particles: {len(self.particles)}",
            f"Power-ups: {len(self.powerups)}",
        ]
        
        y_offset = 10
        for info in debug_info:
            text = self.small_font.render(info, True, (255, 255, 0))
            self.screen.blit(text, (self.screen.get_width() - 200, y_offset))
            y_offset += 25
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.config.display.fullscreen = not self.config.display.fullscreen
        width, height, flags = self.config.get_display_mode()
        self.screen = pygame.display.set_mode((width, height), flags)
        
        # Recalculate grid
        self.grid_width = width // self.grid_size
        self.grid_height = height // self.grid_size
    
    def cleanup(self):
        """Clean up resources."""
        # Save configuration
        self.config.save_config()
        
        # Clean up audio
        if self.audio:
            self.audio.cleanup()
        
        pygame.quit()
        print("SNAKEIUM 2.1 shut down successfully")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SNAKEIUM 2.0 - GHOSTKITTY Edition")
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen mode")
    parser.add_argument("--no-music", action="store_true", help="Disable music")
    parser.add_argument("--config", help="Use custom config file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    try:
        # Initialize configuration
        config = ConfigManager(args.config)
        
        if args.fullscreen:
            config.display.fullscreen = True
        if args.no_music:
            config.audio.music_enabled = False
        if args.debug:
            config.developer.debug_mode = True
        
        # Start game
        game = Game(config)
        game.run()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
