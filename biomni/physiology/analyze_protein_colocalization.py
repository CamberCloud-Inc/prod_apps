#!/usr/bin/env python3
"""
Analyze Protein Colocalization

Analyze colocalization between two fluorescently labeled proteins in microscopy images.
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
        description='Analyze Protein Colocalization'
    )
    parser.add_argument('input_file', help='Input JSON file with channel1_path, channel2_path and optional parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_protein_colocalization

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    channel1_path = inputs['channel1_path']
    channel2_path = inputs['channel2_path']
    output_dir = inputs.get('output_dir', './output')
    threshold_method = inputs.get('threshold_method', 'otsu')

    result = analyze_protein_colocalization(
        channel1_path=channel1_path,
        channel2_path=channel2_path,
        output_dir=output_dir,
        threshold_method=threshold_method
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'protein_colocalization_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
