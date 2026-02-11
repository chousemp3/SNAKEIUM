# Contributing to SNAKEIUM

Thank you for your interest in contributing to SNAKEIUM. This document covers guidelines for submitting issues, feature requests, and pull requests.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

---

## Code of Conduct

Be respectful and constructive in all interactions. SNAKEIUM is open to contributors from all backgrounds and experience levels.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Basic knowledge of Pygame

### Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/snakeium.git
   cd snakeium
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Verify the setup**

   ```bash
   python snakeium.py --test-mode
   pytest tests/ -v
   ```

## Making Changes

### Branch Naming

Use descriptive prefixes:

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code restructuring

### Workflow

1. Create a branch from `main`:

   ```bash
   git checkout -b feature/your-feature
   ```

2. Make changes in small, focused commits.

3. Run quality checks before pushing:

   ```bash
   black src/ tests/ snakeium.py
   flake8 src/ snakeium.py
   pytest tests/ -v
   ```

4. Push and open a pull request.

## Submitting Changes

### Pull Request Guidelines

- Write a clear title and description.
- Reference any related issues.
- Include screenshots or GIFs for visual changes.
- Update `CHANGELOG.md` with your changes.
- Add or update tests as needed.

### Pull Request Checklist

```
- [ ] Code follows project coding standards
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated
```

## Coding Standards

### Python Style

- Follow PEP 8.
- Use type hints where practical.
- Write docstrings for all public functions and classes (Google style).
- Maximum line length: 88 characters (Black default).
- No emoji characters in code or output strings.

### Game Development Guidelines

- Target 60 FPS.
- Handle all errors gracefully with fallbacks.
- Keep visual effects configurable.
- Test on multiple platforms when possible.

### Example

```python
def create_sprite(size: int, color: Tuple[int, int, int]) -> pygame.Surface:
    """Create a square sprite surface.

    Args:
        size: Width and height in pixels.
        color: RGB color tuple.

    Returns:
        The created sprite surface.
    """
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surface, color, (0, 0, size, size))
    return surface
```

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest --cov=snakeium tests/

# Specific test file
pytest tests/test_enhanced.py -v
```

### Writing Tests

- Use `pytest` fixtures for setup and teardown.
- Mock external dependencies (Pygame, filesystem).
- Cover edge cases and error conditions.
- Keep tests focused on one behavior each.

## Bug Reports

Use the [GitHub Issues](https://github.com/chousemp3/SNAKEIUM/issues) page with:

- Clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- System info: OS, Python version, Pygame version

## Feature Requests

Before opening a request:

1. Check existing issues to avoid duplicates.
2. Describe the use case clearly.
3. Consider performance and cross-platform impact.
4. Provide implementation ideas if possible.

## Areas for Contribution

**High priority**: Performance optimization, cross-platform testing, accessibility improvements.

**Medium priority**: Additional themes, multiplayer support, level editor, mobile controls.

**Low priority**: Additional power-ups, replay system, statistics dashboard.

---

Thank you for helping improve SNAKEIUM.
