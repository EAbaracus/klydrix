# Contributing to KLYDRIX

Thank you for considering contributing to KLYDRIX! We welcome contributions from the community.

## Development Environment Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/EAbaracus/klydrix.git
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. Install the package in development mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
6. Verify your setup by running the tests:
   ```bash
   pytest
   ```

## Code Style Guidelines

We use the following tools to maintain code quality:

- **Black**: Code formatter
- **Ruff**: Linter (includes pyflakes and more)
- **Mypy**: Static type checker

These tools are configured in `pyproject.toml`. To check your code:

```bash
# Check formatting with Black
black --check .

# Check code with Ruff
ruff check .

# Check types with Mypy
mypy .

# Or run all checks with pre-commit
pre-commit run --all-files
```

To automatically format your code:

```bash
black .
```

## Testing Requirements

- All new features should include unit tests
- Tests should be placed in the `tests` directory
- We use pytest as our testing framework
- Aim for high test coverage, especially for critical paths
- Run tests before submitting a pull request:
  ```bash
  pytest
  ```
- To run tests with coverage:
  ```bash
  pytest --cov=launch_engine
  ```

## Pull Request Process

1. Ensure your code passes all tests and linting checks
2. Update the documentation if needed (especially for API changes)
3. Make sure your code follows the existing code style
4. Squash commits if necessary (we prefer a clean, linear history)
5. Submit your pull request to the `main` branch
6. A maintainer will review your PR and may request changes
7. Once approved, your PR will be merged

### Pull Request Checklist

- [ ] Code follows the project's code style (Black, Ruff, Mypy)
- [ ] Tests pass locally and in CI
- [ ] New code includes appropriate test coverage
- [ ] Documentation is updated if needed
- [ ] Commit messages follow the conventions below
- [ ] PR title is descriptive and follows conventional commits

## Commit Message Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools
- `revert`: Reverts a previous commit

### Examples

- `feat(engine): add workflow scheduling capability`
- `fix(agent): correct timeout handling in LLM calls`
- `docs: update installation instructions in README`
- `style: format code with black`
- `refactor(core): simplify engine initialization`
- `test(workflow): add tests for conditional task execution`
- `chore: update dependencies`

## Reporting Issues

Please use the GitHub issue tracker to report bugs or request features. When reporting a bug, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Any relevant logs or error messages
- Information about your environment (OS, Python version, etc.)

## Getting Help

If you need help with your contribution, feel free to:

- Ask questions in the issue tracker
- Reach out to maintainers
- Check the existing documentation

Thank you again for contributing to KLYDRIX!