#!/bin/sh

# Check if at least one argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [args...]"
    exit 1
fi

# Run the command with all arguments
"$@"