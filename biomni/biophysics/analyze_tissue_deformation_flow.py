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
    deps = ['biomni', 'opencv-python', 'scipy']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Quantify tissue deformation and flow dynamics from microscopy image sequence'
    )
    parser.add_argument('image_sequence', help='Path to time-lapse microscopy images (glob pattern or directory)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-p', '--pixel-scale', type=float, default=1.0,
                        help='Physical size per pixel in micrometers (default: 1.0)')

    args = parser.parse_args()
    install_dependencies()

    # Convert image_sequence to list if it's a path or glob pattern
    import glob
    image_sequence = sorted(glob.glob(args.image_sequence))

    if not image_sequence:
        print(f"Error: No images found matching pattern: {args.image_sequence}")
        sys.exit(1)

    from biomni.tool.biophysics import analyze_tissue_deformation_flow

    result = analyze_tissue_deformation_flow(
        image_sequence=image_sequence,
        output_dir=args.output,
        pixel_scale=args.pixel_scale
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'tissue_deformation_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
