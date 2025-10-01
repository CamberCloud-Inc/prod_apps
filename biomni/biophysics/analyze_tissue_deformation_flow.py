#!/usr/bin/env python3
"""Biomni Tool: Analyze Tissue Deformation Flow
Wraps: biomni.tool.biophysics.analyze_tissue_deformation_flow
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
        description='Quantify tissue deformation and flow dynamics from microscopy image sequence'
    )
    parser.add_argument('input_file', help='JSON file with input parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_sequence = input_data['image_sequence']
    pixel_scale = input_data.get('pixel_scale', 1.0)

    # Convert image_sequence to list if it's a path or list of paths
    if isinstance(image_sequence, str):
        # Single path - treat as directory or file pattern
        import glob
        image_sequence = sorted(glob.glob(image_sequence))

    from biomni.tool.biophysics import analyze_tissue_deformation_flow

    result = analyze_tissue_deformation_flow(
        image_sequence=image_sequence,
        output_dir=args.output,
        pixel_scale=pixel_scale
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'tissue_deformation_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
