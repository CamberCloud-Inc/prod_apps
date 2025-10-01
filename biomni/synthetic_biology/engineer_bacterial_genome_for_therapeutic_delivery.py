#!/usr/bin/env python3
"""
Camber app wrapper for engineer_bacterial_genome_for_therapeutic_delivery from biomni.tool.synthetic_biology
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Engineer bacterial genome for therapeutic delivery'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import engineer_bacterial_genome_for_therapeutic_delivery

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    bacterial_genome_file = input_data.get("bacterial_genome_file")
    genetic_parts = input_data.get("genetic_parts")

    # Call the function
    result = engineer_bacterial_genome_for_therapeutic_delivery(
        bacterial_genome_file=bacterial_genome_file,
        genetic_parts=genetic_parts
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'genome_engineering_result.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
