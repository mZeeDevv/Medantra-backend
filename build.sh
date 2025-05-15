#!/bin/bash
set -e

echo "Installing production dependencies..."
pip install -r requirements-prod.txt --no-cache-dir

echo "Optimizing dependencies..."
# Remove tests and other unnecessary files from packages
find . -type d -name "tests" -o -name "test" | xargs rm -rf
find . -type d -name "__pycache__" | xargs rm -rf
find . -type f -name "*.pyc" | xargs rm -f

echo "Build completed successfully!"
