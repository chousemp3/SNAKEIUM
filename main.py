#!/usr/bin/env python3
"""
🐍 SNAKEIUM 2.0 - GHOSTKITTY Edition 🎵
=======================================

Main entry point for the enhanced Snake game.
Can run either the new modular version or legacy version for compatibility.

Usage:
    python main.py              # Run SNAKEIUM 2.0
    python main.py --legacy     # Run original SNAKEIUM 1.0
    python main.py --help       # Show help
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def run_legacy():
    """Run the original SNAKEIUM 1.0"""
    print("🐍 Loading SNAKEIUM 1.0 (Legacy Mode)")
    
    # Import and run legacy version
    legacy_path = Path(__file__).parent / "legacy"
    sys.path.insert(0, str(legacy_path))
    
    try:
        import snakeium as legacy_snakeium
        # Run the legacy main function
        if hasattr(legacy_snakeium, 'main'):
            legacy_snakeium.main()
        else:
            # Fallback: create and run game
            game = legacy_snakeium.Game()
            game.run()
    except ImportError as e:
        print(f"❌ Failed to import legacy version: {e}")
        print("💡 Try running: python legacy/snakeium.py")
        sys.exit(1)

def run_enhanced():
    """Run the enhanced SNAKEIUM 2.0"""
    print("🐍 Loading SNAKEIUM 2.0 (Enhanced Mode)")
    
    try:
        from snakeium.game_engine import main as enhanced_main
        enhanced_main()
    except ImportError as e:
        print(f"❌ Failed to import enhanced version: {e}")
        print("💡 Make sure you have pygame installed: pip install pygame")
        print("💡 Or try legacy mode: python main.py --legacy")
        sys.exit(1)

def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="🐍 SNAKEIUM - Modern Retro Snake Game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run SNAKEIUM 2.0
  python main.py --legacy           # Run original version
  python main.py --fullscreen      # Start in fullscreen
  python main.py --no-music        # Disable music
  python main.py --config my.json  # Use custom config

Visit: https://github.com/chousemp3/SNAKEIUM
        """
    )
    
    parser.add_argument(
        "--legacy", 
        action="store_true",
        help="Run the original SNAKEIUM 1.0 (single-file version)"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="SNAKEIUM 2.0.0 - GHOSTKITTY Edition"
    )
    
    # Enhanced version arguments
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen mode")
    parser.add_argument("--no-music", action="store_true", help="Disable music")
    parser.add_argument("--config", help="Use custom config file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Show banner
    print("=" * 60)
    print("🐍 SNAKEIUM - GHOSTKITTY Edition 🎵")
    print("=" * 60)
    print("A modern retro Snake game with epic music and effects!")
    print("Made with 💜 by GHOSTKITTY APPS")
    print("=" * 60)
    
    if args.legacy:
        run_legacy()
    else:
        run_enhanced()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("💡 Try running with --legacy for the original version")
        sys.exit(1)
