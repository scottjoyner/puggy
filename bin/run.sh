#!/bin/bash

# A simple bash script boilerplate

# Set strict mode: exit on error, undefined variable, or pipe fails
set -euo pipefail

# Constants
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(dirname "$0")

# Functions

## Display usage information
usage() {
    echo "Usage: $SCRIPT_NAME [OPTION]"
    echo "Simple Bash Script Boilerplate"
    echo ""
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"
    # Add other options here
}

## Entry point of the script
main() {
    # Parse command line arguments
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Unknown parameter passed: $1"
                usage
                exit 1
                ;;
        esac
        shift
    done

    # Your script logic here
    echo "Hello, world!"

}

# Start the script
main "$@"
