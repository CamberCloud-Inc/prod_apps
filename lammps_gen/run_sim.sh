#!/bin/bash
# Check if temperature argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <temperature>"
    echo "Example: $0 100"
    exit 1
fi

# Get temperature from command line argument
TEMP=$1

sed -i "s/\$(temperature)/$TEMP/g" unbreakable.lmp && \
lmp -in unbreakable.lmp
