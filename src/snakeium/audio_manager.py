"""
Enhanced Audio Manager for SNAKEIUM
Handles music playback, sound effects, and audio visualization.
"""

import pygame
import os
import random
import math
import threading
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
from enum import Enum

try:
    import mutagen
    from mutagen.mp3 import MP3
    from mutagen.id3 import ID3NoHeaderError
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False


class AudioEvent(Enum):
    FOOD_EATEN = "food_eaten"
    POWER_UP_COLLECTED = "power_up_collected"
    GAME_OVER = "game_over"
    LEVEL_UP = "level_up"
    MENU_SELECT = "menu_select"
    MENU_NAVIGATE = "menu_navigate"
    PAUSE = "pause"
    RESUME = "resume"


class MusicManager:
    """Enhanced music management with metadata support."""
    
    def __init__(self, music_folders: List[str] = None, shuffle: bool = True):
        self.music_folders = music_folders or []
        self.shuffle = shuffle
        self.music_files = []
        self.current_index = 0
        self.current_song = None
        self.is_playing = False
        self.volume = 0.7
        self.fade_duration = 1000  # milliseconds
        
        # Metadata cache
        self.metadata_cache = {}
        
        # Auto-detect music folders if none provided
        if not self.music_folders:
            self._auto_detect_music_folders()
        
        self._scan_music_files()
        
        if self.shuffle and self.music_files:
            random.shuffle(self.music_files)
    
    def _auto_detect_music_folders(self):
        """Auto-detect common music folder locations."""
        potential_folders = [
            os.path.expanduser("~/Music"),
            os.path.expanduser("~/Desktop/GHOSTKITTY MP3S"),
            "./music",
            "./assets/music",
            "C:/Users/music2/Desktop/GHOSTKITTY MP3S",  # Legacy path
        ]
        
        for folder in potential_folders:
            if os.path.exists(folder):
                self.music_folders.append(folder)
                print(f"Found music folder: {folder}")
    
    def _scan_music_files(self):
        """Scan for music files in specified folders."""
        supported_formats = ['.mp3', '.ogg', '.wav']
        
        for folder in self.music_folders:
            if not os.path.exists(folder):
                continue
                
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if any(file.lower().endswith(fmt) for fmt in supported_formats):
                        full_path = os.path.join(root, file)
                        self.music_files.append(full_path)
        
        print(f"Found {len(self.music_files)} music files")
    
    def get_metadata(self, file_path: str) -> Dict[str, str]:
        """Get metadata for a music file."""
        if not HAS_MUTAGEN:
            return {"title": os.path.basename(file_path), "artist": "Unknown", "album": "Unknown"}
        
        if file_path in self.metadata_cache:
            return self.metadata_cache[file_path]
        
        try:
            audio_file = mutagen.File(file_path)
            if audio_file is None:
                metadata = {"title": os.path.basename(file_path), "artist": "Unknown", "album": "Unknown"}
            else:
                metadata = {
                    "title": str(audio_file.get("TIT2", [os.path.basename(file_path)])[0] if audio_file.get("TIT2") else os.path.basename(file_path)),
                    "artist": str(audio_file.get("TPE1", ["Unknown"])[0] if audio_file.get("TPE1") else "Unknown"),
                    "album": str(audio_file.get("TALB", ["Unknown"])[0] if audio_file.get("TALB") else "Unknown"),
                    "duration": getattr(audio_file, 'info', type('', (), {'length': 0})).length
                }
            
            self.metadata_cache[file_path] = metadata
            return metadata
            
        except Exception as e:
            print(f"Warning: Error reading metadata for {file_path}: {e}")
            metadata = {"title": os.path.basename(file_path), "artist": "Unknown", "album": "Unknown"}
            self.metadata_cache[file_path] = metadata
            return metadata
    
    def play_next(self) -> Optional[str]:
        """Play the next song in the playlist."""
        if not self.music_files:
            return None
        
        try:
            # Fade out current song
            if self.is_playing:
                pygame.mixer.music.fadeout(self.fade_duration)
                time.sleep(self.fade_duration / 1000.0)
            
            # Get next song
            if self.shuffle:
                song_path = random.choice(self.music_files)
            else:
                song_path = self.music_files[self.current_index]
                self.current_index = (self.current_index + 1) % len(self.music_files)
            
            # Load and play
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)
            
            self.current_song = song_path
            self.is_playing = True
            
            return song_path
            
        except Exception as e:
            print(f"Warning: Error playing music: {e}")
            return None
    
    def set_volume(self, volume: float):
        """Set music volume (0.0 - 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def pause(self):
        """Pause music playback."""
        pygame.mixer.music.pause()
        self.is_playing = False
    
    def resume(self):
        """Resume music playback."""
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def stop(self):
        """Stop music playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def check_music(self) -> Optional[str]:
        """Check if current song has ended and play next."""
        if not pygame.mixer.music.get_busy() and self.is_playing:
            return self.play_next()
        return None


class SoundEffectManager:
    """Manages sound effects for game events."""
    
    def __init__(self):
        self.sounds = {}
        self.volume = 0.8
        self._generate_sound_effects()
    
    def _generate_sound_effects(self):
        """Generate procedural sound effects."""
        try:
            # Generate sound effects using pygame
            sample_rate = 22050
            
            # Food eaten sound (positive chirp)
            self.sounds[AudioEvent.FOOD_EATEN] = self._generate_chirp(440, 0.1, sample_rate)
            
            # Power-up collected (ascending arpeggio)
            self.sounds[AudioEvent.POWER_UP_COLLECTED] = self._generate_arpeggio([440, 554, 659, 880], 0.2, sample_rate)
            
            # Game over (descending tone)
            self.sounds[AudioEvent.GAME_OVER] = self._generate_descending_tone(0.5, sample_rate)
            
            # Menu sounds
            self.sounds[AudioEvent.MENU_SELECT] = self._generate_beep(660, 0.1, sample_rate)
            self.sounds[AudioEvent.MENU_NAVIGATE] = self._generate_beep(440, 0.05, sample_rate)
            
            # Pause/Resume
            self.sounds[AudioEvent.PAUSE] = self._generate_pause_sound(sample_rate)
            self.sounds[AudioEvent.RESUME] = self._generate_resume_sound(sample_rate)
            
            print("Sound effects generated successfully")
            
        except Exception as e:
            print(f"Warning: Error generating sound effects: {e}")
    
    def _generate_chirp(self, frequency: float, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a chirp sound effect."""
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            # Frequency sweep
            freq = frequency * (1 + 0.5 * (i / frames))
            # Amplitude envelope
            amplitude = 0.3 * (1 - i / frames)
            # Generate sample
            sample = int(amplitude * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
            arr.append([sample, sample])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', [item for sublist in arr for item in sublist]))
        return sound
    
    def _generate_arpeggio(self, frequencies: List[float], duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate an arpeggio sound effect."""
        note_duration = duration / len(frequencies)
        frames_per_note = int(note_duration * sample_rate)
        arr = []
        
        for freq in frequencies:
            for i in range(frames_per_note):
                amplitude = 0.3 * (1 - (i / frames_per_note) * 0.5)
                sample = int(amplitude * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
                arr.append([sample, sample])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', [item for sublist in arr for item in sublist]))
        return sound
    
    def _generate_descending_tone(self, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a descending tone for game over."""
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            # Descending frequency
            freq = 440 * (1 - 0.7 * (i / frames))
            amplitude = 0.4 * (1 - i / frames)
            sample = int(amplitude * 32767 * math.sin(2 * math.pi * freq * i / sample_rate))
            arr.append([sample, sample])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', [item for sublist in arr for item in sublist]))
        return sound
    
    def _generate_beep(self, frequency: float, duration: float, sample_rate: int) -> pygame.mixer.Sound:
        """Generate a simple beep."""
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            amplitude = 0.3 * (1 - i / frames)
            sample = int(amplitude * 32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
            arr.append([sample, sample])
        
        sound = pygame.sndarray.make_sound(pygame.array.array('i', [item for sublist in arr for item in sublist]))
        return sound
    
    def _generate_pause_sound(self, sample_rate: int) -> pygame.mixer.Sound:
        """Generate pause sound (two quick beeps)."""
        beep1 = self._generate_beep(440, 0.05, sample_rate)
        beep2 = self._generate_beep(440, 0.05, sample_rate)
        # Combine sounds with gap
        return beep1  # Simplified for now
    
    def _generate_resume_sound(self, sample_rate: int) -> pygame.mixer.Sound:
        """Generate resume sound (ascending beep)."""
        return self._generate_beep(660, 0.1, sample_rate)
    
    def play_sound(self, event: AudioEvent):
        """Play a sound effect for the given event."""
        if event in self.sounds:
            try:
                sound = self.sounds[event]
                sound.set_volume(self.volume)
                sound.play()
            except Exception as e:
                print(f"Warning: Error playing sound effect {event}: {e}")
    
    def set_volume(self, volume: float):
        """Set sound effects volume (0.0 - 1.0)."""
        self.volume = max(0.0, min(1.0, volume))


class AudioManager:
    """Main audio manager that coordinates music and sound effects."""
    
    def __init__(self, config_manager=None):
        self.config = config_manager
        
        # Initialize audio systems
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            print("Audio system initialized")
        except Exception as e:
            print(f"Failed to initialize audio: {e}")
            return
        
        # Initialize managers
        self.music_manager = None
        self.sfx_manager = SoundEffectManager()
        
        # Get settings from config
        if config_manager:
            audio_settings = config_manager.audio
            if audio_settings.music_enabled:
                music_folders = [audio_settings.music_folder] if audio_settings.music_folder else []
                self.music_manager = MusicManager(music_folders, audio_settings.shuffle_music)
                if self.music_manager:
                    self.music_manager.set_volume(audio_settings.music_volume)
            
            self.sfx_manager.set_volume(audio_settings.sfx_volume)
        else:
            # Default initialization
            self.music_manager = MusicManager()
    
    def play_music(self) -> Optional[str]:
        """Start playing music."""
        if self.music_manager:
            return self.music_manager.play_next()
        return None
    
    def skip_track(self) -> Optional[str]:
        """Skip to next track."""
        if self.music_manager:
            return self.music_manager.play_next()
        return None
    
    def pause_music(self):
        """Pause music playback."""
        if self.music_manager:
            self.music_manager.pause()
    
    def resume_music(self):
        """Resume music playback."""
        if self.music_manager:
            self.music_manager.resume()
    
    def stop_music(self):
        """Stop music playback."""
        if self.music_manager:
            self.music_manager.stop()
    
    def set_music_volume(self, volume: float):
        """Set music volume."""
        if self.music_manager:
            self.music_manager.set_volume(volume)
        if self.config:
            self.config.audio.music_volume = volume
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume."""
        self.sfx_manager.set_volume(volume)
        if self.config:
            self.config.audio.sfx_volume = volume
    
    def play_sound(self, event: AudioEvent):
        """Play a sound effect."""
        if self.config and not self.config.audio.sound_effects_enabled:
            return
        self.sfx_manager.play_sound(event)
    
    def check_music(self) -> Optional[str]:
        """Check if music needs to continue to next track."""
        if self.music_manager:
            return self.music_manager.check_music()
        return None
    
    def get_current_song_info(self) -> Optional[Dict[str, str]]:
        """Get information about the currently playing song."""
        if self.music_manager and self.music_manager.current_song:
            return self.music_manager.get_metadata(self.music_manager.current_song)
        return None
    
    def cleanup(self):
        """Clean up audio resources."""
        try:
            pygame.mixer.quit()
            print("Audio system cleaned up")
        except:
            pass
