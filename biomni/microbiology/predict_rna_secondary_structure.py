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
    deps = ['biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Predict RNA secondary structure from sequence using thermodynamic models.'
    )
    parser.add_argument('--rna-sequence', type=str, required=True, help='RNA sequence to analyze')
    parser.add_argument('--output-format', type=str, default='dot_bracket', help='Output format (dot_bracket, ct, etc.)')
    parser.add_argument('--temperature', type=float, default=37.0, help='Temperature in Celsius for thermodynamic calculations')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import predict_rna_secondary_structure

    # Call the function
    result = predict_rna_secondary_structure(
        rna_sequence=args.rna_sequence,
        output_format=args.output_format,
        temperature=args.temperature
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'rna_structure_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
