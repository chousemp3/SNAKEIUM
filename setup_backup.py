#!/usr/bin/env python3
"""
Setup script for SNAKEIUM - GHOSTKITTY Edition
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "A modern retro Snake game with GHOSTKITTY music"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        return ["pygame>=2.1.0"]

setup(
    name="snakeium-ghostkitty",
    version="1.0.0",
    author="GHOSTKITTY",
    author_email="ghostkitty@example.com",
    description="A modern retro Snake game with 8-bit visuals and GHOSTKITTY music",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/GHOSTKITTY/SNAKEIUM",
    project_urls={
        "Bug Reports": "https://github.com/GHOSTKITTY/SNAKEIUM/issues",
        "Source": "https://github.com/GHOSTKITTY/SNAKEIUM",
        "Documentation": "https://github.com/GHOSTKITTY/SNAKEIUM#readme",
    },
    py_modules=["snakeium"],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
        "music": [
            "mutagen>=1.45.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Arcade",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    keywords="snake game retro 8bit pygame music ghostkitty arcade",
    entry_points={
        "console_scripts": [
            "snakeium=snakeium:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
