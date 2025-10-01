#!/usr/bin/env python3
"""
Quantify Amyloid Beta Plaques

Quantifies amyloid-beta plaques in microscopy images using image segmentation and analysis.
"""

import argparse
import sys
import os
import subprocess
import json


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'opencv-python', 'scikit-image', 'scipy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Quantify Amyloid Beta Plaques'
    )
    parser.add_argument('--image-path', required=True, help='Path to microscopy image file of amyloid-beta stained tissue')
    parser.add_argument('--output-dir', default='./results', help='Directory for output files and visualizations (default: ./results)')
    parser.add_argument('--threshold-method', default='otsu', help='Thresholding method for plaque detection (otsu, manual, adaptive) (default: otsu)')
    parser.add_argument('--min-plaque-size', type=int, default=50, help='Minimum plaque area in pixels to exclude noise (default: 50)')
    parser.add_argument('--manual-threshold', type=int, default=127, help='Threshold value if using manual thresholding (default: 127)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import quantify_amyloid_beta_plaques

    result = quantify_amyloid_beta_plaques(
        image_path=args.image_path,
        output_dir=args.output_dir,
        threshold_method=args.threshold_method,
        min_plaque_size=args.min_plaque_size,
        manual_threshold=args.manual_threshold
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'amyloid_beta_plaques_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
