#!/usr/bin/env python3
"""
Camber app wrapper for identify_fas_functional_domains from biomni.tool.synthetic_biology
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
        description='Identify FAS functional domains'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import identify_fas_functional_domains

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    sequence = input_data.get("sequence")
    sequence_type = input_data.get("sequence_type", "protein")
    output_file = input_data.get("output_file", "fas_domains_report.txt")

    # Call the function
    result = identify_fas_functional_domains(
        sequence=sequence,
        sequence_type=sequence_type,
        output_file=output_file
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fas_domains_analysis.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
