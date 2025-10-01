#!/usr/bin/env python3
"""Biomni Tool: Predict Protein Disorder Regions
Wraps: biomni.tool.biophysics.predict_protein_disorder_regions
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Predicts intrinsically disordered regions (IDRs) in a protein sequence using IUPred2A'
    )
    parser.add_argument('protein_sequence', help='Amino acid sequence in single-letter code')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-t', '--threshold', type=float, default=0.5,
                        help='Disorder probability threshold (0.0 to 1.0, default: 0.5)')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.biophysics import predict_protein_disorder_regions

    # Create output directory and set output_file path
    os.makedirs(args.output, exist_ok=True)
    output_csv_file = os.path.join(args.output, 'disorder_prediction_results.csv')

    result = predict_protein_disorder_regions(
        protein_sequence=args.protein_sequence,
        threshold=args.threshold,
        output_file=output_csv_file
    )

    output_file = os.path.join(args.output, 'disorder_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
