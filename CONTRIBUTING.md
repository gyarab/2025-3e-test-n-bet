# Contributing to Test N Bet

Thank you for considering contributing to Test N Bet! This document provides guidelines and instructions for contributing to the project.

## 🎯 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/YOUR_USERNAME/2025-3e-test-n-bet.git
   cd 2025-3e-test-n-bet
   ```
3. **Set up the development environment** following the README.md instructions
4. **Create a branch** for your changes
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Development Workflow

### Before Making Changes

1. Make sure you're working on the latest code:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Create a new branch from main:
   ```bash
   git checkout -b feature/descriptive-name
   ```

### Making Changes

1. **Write clean, readable code**
   - Follow PEP 8 style guidelines for Python
   - Use meaningful variable and function names
   - Keep functions small and focused
   - Add comments for complex logic

2. **Write tests**
   - Add unit tests for new features
   - Ensure existing tests still pass
   - Aim for good test coverage

3. **Update documentation**
   - Update README.md if adding new features
   - Add docstrings to functions and classes
   - Update API documentation if needed

### Testing Your Changes

1. **Run all tests**
   ```bash
   python manage.py test
   ```

2. **Run specific app tests**
   ```bash
   python manage.py test apps.backtests
   python manage.py test apps.strategies
   ```

3. **Run with pytest**
   ```bash
   pytest
   pytest -m "not slow"  # Skip slow tests
   ```

4. **Check for Django issues**
   ```bash
   python manage.py check
   ```

### Committing Changes

1. **Stage your changes**
   ```bash
   git add .
   ```

2. **Commit with a clear message**
   ```bash
   git commit -m "Add feature: brief description"
   ```

   Good commit message examples:
   - `Add backtesting engine for moving average strategies`
   - `Fix bug in trade risk calculation`
   - `Update documentation for API endpoints`
   - `Refactor strategy service for better performance`

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

## 🔍 Pull Request Process

1. **Create a Pull Request** on GitHub from your fork to the main repository

2. **Fill out the PR template** with:
   - Clear description of changes
   - Related issue numbers (if applicable)
   - Testing performed
   - Screenshots (if UI changes)

3. **Ensure CI passes**
   - All tests must pass
   - No linting errors
   - Code builds successfully

4. **Address review feedback**
   - Respond to comments
   - Make requested changes
   - Push updates to the same branch

5. **Wait for approval**
   - At least one maintainer approval required
   - All conversations must be resolved

## 🎨 Coding Standards

### Python Style

- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where appropriate

### Django Best Practices

- Use Django's built-in features when possible
- Follow the Model-View-Template pattern
- Keep business logic in services, not views
- Use Django ORM instead of raw SQL
- Protect against SQL injection and XSS

### Security Guidelines

- Never commit sensitive data (API keys, passwords, etc.)
- Always use environment variables for secrets
- Validate and sanitize user input
- Use Django's built-in security features
- Keep dependencies up to date

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new features
- Test edge cases and error conditions
- Use descriptive test names
- Keep tests isolated and independent

### Test Structure

```python
def test_feature_expected_behavior():
    """Test that feature does X when given Y."""
    # Arrange
    setup_data()
    
    # Act
    result = perform_action()
    
    # Assert
    assert result == expected_value
```

### Test Markers

Use pytest markers for test categorization:
```python
@pytest.mark.slow
def test_long_running_operation():
    pass

@pytest.mark.optional
def test_optional_feature():
    pass
```

## 📚 Documentation Guidelines

### Code Documentation

- Add docstrings to all public functions and classes
- Use clear, concise language
- Include parameter descriptions and return types
- Provide usage examples when helpful

Example:
```python
def calculate_moving_average(prices: list[float], period: int) -> float:
    """
    Calculate the simple moving average for a given period.
    
    Args:
        prices: List of price values
        period: Number of periods to average
        
    Returns:
        The calculated moving average
        
    Raises:
        ValueError: If period is greater than prices length
    """
    if period > len(prices):
        raise ValueError("Period cannot exceed prices length")
    return sum(prices[-period:]) / period
```

### README Updates

Update README.md when:
- Adding new features
- Changing setup requirements
- Modifying configuration options
- Adding new dependencies

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the bug has already been reported
2. Verify it's not a configuration issue
3. Try to reproduce with minimal steps

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.12]
- Django version: [e.g., 5.0]
- Browser (if applicable): [e.g., Chrome 120]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

We welcome feature suggestions! Please:

1. Check if the feature has already been requested
2. Provide a clear use case
3. Explain the expected benefit
4. Consider implementation complexity

## 🔄 Review Process

### What We Look For

- Code quality and readability
- Test coverage
- Documentation completeness
- Adherence to project standards
- Security considerations

### Review Timeline

- Initial review: 1-3 business days
- Follow-up reviews: 1-2 business days
- Merge after approval and passing CI

## 📋 Checklist Before Submitting PR

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No sensitive data committed
- [ ] Commit messages are clear
- [ ] Branch is up to date with main
- [ ] PR description is complete

## 🙏 Recognition

Contributors will be:
- Added to the contributors list
- Credited in release notes
- Appreciated in the community

## 📞 Getting Help

If you need help:
- Open a GitHub issue with the "question" label
- Check existing documentation
- Review closed issues for similar problems

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Test N Bet! 🎉
