# Contributing to SNAKEIUM

Thank you for your interest in contributing to SNAKEIUM! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

Please be respectful and constructive in all interactions. We want SNAKEIUM to be welcoming to contributors from all backgrounds.

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Git
- Basic knowledge of pygame
- Familiarity with game development concepts

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/snakeium.git
   cd snakeium
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pytest black flake8
   ```

3. **Test the setup**
   ```bash
   python snakeium.py --debug
   ```

## 🔧 Making Changes

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/awesome-new-feature
   ```

2. **Make your changes**
   - Keep commits small and focused
   - Write clear commit messages
   - Test your changes thoroughly

3. **Run quality checks**
   ```bash
   # Format code
   black snakeium.py
   
   # Check for issues
   flake8 snakeium.py
   
   # Run tests
   pytest tests/
   ```

## 📝 Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Update CHANGELOG.md** with your changes
4. **Create pull request** with:
   - Clear title and description
   - Reference any related issues
   - Include screenshots/GIFs for visual changes

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] Updated documentation

## Screenshots
If applicable, add screenshots or GIFs
```

## 🎨 Coding Standards

### Python Style
- Follow PEP 8
- Use type hints where possible
- Write docstrings for functions and classes
- Keep line length under 88 characters

### Game Development Guidelines
- Maintain 120 FPS target
- Handle errors gracefully
- Optimize for performance
- Keep visual effects configurable

### Example Code Style
```python
def create_sprite(size: int, color: Tuple[int, int, int]) -> pygame.Surface:
    """Create a sprite surface with specified size and color.
    
    Args:
        size: Size in pixels for square sprite
        color: RGB color tuple
        
    Returns:
        pygame.Surface: The created sprite surface
    """
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surface, color, (0, 0, size, size))
    return surface
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=snakeium

# Run specific test file
pytest tests/test_music.py
```

### Writing Tests
- Test new features and bug fixes
- Use pytest fixtures for setup
- Mock external dependencies
- Test edge cases and error conditions

### Test Structure
```python
import pytest
from snakeium import MusicManager

def test_music_manager_initialization():
    """Test MusicManager initializes correctly."""
    manager = MusicManager("test_folder")
    assert manager.playlist == []
    assert manager.current_song is None
```

## 📚 Documentation

### Docstring Format
Use Google-style docstrings:

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """One line summary.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2 with default
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
```

### README Updates
- Keep README.md current with new features
- Update command-line options
- Add examples for new functionality

## 🎯 Areas for Contribution

### High Priority
- [ ] Performance optimizations
- [ ] Cross-platform testing
- [ ] Additional music format support
- [ ] Mobile/touch controls
- [ ] Accessibility improvements

### Medium Priority
- [ ] High score system
- [ ] Additional visual effects
- [ ] Custom themes
- [ ] Multiplayer support
- [ ] Level editor

### Low Priority
- [ ] Additional power-ups
- [ ] Achievement system
- [ ] Replay system
- [ ] Statistics tracking

## 💡 Feature Requests

When suggesting new features:

1. **Check existing issues** first
2. **Describe the use case** clearly
3. **Consider performance impact**
4. **Provide implementation ideas** if possible
5. **Include mockups/examples** for UI changes

## 🐛 Bug Reports

When reporting bugs:

1. **Use the issue template**
2. **Provide reproduction steps**
3. **Include system information**
4. **Add error messages/logs**
5. **Attach screenshots if relevant**

### Bug Report Template
```markdown
**Describe the bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**System Information:**
 - OS: [e.g. Windows 10]
 - Python version: [e.g. 3.9.7]
 - Pygame version: [e.g. 2.1.0]

**Additional context**
Any other context about the problem.
```

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: Tag maintainers for review help

## 🎉 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Given credit in commit messages

Thank you for helping make SNAKEIUM awesome! 🐍✨
