#!/usr/bin/env python3
"""
Setup script for SNAKEIUM 2.1 - GHOSTKITTY Edition
Enhanced modular Snake game with advanced features
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "A modern retro Snake game with GHOSTKITTY music - Enhanced 2.1 Edition"

# Read requirements
def read_requirements(filename="requirements.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            # Filter out commented dev dependencies
            return [line for line in lines if not line.startswith("# ")]
    except:
        return ["pygame>=2.5.0", "numpy>=1.24.0", "mutagen>=1.47.0"]

# Get version from package
def get_version():
    try:
        with open("src/snakeium/__init__.py", "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split('"')[1]
    except:
        pass
    return "2.0.0"

setup(
    name="snakeium-ghostkitty",
    version=get_version(),
    author="GHOSTKITTY APPS",
    author_email="ghostkitty@snakeium.dev",
    description="A modern retro Snake game with enhanced features and GHOSTKITTY music",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/chousemp3/SNAKEIUM",
    project_urls={
        "Bug Reports": "https://github.com/chousemp3/SNAKEIUM/issues",
        "Source": "https://github.com/chousemp3/SNAKEIUM",
        "Documentation": "https://github.com/chousemp3/SNAKEIUM#readme",
        "Changelog": "https://github.com/chousemp3/SNAKEIUM/blob/main/CHANGELOG.md",
        "Discussions": "https://github.com/chousemp3/SNAKEIUM/discussions",
    },
    
    # Package configuration
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    
    # Entry points
    entry_points={
        "console_scripts": [
            "snakeium=snakeium.game_engine:main",
            "snakeium-game=snakeium.game_engine:main",
        ],
    },
    
    # Dependencies
    python_requires=">=3.8",
    install_requires=read_requirements(),
    
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "audio": [
            "mutagen>=1.47.0",
        ],
        "performance": [
            "psutil>=5.9.0",
            "memory-profiler>=0.61.0",
        ],
        "packaging": [
            "pyinstaller>=5.13.0",
            "cx-Freeze>=6.15.0",
        ],
        "all": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "mutagen>=1.47.0",
            "psutil>=5.9.0",
            "memory-profiler>=0.61.0",
            "pyinstaller>=5.13.0",
            "cx-Freeze>=6.15.0",
        ],
    },
    
    # Package data
    package_data={
        "snakeium": [
            "assets/*",
            "config/*.json",
            "themes/*.json",
        ],
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Arcade",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    
    keywords=[
        "snake", "game", "retro", "arcade", "pygame", "music", 
        "ghostkitty", "8bit", "pixel", "rainbow", "effects"
    ],
    
    # Platform specific
    platforms=["any"],
    
    zip_safe=False,
)
