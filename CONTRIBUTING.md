# Contributing to JACoW Invincible Paper Crawler

Thank you for your interest in contributing to the JACoW Invincible Paper Crawler! This document provides guidelines and information for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Reporting Issues](#reporting-issues)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming and inclusive environment. By participating, you are expected to uphold this code.

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of web scraping and async programming

### Initial Setup
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/jacow-invincible-crawler.git
   cd jacow-invincible-crawler
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/jacow-invincible-crawler.git
   ```

## Development Setup

### Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. Install development tools:
   ```bash
   pip install black flake8 pytest pytest-cov bandit
   ```

4. Verify installation:
   ```bash
   python tests/verify.py
   ```

### Project Structure
```
jacow-invincible-crawler/
├── crawler/           # Core crawling modules
├── utils/            # Utility functions
├── tests/            # Test suite
├── docs/             # Documentation
├── examples/         # Usage examples
├── scripts/          # Standalone tools
└── .github/          # GitHub workflows and templates
```

## Contributing Guidelines

### Types of Contributions
We welcome several types of contributions:
- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Submit bug fixes or new features
- **Documentation**: Improve or add documentation
- **Testing**: Add test cases or improve test coverage

### Priority Areas
Current areas where contributions are especially welcome:
1. Support for additional JACoW conferences
2. Enhanced error handling and recovery
3. Performance optimizations
4. Cross-platform compatibility improvements
5. Documentation and examples

## Reporting Issues

### Before Reporting
1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Run the verification script: `python tests/verify.py`

### Issue Template
Please use the provided issue templates and include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Relevant error messages or logs

## Submitting Pull Requests

### Before You Start
1. Create an issue to discuss major changes
2. Check if someone else is already working on it
3. Fork the repository and create a feature branch

### PR Process
1. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:
   - Write clear, focused commits
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**:
   ```bash
   python tests/verify.py
   pytest tests/
   python main.py --dry-run --year 2023
   ```

4. **Lint Your Code**:
   ```bash
   black .
   flake8 .
   ```

5. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Use the provided PR template
   - Link related issues
   - Provide clear description of changes
   - Add screenshots/examples if applicable

### PR Requirements
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated if needed
- [ ] No new security vulnerabilities
- [ ] Backward compatibility maintained (unless breaking change)

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Organization
- Keep functions focused and small
- Use descriptive variable and function names
- Add docstrings to all public functions
- Include error handling and logging

### Example Code Style
```python
async def download_paper(
    session: aiohttp.ClientSession,
    paper_info: Dict[str, Any],
    output_dir: Path,
    logger: logging.Logger
) -> Dict[str, Any]:
    """
    Download a single paper from JACoW.
    
    Args:
        session: HTTP session for downloading
        paper_info: Dictionary containing paper metadata
        output_dir: Directory to save the paper
        logger: Logger instance for progress tracking
        
    Returns:
        Dictionary with download results and metadata
        
    Raises:
        aiohttp.ClientError: If download fails
        IOError: If file cannot be saved
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Failed to download {paper_info['title']}: {e}")
        raise
```

## Testing

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=crawler --cov=utils

# Run specific test file
pytest tests/test_individual.py

# Run verification script
python tests/verify.py
```

### Writing Tests
- Add tests for new functionality
- Include both positive and negative test cases
- Test error conditions and edge cases
- Use meaningful test names and docstrings

### Test Categories
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test efficiency and scalability

## Documentation

### Types of Documentation
- **Code Comments**: Explain complex logic
- **Docstrings**: Document functions and classes
- **README**: Project overview and quick start
- **Guides**: Detailed usage instructions
- **API Documentation**: Generated from docstrings

### Documentation Standards
- Use clear, concise language
- Include examples where helpful
- Keep documentation up-to-date with code changes
- Use proper Markdown formatting

## Release Process

### Version Numbering
We follow Semantic Versioning (SemVer):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps
1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release: `git tag v1.0.0`
5. Push tags: `git push --tags`

## Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Email**: mliu@ihep.ac.cn for project-related inquiries

### Resources
- [Project Documentation](https://github.com/OWNER/REPO/docs)
- [JACoW Website](https://www.jacow.org/)
- [Python aiohttp Documentation](https://docs.aiohttp.org/)

## Recognition

Contributors will be acknowledged in:
- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- GitHub contributors graph

Thank you for contributing to the JACoW Invincible Paper Crawler! 🚀

---
**Author**: Ming Liu (mliu@ihep.ac.cn)  
**Last Updated**: September 9, 2025
