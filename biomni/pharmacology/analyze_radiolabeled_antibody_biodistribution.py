#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_radiolabeled_antibody_biodistribution
Analyzes radiolabeled antibody biodistribution.
"""

import argparse
import sys
import subprocess
import os
import json


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyzes radiolabeled antibody biodistribution'
    )
    parser.add_argument('--time-points', required=True, help='List of time points for biodistribution measurements (JSON array, e.g., [1, 4, 24, 48, 72])')
    parser.add_argument('--tissue-data', required=True, help='Dictionary of tissue types with radioactivity measurements (JSON object)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse JSON parameters
    time_points = json.loads(args.time_points)
    tissue_data = json.loads(args.tissue_data)

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_radiolabeled_antibody_biodistribution

    result = analyze_radiolabeled_antibody_biodistribution(
        time_points=time_points,
        tissue_data=tissue_data
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'biodistribution_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
