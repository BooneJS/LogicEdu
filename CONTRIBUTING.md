# Contributing to ManimLogic

Thank you for your interest in contributing to ManimLogic! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/manimlogic.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install in development mode: `pip install -e .`
6. Install development dependencies: `pip install -r requirements-dev.txt`

## Development Setup

### Prerequisites
- Python 3.13 or higher
- Manim 0.19.0 or higher

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep line length under 88 characters (Black formatter default)

### Testing
- Write tests for new components in `tests/`
- Run tests: `pytest`
- Ensure all tests pass before submitting a PR

## Adding New Components

### Logic Gates
1. Add the gate type to `LogicType` enum in `manimlogic/components/logic_gates.py`
2. Create the gate class inheriting from `BinaryLogic` or `UnaryLogic`
3. Add the gate to the `all_gates` list
4. Update `__init__.py` files to export the new gate

### Architecture Components
1. Create the component class in `manimlogic/components/blocks.py`
2. Inherit from `VGroupLogicObjectBase`
3. Implement required methods (`dim_all`, `undim_all`, etc.)
4. Add proper pin connections
5. Update `__init__.py` files

### Example Structure
```python
class MyComponent(VGroupLogicObjectBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Component implementation
        
    def dim_all(self):
        # Dimming logic
        
    def undim_all(self):
        # Undimming logic
```

## Submitting Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Add tests for new functionality
4. Update documentation if needed
5. Commit your changes with descriptive messages
6. Push to your fork
7. Create a Pull Request

## Pull Request Guidelines

- Provide a clear description of the changes
- Include examples of how to use new features
- Ensure all tests pass
- Update documentation if adding new features
- Reference any related issues

## Code Review Process

1. All PRs require at least one review
2. Address review comments promptly
3. Maintainers will merge after approval

## Questions?

Feel free to open an issue for questions or discussions about the project. 