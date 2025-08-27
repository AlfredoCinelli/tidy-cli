#!/bin/bash

# Check if dist folder exists and remove it
if [ -d "dist" ]; then
    echo "🗑️ Removing existing dist files and other artifacts..."
    rm -rf dist/
    rm -rf *.egg-info/
    echo "✅ Existing dist and artifacts files removed"
else
    echo "🔕 No existing dist folder found"
fi

uv build . # create distribution files

twine check dist/* # check if the distribution files are valid (for publishing)