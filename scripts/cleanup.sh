#!/bin/bash
# Cleanup script for generated files and temporary data

set -e

echo "🧹 Cypher Cleanup Script"
echo "========================"

# Remove generated files
echo "Removing generated files..."
rm -rf generated/*.html
rm -rf generated/*.json
rm -rf generated/*.csv
rm -rf generated/*.xlsx

# Remove Python cache
echo "Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Remove temporary files
echo "Removing temporary files..."
rm -f *.log
rm -f *.tmp
rm -f probe_*.txt

echo "✅ Cleanup complete!"
