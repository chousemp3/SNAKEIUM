"""
SNAKEIUM Installation and Setup Script
=====================================

This script provides automated installation and setup for SNAKEIUM - GHOSTKITTY Edition.
Handles dependencies, music setup, and platform-specific configurations.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Ensure Python 3.8+ is being used."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[OK] Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("[FAIL] Failed to install dependencies")
        sys.exit(1)

def setup_music_directory():
    """Create music directory structure if needed."""
    music_dir = Path("music")
    if not music_dir.exists():
        music_dir.mkdir()
        print("[OK] Created music directory")
        print("  Place your GHOSTKITTY MP3 files in the 'music' folder")
    else:
        music_files = list(music_dir.glob("*.mp3"))
        print(f"[OK] Found {len(music_files)} music files")

def check_system_compatibility():
    """Check system compatibility and provide warnings."""
    system = platform.system()
    print(f"Operating System: {system}")

    if system == "Linux":
        print("  Linux users may need: sudo apt-get install python3-pygame")
    elif system == "Darwin":  # macOS
        print("  macOS users may need: brew install pygame")
    elif system == "Windows":
        print("  Windows compatibility confirmed")

def create_launcher_scripts():
    """Create platform-specific launcher scripts."""
    system = platform.system()
    
    if system == "Windows":
        with open("launch_snakeium.bat", "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("title SNAKEIUM - GHOSTKITTY Edition\n")
            f.write("python snakeium.py\n")
            f.write("pause\n")
        print("[OK] Created Windows launcher: launch_snakeium.bat")
    
    else:  # Unix-like systems
        with open("launch_snakeium.sh", "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting SNAKEIUM - GHOSTKITTY Edition...'\n")
            f.write("python3 snakeium.py\n")
        
        # Make executable
        os.chmod("launch_snakeium.sh", 0o755)
        print("[OK] Created Unix launcher: launch_snakeium.sh")

def main():
    """Main setup function."""
    print("SNAKEIUM - GHOSTKITTY Edition Setup")
    print("=" * 40)

    check_python_version()
    check_system_compatibility()
    install_dependencies()
    setup_music_directory()
    create_launcher_scripts()

    print("\nSetup completed successfully.")
    print("\nTo start the game:")
    print("  python snakeium.py")
    if platform.system() == "Windows":
        print("  OR double-click: launch_snakeium.bat")
    else:
        print("  OR run: ./launch_snakeium.sh")

    print("\nAdd GHOSTKITTY MP3 files to the 'music' folder for background music.")

if __name__ == "__main__":
    main()
