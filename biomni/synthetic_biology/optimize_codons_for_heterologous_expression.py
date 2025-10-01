#!/usr/bin/env python3
"""
Camber app wrapper for optimize_codons_for_heterologous_expression from biomni.tool.synthetic_biology
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
        description='Optimize codons for heterologous expression'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.synthetic_biology import optimize_codons_for_heterologous_expression

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    target_sequence = input_data.get("target_sequence")
    host_codon_usage = input_data.get("host_codon_usage")

    # Call the function
    result = optimize_codons_for_heterologous_expression(
        target_sequence=target_sequence,
        host_codon_usage=host_codon_usage
    )

    # Write result to file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'codon_optimization_result.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
