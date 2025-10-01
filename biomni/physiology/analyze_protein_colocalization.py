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
    deps = ['biomni', 'opencv-python', 'scikit-image', 'scipy', 'skimage']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Protein Colocalization'
    )
    parser.add_argument('--channel1-path', required=True, help='Path to channel 1 image file (first fluorescent protein)')
    parser.add_argument('--channel2-path', required=True, help='Path to channel 2 image file (second fluorescent protein)')
    parser.add_argument('--output-dir', default='./output', help='Directory for output files (default: ./output)')
    parser.add_argument('--threshold-method', default='otsu', help='Thresholding method (otsu, manual, adaptive) (default: otsu)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_protein_colocalization

    result = analyze_protein_colocalization(
        channel1_path=args.channel1_path,
        channel2_path=args.channel2_path,
        output_dir=args.output_dir,
        threshold_method=args.threshold_method
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'protein_colocalization_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
