# Contributing to Interactive Data Dashboard

Thank you for your interest in contributing to the Interactive Data Dashboard! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Community](#community)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a welcoming and inclusive community.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Streamlit, Pandas, and Plotly

### First-time Contributors

If you're new to open source contribution:

1. Look for issues labeled `good first issue` or `help wanted`
2. Read through the codebase to understand the project structure
3. Start with small changes like documentation improvements or bug fixes
4. Ask questions in GitHub Discussions if you need help

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/interactive-data-dashboard.git
cd interactive-data-dashboard

# Add the original repository as upstream
git remote add upstream https://github.com/ORIGINAL_OWNER/interactive-data-dashboard.git
```

### 2. Set Up Development Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your local settings
# Set DEBUG=true for development
```

### 4. Verify Setup

```bash
# Run tests to ensure everything works
pytest

# Start the development server
streamlit run app.py
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix existing issues
- **Feature additions**: Add new functionality
- **Documentation**: Improve or add documentation
- **Performance improvements**: Optimize existing code
- **Tests**: Add or improve test coverage
- **UI/UX improvements**: Enhance user experience
- **Code refactoring**: Improve code quality

### Before You Start

1. **Check existing issues**: Look for existing issues or discussions
2. **Create an issue**: For new features or significant changes
3. **Discuss first**: For major changes, discuss in GitHub Discussions
4. **Keep it focused**: One feature or fix per pull request

### Branch Naming Convention

Use descriptive branch names:

```bash
# Feature branches
feature/add-export-functionality
feature/improve-chart-performance

# Bug fix branches
fix/memory-leak-large-datasets
fix/chart-rendering-mobile

# Documentation branches
docs/update-installation-guide
docs/add-api-examples

# Refactoring branches
refactor/data-processor-class
refactor/chart-generator-methods
```

## Pull Request Process

### 1. Create Your Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the coding standards
- Add tests for new functionality
- Update documentation as needed
- Commit frequently with clear messages

### 3. Test Your Changes

```bash
# Run the full test suite
pytest

# Run specific test categories
pytest -m unit
pytest -m integration

# Check code coverage
pytest --cov=src --cov-report=html

# Run linting and formatting
black src/ tests/
ruff check src/ tests/
mypy src/
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add export functionality for charts

- Add export buttons for PNG, SVG, and HTML formats
- Implement download functionality in chart generator
- Add tests for export features
- Update documentation with export examples"
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
# Use the pull request template
# Provide clear description of changes
```

### Pull Request Template

When creating a pull request, include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings or errors
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Use isort for import organization
- **Type hints**: Required for all public functions
- **Docstrings**: Google style for all public methods

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/

# Security check
bandit -r src/
```

### Documentation Standards

```python
def process_data(df: pd.DataFrame, clean: bool = True) -> pd.DataFrame:
    """Process and clean the input DataFrame.
    
    Args:
        df: Input DataFrame to process
        clean: Whether to perform data cleaning
        
    Returns:
        Processed DataFrame with cleaned data
        
    Raises:
        ValueError: If DataFrame is empty
        TypeError: If input is not a DataFrame
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, None], 'B': [4, 5, 6]})
        >>> cleaned_df = process_data(df, clean=True)
        >>> len(cleaned_df)
        2
    """
```

## Testing

### Test Structure

```
tests/
├── unit/
│   ├── test_data_processor.py
│   ├── test_chart_generator.py
│   └── test_utils.py
├── integration/
│   ├── test_app_flow.py
│   └── test_data_pipeline.py
├── performance/
│   └── test_large_datasets.py
└── fixtures/
    ├── sample_data.csv
    └── test_config.py
```

### Writing Tests

```python
import pytest
import pandas as pd
from interactive_data_dashboard.data_processor import DataProcessor

class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            'A': [1, 2, 3, None, 5],
            'B': ['x', 'y', 'z', 'w', 'v'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
    
    def test_data_cleaning(self, sample_data):
        """Test data cleaning functionality."""
        processor = DataProcessor()
        cleaned = processor.clean_data(sample_data)
        
        assert len(cleaned) == 4  # One row with None removed
        assert cleaned['A'].isna().sum() == 0
    
    @pytest.mark.parametrize("file_type,expected", [
        ("csv", "text/csv"),
        ("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        ("json", "application/json")
    ])
    def test_file_type_detection(self, file_type, expected):
        """Test file type detection for various formats."""
        # Test implementation
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_data_processor.py

# Run tests with specific marker
pytest -m "unit and not slow"

# Run tests in parallel
pytest -n auto
```

## Documentation

### Types of Documentation

1. **Code documentation**: Docstrings and comments
2. **User documentation**: README, usage guides
3. **API documentation**: Auto-generated from docstrings
4. **Developer documentation**: Contributing guides, architecture

### Documentation Guidelines

- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting
- Include screenshots for UI features

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Clear title**: Descriptive summary of the issue
2. **Environment**: OS, Python version, package versions
3. **Steps to reproduce**: Detailed steps to recreate the bug
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Screenshots**: If applicable
7. **Error messages**: Full error traceback
8. **Sample data**: Minimal example that reproduces the issue

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**Environment**
- OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.0.0]
- Browser: [e.g., Chrome 96.0]

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Actual Behavior**
A clear description of what actually happened.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Error Messages**
```
Paste any error messages or tracebacks here
```

**Additional Context**
Add any other context about the problem here.
```

## Feature Requests

### Before Requesting

1. Check existing issues and discussions
2. Consider if it fits the project scope
3. Think about implementation complexity
4. Consider backward compatibility

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
Describe your preferred solution.

**Alternative Solutions**
Describe any alternative solutions you've considered.

**Use Cases**
Provide specific examples of how this feature would be used.

**Implementation Ideas**
If you have ideas about implementation, share them.

**Additional Context**
Add any other context, mockups, or examples.
```

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code review and collaboration

### Getting Help

1. **Search existing issues**: Your question might already be answered
2. **Check documentation**: README and docs might have the answer
3. **Ask in discussions**: For general questions
4. **Create an issue**: For specific bugs or feature requests

### Recognition

We recognize contributors in several ways:

- Contributors list in README
- Release notes acknowledgments
- GitHub contributor statistics
- Special recognition for significant contributions

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Update documentation
5. Create release notes
6. Tag release
7. Deploy to package repositories

---

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort in helping improve the Interactive Data Dashboard!

For questions about contributing, feel free to reach out through GitHub Discussions or create an issue.

Happy coding! 🚀