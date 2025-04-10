# Taipan! Responsive

A modern, mobile-friendly terminal version of the classic game Taipan!

## Development Setup

1. Install Python 3.10 or later (recommended: use [pyenv](https://github.com/pyenv/pyenv))
   ```bash
   # Install pyenv
   curl https://pyenv.run | bash
   
   # Install Python 3.10
   pyenv install 3.10.0
   pyenv global 3.10.0
   ```

2. Install [Poetry](https://python-poetry.org/docs/#installation)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Clone the repository and set up the environment:
   ```bash
   git clone <repository-url>
   cd taipan-responsive
   
   # Install dependencies
   poetry install
   
   # Activate the virtual environment
   poetry shell
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Project Structure

```
taipan/
├── src/
│   ├── taipan/
│   │   ├── __init__.py
│   │   ├── app.py          # Main Textual app
│   │   ├── models/         # Game state and logic
│   │   ├── ui/            # UI components
│   │   └── utils/         # Helper functions
│   └── tests/             # Test suite
├── pyproject.toml         # Project configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── README.md             # This file
```

## Development Tools

- **Textual**: Modern TUI framework
- **Poetry**: Dependency management
- **Ruff**: Fast Python linter
- **Black**: Code formatter
- **Pytest**: Testing framework
- **Pre-commit**: Git hooks for code quality
- **Mypy**: Static type checking

## Running the Game

```bash
poetry run python -m taipan
```

## Development Commands

- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Lint code: `poetry run ruff check .`
- Type check: `poetry run mypy .`

## License

MIT License 