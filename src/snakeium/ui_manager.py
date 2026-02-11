"""
UI Manager for SNAKEIUM
Handles all user interface elements, menus, HUD, and visual feedback.
"""

import pygame
import math
import time
from typing import List, Tuple, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass

from .config_manager import GameMode, Theme
from .audio_manager import AudioEvent


class MenuState(Enum):
    MAIN = "main"
    GAME_MODE_SELECT = "game_mode_select"
    SETTINGS = "settings"
    HIGH_SCORES = "high_scores"
    CONTROLS = "controls"
    AUDIO = "audio"
    GRAPHICS = "graphics"
    ABOUT = "about"


@dataclass
class MenuItem:
    text: str
    action: str
    value: Any = None
    enabled: bool = True


class UIElement:
    """Base class for UI elements."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
    
    def update(self):
        pass
    
    def draw(self, screen: pygame.Surface):
        pass
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        return False


class Button(UIElement):
    """Clickable button UI element."""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 font: pygame.font.Font, colors: Dict[str, Tuple[int, int, int]]):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font
        self.colors = colors
        self.hovered = False
        self.pressed = False
        self.callback = None
    
    def set_callback(self, callback):
        self.callback = callback
    
    def update(self):
        # Check mouse hover
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = (self.x <= mouse_pos[0] <= self.x + self.width and
                       self.y <= mouse_pos[1] <= self.y + self.height)
    
    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        
        # Choose colors based on state
        if self.pressed:
            bg_color = self.colors.get('pressed', self.colors['normal'])
            text_color = self.colors.get('text_pressed', self.colors['text'])
        elif self.hovered:
            bg_color = self.colors.get('hover', self.colors['normal'])
            text_color = self.colors.get('text_hover', self.colors['text'])
        else:
            bg_color = self.colors['normal']
            text_color = self.colors['text']
        
        # Draw button background
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.colors.get('border', text_color), 
                        (self.x, self.y, self.width, self.height), 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, 
                                                 self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled or not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.hovered and self.callback:
                self.pressed = False
                self.callback()
                return True
            self.pressed = False
        
        return False


class Slider(UIElement):
    """Slider for numeric values."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 min_val: float, max_val: float, initial_val: float,
                 colors: Dict[str, Tuple[int, int, int]]):
        super().__init__(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.colors = colors
        self.dragging = False
        self.callback = None
    
    def set_callback(self, callback):
        self.callback = callback
    
    def get_knob_x(self) -> int:
        return int(self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * (self.width - 20))
    
    def set_value_from_x(self, mouse_x: int):
        relative_x = mouse_x - self.x
        ratio = max(0, min(1, relative_x / (self.width - 20)))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        if self.callback:
            self.callback(self.value)
    
    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        
        # Draw track
        track_y = self.y + self.height // 2
        pygame.draw.line(screen, self.colors['track'], 
                        (self.x, track_y), (self.x + self.width - 20, track_y), 4)
        
        # Draw knob
        knob_x = self.get_knob_x()
        knob_color = self.colors['knob_hover'] if self.dragging else self.colors['knob']
        pygame.draw.circle(screen, knob_color, (knob_x + 10, track_y), 8)
        pygame.draw.circle(screen, self.colors.get('border', (255, 255, 255)), 
                          (knob_x + 10, track_y), 8, 2)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled or not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            knob_x = self.get_knob_x()
            mouse_x, mouse_y = event.pos
            knob_rect = pygame.Rect(knob_x, self.y, 20, self.height)
            if knob_rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_value_from_x(event.pos[0])
            return True
        
        return False


class MenuManager:
    """Manages game menus and navigation."""
    
    def __init__(self, screen: pygame.Surface, config_manager, audio_manager):
        self.screen = screen
        self.config = config_manager
        self.audio = audio_manager
        
        # Menu state
        self.current_menu = MenuState.MAIN
        self.selected_index = 0
        
        # Fonts
        self.large_font = pygame.font.Font(None, 64)
        self.medium_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        # Colors from theme
        self.colors = self.config.get_theme_colors()
        
        # Menu items
        self.menu_items = {
            MenuState.MAIN: [
                MenuItem("Start Game", "start_game"),
                MenuItem("Game Modes", "menu", MenuState.GAME_MODE_SELECT),
                MenuItem("High Scores", "menu", MenuState.HIGH_SCORES),
                MenuItem("Settings", "menu", MenuState.SETTINGS),
                MenuItem("About", "menu", MenuState.ABOUT),
                MenuItem("Quit", "quit")
            ],
            MenuState.GAME_MODE_SELECT: [
                MenuItem("Classic", "start_game", GameMode.CLASSIC),
                MenuItem("Time Attack", "start_game", GameMode.TIME_ATTACK),
                MenuItem("Survival", "start_game", GameMode.SURVIVAL),
                MenuItem("Maze Mode", "start_game", GameMode.MAZE),
                MenuItem("Challenge", "start_game", GameMode.CHALLENGE),
                MenuItem("Back", "menu", MenuState.MAIN)
            ],
            MenuState.SETTINGS: [
                MenuItem("Controls", "menu", MenuState.CONTROLS),
                MenuItem("Audio", "menu", MenuState.AUDIO),
                MenuItem("Graphics", "menu", MenuState.GRAPHICS),
                MenuItem("Reset to Defaults", "reset_config"),
                MenuItem("Back", "menu", MenuState.MAIN)
            ],
            MenuState.HIGH_SCORES: [
                MenuItem("Back", "menu", MenuState.MAIN)
            ],
            MenuState.CONTROLS: [
                MenuItem("Configure Keys", "configure_controls"),
                MenuItem("Reset Controls", "reset_controls"),
                MenuItem("Back", "menu", MenuState.SETTINGS)
            ],
            MenuState.AUDIO: [
                MenuItem("Back", "menu", MenuState.SETTINGS)
            ],
            MenuState.GRAPHICS: [
                MenuItem("Back", "menu", MenuState.SETTINGS)
            ],
            MenuState.ABOUT: [
                MenuItem("Back", "menu", MenuState.MAIN)
            ]
        }
        
        # UI elements
        self.ui_elements = []
        self.build_ui_elements()
    
    def build_ui_elements(self):
        """Build UI elements for current menu."""
        self.ui_elements.clear()
        
        if self.current_menu == MenuState.AUDIO:
            # Music volume slider
            music_slider = Slider(400, 300, 200, 30, 0.0, 1.0, 
                                 self.config.audio.music_volume, self.colors)
            music_slider.set_callback(lambda val: self.audio.set_music_volume(val))
            self.ui_elements.append(music_slider)
            
            # SFX volume slider
            sfx_slider = Slider(400, 350, 200, 30, 0.0, 1.0, 
                               self.config.audio.sfx_volume, self.colors)
            sfx_slider.set_callback(lambda val: self.audio.set_sfx_volume(val))
            self.ui_elements.append(sfx_slider)
        
        elif self.current_menu == MenuState.GRAPHICS:
            # Resolution buttons
            resolutions = [(1280, 720), (1400, 900), (1920, 1080)]
            for i, (w, h) in enumerate(resolutions):
                button = Button(300, 200 + i * 60, 200, 40, f"{w}x{h}", 
                               self.medium_font, self.get_button_colors())
                button.set_callback(lambda w=w, h=h: self.set_resolution(w, h))
                self.ui_elements.append(button)
    
    def get_button_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Get button color scheme."""
        return {
            'normal': (50, 50, 50),
            'hover': self.colors['neon_blue'],
            'pressed': self.colors['neon_purple'],
            'text': self.colors['ui_text'],
            'border': self.colors['neon_green']
        }
    
    def set_resolution(self, width: int, height: int):
        """Set display resolution."""
        self.config.display.width = width
        self.config.display.height = height
        # Note: This would typically trigger a display mode change
    
    def update(self):
        """Update menu state and UI elements."""
        for element in self.ui_elements:
            element.update()
    
    def draw(self):
        """Draw the current menu."""
        # Clear screen with background
        self.screen.fill(self.colors['background'])
        
        # Draw animated background
        self.draw_animated_background()
        
        # Draw menu content
        if self.current_menu == MenuState.MAIN:
            self.draw_main_menu()
        elif self.current_menu == MenuState.HIGH_SCORES:
            self.draw_high_scores()
        elif self.current_menu == MenuState.AUDIO:
            self.draw_audio_menu()
        elif self.current_menu == MenuState.GRAPHICS:
            self.draw_graphics_menu()
        elif self.current_menu == MenuState.ABOUT:
            self.draw_about_menu()
        else:
            self.draw_generic_menu()
        
        # Draw UI elements
        for element in self.ui_elements:
            element.draw(self.screen)
    
    def draw_animated_background(self):
        """Draw animated background effects."""
        if not self.config.theme.rainbow_background:
            return
        
        # Rainbow background strips
        hue = (time.time() * 0.1) % 1.0
        strip_height = self.screen.get_height() // 20
        
        for i in range(20):
            color_hue = (hue + i * 0.05) % 1.0
            r, g, b = [int(x * 255) for x in pygame.Color(0).hsva[:3]]
            color = pygame.Color(0)
            color.hsva = (color_hue * 360, 30, 20, 100)
            pygame.draw.rect(self.screen, color, 
                           (0, i * strip_height, self.screen.get_width(), strip_height))
    
    def draw_main_menu(self):
        """Draw the main menu."""
        # Title
        title_text = self.large_font.render("SNAKEIUM 2.1", True, self.colors['neon_green'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.medium_font.render("GHOSTKITTY Edition", True, self.colors['neon_pink'])
        subtitle_rect = subtitle_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu items
        self.draw_menu_items(MenuState.MAIN, 300)
    
    def draw_high_scores(self):
        """Draw high scores menu."""
        title_text = self.large_font.render("High Scores", True, self.colors['neon_yellow'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Display scores for each mode
        y_offset = 180
        for mode in GameMode:
            mode_text = self.medium_font.render(mode.value.title(), True, self.colors['ui_text'])
            self.screen.blit(mode_text, (100, y_offset))
            
            scores = self.config.get_high_scores(mode.value, 5)
            for i, score in enumerate(scores):
                score_text = self.small_font.render(f"{i+1}. {score:,}", True, self.colors['neon_green'])
                self.screen.blit(score_text, (300, y_offset + i * 25))
            
            y_offset += 150
        
        # Back button
        self.draw_menu_items(MenuState.HIGH_SCORES, y_offset)
    
    def draw_audio_menu(self):
        """Draw audio settings menu."""
        title_text = self.large_font.render("Audio Settings", True, self.colors['neon_blue'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Music volume
        music_text = self.medium_font.render("Music Volume", True, self.colors['ui_text'])
        self.screen.blit(music_text, (100, 300))
        
        # SFX volume
        sfx_text = self.medium_font.render("Sound Effects", True, self.colors['ui_text'])
        self.screen.blit(sfx_text, (100, 350))
        
        # Current song info
        song_info = self.audio.get_current_song_info()
        if song_info:
            info_text = self.small_font.render(f"{song_info['title']} - {song_info['artist']}", 
                                             True, self.colors['neon_pink'])
            self.screen.blit(info_text, (100, 450))
        
        # Back button
        self.draw_menu_items(MenuState.AUDIO, 500)
    
    def draw_graphics_menu(self):
        """Draw graphics settings menu."""
        title_text = self.large_font.render("Graphics Settings", True, self.colors['neon_purple'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Current resolution
        res_text = self.medium_font.render(f"Resolution: {self.config.display.width}x{self.config.display.height}", 
                                         True, self.colors['ui_text'])
        self.screen.blit(res_text, (100, 150))
        
        # Back button
        self.draw_menu_items(MenuState.GRAPHICS, 400)
    
    def draw_about_menu(self):
        """Draw about menu."""
        title_text = self.large_font.render("About SNAKEIUM", True, self.colors['neon_orange'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        about_lines = [
            "SNAKEIUM 2.0 - GHOSTKITTY Edition",
            "A modern retro Snake game with epic music",
            "",
            "Created by: GHOSTKITTY APPS",
            "Version: 2.0.0",
            "License: MIT",
            "",
            "Made for the retro gaming community."
        ]
        
        y_offset = 180
        for line in about_lines:
            if line:
                text = self.small_font.render(line, True, self.colors['ui_text'])
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 30
        
        # Back button
        self.draw_menu_items(MenuState.ABOUT, y_offset + 50)
    
    def draw_generic_menu(self):
        """Draw a generic menu layout."""
        # Title
        title = self.current_menu.value.replace('_', ' ').title()
        title_text = self.large_font.render(title, True, self.colors['neon_green'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Menu items
        self.draw_menu_items(self.current_menu, 250)
    
    def draw_menu_items(self, menu_state: MenuState, y_start: int):
        """Draw menu items for the given state."""
        items = self.menu_items.get(menu_state, [])
        
        for i, item in enumerate(items):
            color = self.colors['neon_green'] if i == self.selected_index else self.colors['ui_text']
            if not item.enabled:
                color = (100, 100, 100)
            
            # Selection indicator
            prefix = "> " if i == self.selected_index else "  "
            
            text = self.medium_font.render(f"{prefix}{item.text}", True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y_start + i * 50))
            self.screen.blit(text, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle menu events and return action if any."""
        # Let UI elements handle events first
        for element in self.ui_elements:
            if element.handle_event(event):
                return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items[self.current_menu])
                self.audio.play_sound(AudioEvent.MENU_NAVIGATE)
                
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items[self.current_menu])
                self.audio.play_sound(AudioEvent.MENU_NAVIGATE)
                
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.select_current_item()
                
            elif event.key == pygame.K_ESCAPE:
                return self.go_back()
        
        return None
    
    def select_current_item(self) -> Optional[str]:
        """Select the currently highlighted menu item."""
        items = self.menu_items[self.current_menu]
        if 0 <= self.selected_index < len(items):
            item = items[self.selected_index]
            if not item.enabled:
                return None
            
            self.audio.play_sound(AudioEvent.MENU_SELECT)
            
            if item.action == "menu":
                self.navigate_to_menu(item.value)
            elif item.action == "start_game":
                return f"start_game:{item.value.value if item.value else 'classic'}"
            elif item.action == "quit":
                return "quit"
            elif item.action == "reset_config":
                self.config.reset_to_defaults()
                self.config.save_config()
            
        return None
    
    def navigate_to_menu(self, menu_state: MenuState):
        """Navigate to a different menu."""
        self.current_menu = menu_state
        self.selected_index = 0
        self.build_ui_elements()
    
    def go_back(self) -> Optional[str]:
        """Go back to previous menu or quit."""
        if self.current_menu == MenuState.MAIN:
            return "quit"
        elif self.current_menu in [MenuState.CONTROLS, MenuState.AUDIO, MenuState.GRAPHICS]:
            self.navigate_to_menu(MenuState.SETTINGS)
        else:
            self.navigate_to_menu(MenuState.MAIN)
        return None


class HUD:
    """Heads-up display for in-game UI."""
    
    def __init__(self, screen: pygame.Surface, config_manager):
        self.screen = screen
        self.config = config_manager
        self.colors = config_manager.get_theme_colors()
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Animation state
        self.pulse_timer = 0
    
    def update(self):
        """Update HUD animations."""
        self.pulse_timer += 0.1
    
    def draw_game_hud(self, score: int, length: int, speed: int, effects: Dict[str, int], 
                     current_song: Optional[str] = None):
        """Draw the main game HUD."""
        # Score
        score_text = self.font.render(f"Score: {score:,}", True, self.colors['ui_text'])
        self.screen.blit(score_text, (10, 10))
        
        # Snake length
        length_text = self.font.render(f"Length: {length}", True, self.colors['ui_text'])
        self.screen.blit(length_text, (10, 50))
        
        # Speed
        speed_text = self.font.render(f"Speed: {speed}", True, self.colors['ui_text'])
        self.screen.blit(speed_text, (10, 90))
        
        # Active effects
        y_offset = 130
        for effect, timer in effects.items():
            if timer > 0:
                pulse = abs(math.sin(self.pulse_timer))
                alpha = int(255 * (0.7 + 0.3 * pulse))
                
                effect_color = {
                    'speed_boost': self.colors['neon_blue'],
                    'score_multiplier': self.colors['neon_yellow'],
                    'rainbow_mode': self.colors['neon_purple']
                }.get(effect, self.colors['ui_text'])
                
                effect_text = self.small_font.render(f"{effect.upper()}!", True, effect_color)
                self.screen.blit(effect_text, (10, y_offset))
                y_offset += 25
        
        # Current song
        if current_song:
            song_text = self.small_font.render(f"{current_song}", True, self.colors['neon_pink'])
            self.screen.blit(song_text, (10, self.screen.get_height() - 30))
        
        # FPS counter (if enabled)
        if self.config.display.show_fps:
            fps = pygame.time.Clock().get_fps()
            fps_text = self.small_font.render(f"FPS: {fps:.1f}", True, self.colors['ui_text'])
            fps_rect = fps_text.get_rect(topright=(self.screen.get_width() - 10, 10))
            self.screen.blit(fps_text, fps_rect)
    
    def draw_pause_overlay(self):
        """Draw pause screen overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font.render("PAUSED", True, self.colors['neon_yellow'])
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, 
                                                self.screen.get_height() // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        continue_text = self.small_font.render("Press SPACE to continue", True, self.colors['ui_text'])
        continue_rect = continue_text.get_rect(center=(self.screen.get_width() // 2, 
                                                      self.screen.get_height() // 2 + 50))
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over(self, final_score: int, is_high_score: bool):
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font.render("GAME OVER", True, self.colors['neon_orange'])
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, 
                                                        self.screen.get_height() // 2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {final_score:,}", True, self.colors['ui_text'])
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 
                                                self.screen.get_height() // 2))
        self.screen.blit(score_text, score_rect)
        
        # High score notification
        if is_high_score:
            hs_text = self.small_font.render("NEW HIGH SCORE!", True, self.colors['neon_yellow'])
            hs_rect = hs_text.get_rect(center=(self.screen.get_width() // 2, 
                                              self.screen.get_height() // 2 + 40))
            self.screen.blit(hs_text, hs_rect)
        
        # Instructions
        continue_text = self.small_font.render("Press R to restart or ESC for menu", True, self.colors['ui_text'])
        continue_rect = continue_text.get_rect(center=(self.screen.get_width() // 2, 
                                                      self.screen.get_height() // 2 + 80))
        self.screen.blit(continue_text, continue_rect)


class UIManager:
    """Main UI manager that coordinates all UI systems."""
    
    def __init__(self, screen: pygame.Surface, config_manager, audio_manager):
        self.screen = screen
        self.config = config_manager
        self.audio = audio_manager
        
        # UI components
        self.menu_manager = MenuManager(screen, config_manager, audio_manager)
        self.hud = HUD(screen, config_manager)
        
        # Current state
        self.current_state = "menu"  # "menu", "game", "pause", "game_over"
    
    def update(self):
        """Update UI components."""
        if self.current_state == "menu":
            self.menu_manager.update()
        
        self.hud.update()
    
    def draw(self, game_state: Optional[Dict] = None):
        """Draw UI based on current state."""
        if self.current_state == "menu":
            self.menu_manager.draw()
        elif self.current_state == "game" and game_state:
            self.hud.draw_game_hud(
                score=game_state.get('score', 0),
                length=game_state.get('length', 1),
                speed=game_state.get('speed', 1),
                effects=game_state.get('effects', {}),
                current_song=game_state.get('current_song')
            )
        elif self.current_state == "pause":
            if game_state:
                self.hud.draw_game_hud(
                    score=game_state.get('score', 0),
                    length=game_state.get('length', 1),
                    speed=game_state.get('speed', 1),
                    effects=game_state.get('effects', {}),
                    current_song=game_state.get('current_song')
                )
            self.hud.draw_pause_overlay()
        elif self.current_state == "game_over" and game_state:
            self.hud.draw_game_over(
                final_score=game_state.get('score', 0),
                is_high_score=game_state.get('is_high_score', False)
            )
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle UI events and return action if any."""
        if self.current_state == "menu":
            return self.menu_manager.handle_event(event)
        return None
    
    def set_state(self, state: str):
        """Set the current UI state."""
        self.current_state = state
        if state == "menu":
            self.menu_manager.navigate_to_menu(MenuState.MAIN)
