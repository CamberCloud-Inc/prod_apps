#!/bin/bash
[ $# -ne 1 ] && { echo "Usage: $0 <left_force_duration>"; exit 1; }

LEFT_FORCE_DURATION=$1
mkdir -p output
rm -f output/*.{lammpstrj,csv,log}

# Store LEFT_FORCE_DURATION parameter in output file for visualization
echo "LEFT_FORCE_DURATION=$LEFT_FORCE_DURATION" > output/parameters.txt

cd scripts && lmp -in unbreakable.lmp -var LEFT_FORCE_DURATION $LEFT_FORCE_DURATION && cd .. || exit 1