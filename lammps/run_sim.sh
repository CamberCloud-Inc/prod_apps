#!/bin/bash
# filepath: run_lammps.sh

# Check if temperature argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <temperature>"
    echo "Example: $0 100"
    exit 1
fi

# Get temperature from command line argument
TEMP=$1

# Validate that temperature is a number
if ! [[ "$TEMP" =~ ^[0-9]+$ ]]; then
    echo "Error: Temperature must be a positive integer"
    exit 1
fi

# Clone repository, navigate to directory, substitute temperature, and run LAMMPS
# git clone https://github.com/CamberCloud-Inc/prod_apps.git && \
# cd prod_apps/lammps/ && \
sed -i "s/\$(temperature)/$TEMP/g" unbreakable.lmp && \
lmp -in unbreakable.lmp
