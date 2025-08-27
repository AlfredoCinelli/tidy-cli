#!/bin/bash

# Check if dist folder exists and remove it
if [ -d "dist" ]; then
    echo "⚠ Removing existing dist folder..."
    rm -rf dist/
    echo "✓ Existing dist folder removed"
else
    echo "No existing dist folder found"
fi

uv build . # create distribution files

twine check dist/* # check if the distribution files are valid (for publishing)

read -p "Do you want to publish the package?: y/n " publish

if [[ "$publish" == "y" ]]; then 
    twine upload dist/*
fi