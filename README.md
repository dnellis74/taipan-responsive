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

## Building for Amazon Linux 2023

### Prerequisites
- Amazon Linux 2023 instance
- sudo access
- Internet connection

### Building the Executable

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd taipan-responsive
   ```

2. Run the build script:
   ```bash
   ./build_amazon_linux.sh
   ```

3. The build process will:
   - Install required system packages
   - Set up a Python virtual environment
   - Install Poetry and project dependencies
   - Build a standalone executable
   - Create a distribution package

4. After successful build, you'll find:
   - Executable: `dist/taipan`
   - Distribution package: `dist/taipan-amazon-linux-2023.tar.gz`

### Installing the Executable

1. Extract the distribution package:
   ```bash
   tar -xzf taipan-amazon-linux-2023.tar.gz
   cd package
   ```

2. Make the executable:
   ```bash
   chmod +x taipan
   ```

3. Run the game:
   ```bash
   ./taipan
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
├── build_amazon_linux.sh  # Build script
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
- **PyInstaller**: Executable builder

## Running the Game

Development:
```bash
poetry run python -m taipan
```

Production (after building):
```bash
./taipan
```

## Development Commands

- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Lint code: `poetry run ruff check .`
- Type check: `poetry run mypy .`
- Build executable: `./build_amazon_linux.sh`

## License

MIT License 