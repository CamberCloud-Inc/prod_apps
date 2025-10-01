#!/usr/bin/env python3
"""Biomni Tool: Analyze Cell Morphology and Cytoskeleton
Wraps: biomni.tool.biophysics.analyze_cell_morphology_and_cytoskeleton
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
        description='Quantifies cell morphology and cytoskeletal organization from fluorescence microscopy images'
    )
    parser.add_argument('input_file', help='JSON file with input parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input parameters
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_path = input_data['image_path']
    threshold_method = input_data.get('threshold_method', 'otsu')

    from biomni.tool.biophysics import analyze_cell_morphology_and_cytoskeleton

    result = analyze_cell_morphology_and_cytoskeleton(
        image_path=image_path,
        output_dir=args.output,
        threshold_method=threshold_method
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cell_morphology_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
