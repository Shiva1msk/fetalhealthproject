# Contributing to Fetal Health Prediction System

Thank you for your interest in contributing to the Fetal Health Prediction System! This document provides guidelines for contributing to this project.

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Error messages and logs

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Describe the feature** in detail
3. **Explain the use case** and benefits
4. **Consider implementation complexity**

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow coding standards** (see below)
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass**
6. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites
- Python 3.10+
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/fetal-health-prediction.git
cd fetal-health-prediction

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Run tests
python -m pytest tests/

# Run the application
python run.py --setup
python run.py --both
```

## Coding Standards

### Python Style
- Follow **PEP 8** style guidelines
- Use **Black** for code formatting: `black .`
- Use **flake8** for linting: `flake8 .`
- Use **type hints** where appropriate
- Maximum line length: 88 characters

### Code Quality
- Write **clear, descriptive variable names**
- Add **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful commit messages**

### Testing
- Write **unit tests** for new functionality
- Maintain **test coverage** above 80%
- Use **pytest** for testing framework
- Test both **success and error cases**

### Documentation
- Update **README.md** for user-facing changes
- Update **API.md** for API changes
- Add **inline comments** for complex logic
- Update **CHANGELOG.md** for releases

## Project Structure

```
fetal-health-system/
├── app.py                 # Main Flask application
├── agent.py              # AI agent core logic
├── agent_app.py          # AI agent web interface
├── run.py                # Application runner
├── requirements.txt      # Python dependencies
├── models/               # ML model files
├── data/                 # Dataset files
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── tests/               # Test files
├── docs/                # Documentation
└── deployment/          # Deployment configs
```

## Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/config changes

Examples:
```
feat(agent): add natural language query processing
fix(api): handle missing model file gracefully
docs(readme): update installation instructions
```

## Testing Guidelines

### Unit Tests
```python
def test_prediction_valid_data():
    """Test prediction with valid input data."""
    agent = FetalHealthAgent()
    sample_data = agent.get_sample_data()
    result = agent.make_prediction(sample_data)
    
    assert result['success'] == True
    assert result['prediction'] in ['NORMAL', 'SUSPECT', 'PATHOLOGICAL']
```

### Integration Tests
```python
def test_api_prediction_endpoint(client):
    """Test API prediction endpoint."""
    response = client.post('/api/predict', json=sample_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
```

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_agent.py

# Run with verbose output
python -m pytest -v
```

## Documentation Guidelines

### Code Documentation
```python
def make_prediction(self, data: Dict[str, float]) -> Dict[str, Any]:
    """
    Make a fetal health prediction using the loaded model.
    
    Args:
        data: Dictionary containing medical parameters
        
    Returns:
        Dictionary containing prediction result and confidence scores
        
    Raises:
        ValueError: If input data is invalid
    """
```

### API Documentation
- Use clear endpoint descriptions
- Provide request/response examples
- Document error codes and messages
- Include authentication requirements

## Security Guidelines

### Input Validation
- **Validate all user inputs**
- **Sanitize data** before processing
- **Use parameterized queries** if using databases
- **Implement rate limiting** for APIs

### Error Handling
- **Don't expose sensitive information** in error messages
- **Log security events** appropriately
- **Use secure defaults**
- **Validate file uploads** if implemented

## Performance Guidelines

### Code Performance
- **Profile code** for bottlenecks
- **Use appropriate data structures**
- **Cache expensive operations**
- **Optimize database queries** if applicable

### Model Performance
- **Monitor prediction latency**
- **Track model accuracy** over time
- **Implement model versioning**
- **Consider model optimization**

## Release Process

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps
1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Create release branch
5. Submit pull request
6. Tag release after merge
7. Deploy to production

## Medical Considerations

### Compliance
- **Follow medical data regulations** (HIPAA, GDPR, etc.)
- **Implement audit logging** for medical predictions
- **Ensure data privacy** and security
- **Document medical disclaimers**

### Validation
- **Validate against medical standards**
- **Test with medical professionals**
- **Document clinical validation**
- **Implement safety checks**

## Getting Help

### Resources
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check docs/ directory
- **Code Examples**: See tests/ directory

### Contact
- Create an issue for technical questions
- Use discussions for general questions
- Follow project updates for announcements

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- GitHub contributors page

Thank you for contributing to the Fetal Health Prediction System! Your contributions help improve healthcare technology and potentially save lives.