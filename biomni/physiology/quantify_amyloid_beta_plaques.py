#!/usr/bin/env python3
"""
Quantify Amyloid Beta Plaques

Quantifies amyloid-beta plaques in microscopy images using image segmentation and analysis.
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
        description='Quantify Amyloid Beta Plaques'
    )
    parser.add_argument('input_file', help='Input JSON file with image_path and optional parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import quantify_amyloid_beta_plaques

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    image_path = inputs['image_path']
    output_dir = inputs.get('output_dir', './results')
    threshold_method = inputs.get('threshold_method', 'otsu')
    min_plaque_size = inputs.get('min_plaque_size', 50)
    manual_threshold = inputs.get('manual_threshold', 127)

    result = quantify_amyloid_beta_plaques(
        image_path=image_path,
        output_dir=output_dir,
        threshold_method=threshold_method,
        min_plaque_size=min_plaque_size,
        manual_threshold=manual_threshold
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'amyloid_beta_plaques_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
