#!/usr/bin/env python3
"""
Windows-Safe SNAKEIUM Test
==========================
Basic syntax and import verification for Windows CI environments.
"""

import sys

def test_basic():
    """Test basic Python functionality"""
    print("🪟 Windows Compatibility Test")
    print("============================")
    
    print(f"🐍 Python {sys.version}")
    
    try:
        print("📦 Testing pygame import...")
        import pygame
        print(f"✅ Pygame {pygame.version.ver} available")
        
        print("📝 Testing syntax...")
        import py_compile
        py_compile.compile('snakeium.py', doraise=True)
        print("✅ Syntax check passed")
        
        print("✅ Windows compatibility verified!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_basic()
    sys.exit(0 if success else 1)
