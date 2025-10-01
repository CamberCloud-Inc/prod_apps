#!/usr/bin/env python3
"""
Camber app wrapper for analyze_barcode_sequencing_data from biomni.tool.synthetic_biology
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
        description='Analyze barcode sequencing data'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import analyze_barcode_sequencing_data

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    input_file = input_data.get("input_file")
    barcode_pattern = input_data.get("barcode_pattern")
    flanking_seq_5prime = input_data.get("flanking_seq_5prime")
    flanking_seq_3prime = input_data.get("flanking_seq_3prime")
    min_count = input_data.get("min_count", 5)
    output_dir = input_data.get("output_dir", "./results")

    # Call the function
    result = analyze_barcode_sequencing_data(
        input_file=input_file,
        barcode_pattern=barcode_pattern,
        flanking_seq_5prime=flanking_seq_5prime,
        flanking_seq_3prime=flanking_seq_3prime,
        min_count=min_count,
        output_dir=output_dir
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'barcode_analysis.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
