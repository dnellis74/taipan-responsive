#!/bin/bash

# Exit on error
set -e

# Install required system packages
sudo yum update -y
sudo yum install -y python3.9 python3.9-devel gcc make

# Create and activate virtual environment
python3.9 -m venv .venv
source .venv/bin/activate

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Build the executable
poetry run pyinstaller \
    --onefile \
    --name taipan \
    --add-data "src/taipan:taipan" \
    --hidden-import=taipan \
    --hidden-import=taipan.ui \
    --hidden-import=taipan.models \
    --hidden-import=taipan.utils \
    --paths=src \
    src/taipan/__main__.py

# Create a distribution package
mkdir -p dist/package
cp dist/taipan dist/package/
cp README.md dist/package/

# Create a tarball
cd dist
tar -czf taipan-amazon-linux-2023.tar.gz package/

echo "Build complete! Executable is in dist/taipan"
echo "Distribution package is in dist/taipan-amazon-linux-2023.tar.gz" 