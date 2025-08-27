#!/bin/bash

path="$1"

# Run pytests
if [ "$path" != "" ]; then
    read -p "🎛️ Do you want to show logs? [y/n]: " logs
    if [[ "$logs" == "y" ]]; then
        echo "🔊 Showing logs..."
        uv run python -m pytest "$path" -s --disable-pytest-warnings
    else
        echo "🔇 Not showing logs..."
        uv run python -m pytest "$path" --disable-pytest-warnings
    fi
else
    uv run coverage run --rcfile=./pyproject.toml -m pytest --disable-pytest-warnings && uv run coverage report
    # delete coverage file
    rm -f .coverage
fi

# delete all cache of tests
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf