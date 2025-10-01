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
    deps = ['biomni', 'cv2', 'opencv-python', 'scipy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Quantifies cell morphology and cytoskeletal organization from fluorescence microscopy images'
    )
    parser.add_argument('image_path', help='Path to the fluorescence microscopy image file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-t', '--threshold-method', default='otsu',
                        help='Segmentation threshold method (otsu, adaptive, or manual)')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.biophysics import analyze_cell_morphology_and_cytoskeleton

    result = analyze_cell_morphology_and_cytoskeleton(
        image_path=args.image_path,
        output_dir=args.output,
        threshold_method=args.threshold_method
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cell_morphology_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
