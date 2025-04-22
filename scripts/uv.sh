#!/bin/bash

# Function to display help
show_help() {
    echo "Usage: ./uv.sh [command]"
    echo ""
    echo "Commands:"
    echo "  install     Install dependencies"
    echo "  dev         Install development dependencies"
    echo "  update      Update dependencies"
    echo "  clean       Clean the virtual environment"
    echo "  help        Show this help message"
}

# Function to install dependencies
install() {
    echo "Installing dependencies..."
    uv pip install -e .
}

# Function to install development dependencies
dev() {
    echo "Installing development dependencies..."
    uv pip install -e ".[dev]"
}

# Function to update dependencies
update() {
    echo "Updating dependencies..."
    uv pip install --upgrade -e .
    uv pip install --upgrade -e ".[dev]"
}

# Function to clean the virtual environment
clean() {
    echo "Cleaning virtual environment..."
    uv pip freeze | xargs uv pip uninstall -y
}

# Main script
case "$1" in
    install)
        install
        ;;
    dev)
        dev
        ;;
    update)
        update
        ;;
    clean)
        clean
        ;;
    help|*)
        show_help
        ;;
esac 