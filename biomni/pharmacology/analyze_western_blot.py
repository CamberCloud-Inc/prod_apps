#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_western_blot
Analyzes western blot images.
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
        description='Analyzes western blot images'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    blot_image_path = input_data.get('blot_image_path')
    target_bands = input_data.get('target_bands')
    loading_control_band = input_data.get('loading_control_band')
    antibody_info = input_data.get('antibody_info')
    output_dir = input_data.get('output_dir', './results')

    if not blot_image_path or not target_bands or not loading_control_band or not antibody_info:
        raise ValueError("Missing required parameters: blot_image_path, target_bands, loading_control_band, antibody_info")

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_western_blot

    result = analyze_western_blot(
        blot_image_path=blot_image_path,
        target_bands=target_bands,
        loading_control_band=loading_control_band,
        antibody_info=antibody_info,
        output_dir=output_dir
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'western_blot_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
