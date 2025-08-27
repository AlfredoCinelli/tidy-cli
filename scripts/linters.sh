#!/bin/bash

path="src/$1"
echo "Run on this path: $path" 
read -p "Do you want to run linters in dynamic mode?: y/n " type_run
if [[ "$type_run" == "n" ]]; then
    ruff check $path
    ruff format $path
    pydoclint $path
    mypy $path --pretty
else
    # Ruff linting section

    read -p "Do you want to run ruff for linting?: y/n " run_lint
    if [[ "$run_lint" == "y" ]]; then
        read -p "Do you want ruff to auto-fix when fixable errors?: y/n " ruff_fix
        if [[ "$ruff_fix" == "y" ]]; then
            ruff check $path --fix
        else
            ruff check $path
        fi
    fi

    # Ruff format section

    read -p "Do you want to run ruff for formatting?: y/n " run_format
    if [[ "$run_format" == "y" ]]; then 
        ruff format $path
    fi

    # Pydoclint section

    read -p "Do you want to run pydoclint?: y/n " run_pydoclint
    if [[ "$run_pydoclint" == "y" ]]; then
        pydoclint $path
    fi

    # Mypy section

    read -p "Do you want to run mypy?: y/n " run_mypy
    if [[ "$run_mypy" == "y" ]]; then 
        mypy $path --pretty || true
    fi
fi