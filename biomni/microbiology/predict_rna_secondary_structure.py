#!/usr/bin/env python3
"""
Predict RNA secondary structure from sequence using thermodynamic models.
"""

import sys
import json
import argparse
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Predict RNA secondary structure from sequence using thermodynamic models.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import predict_rna_secondary_structure

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    rna_sequence = input_data.get('rna_sequence')
    output_format = input_data.get('output_format', 'dot_bracket')
    temperature = input_data.get('temperature', 37.0)

    # Call the function
    result = predict_rna_secondary_structure(
        rna_sequence=rna_sequence,
        output_format=output_format,
        temperature=temperature
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'rna_structure_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
