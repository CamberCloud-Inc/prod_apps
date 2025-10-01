#!/usr/bin/env python3
"""
Biomni Tool: Analyze Cns Lesion Histology
Wraps: biomni.tool.immunology.analyze_cns_lesion_histology
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
        description='Analyze Cns Lesion Histology'
    )
    parser.add_argument('--image_path', help='Path to histology image file')
    parser.add_argument('--cell_markers', help='Cell markers with color thresholds (JSON dict, optional)')
    parser.add_argument('--pixel_size_um', help='Physical size of each pixel in micrometers (default: 0.5)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import analyze_cns_lesion_histology

    # Parse cell_markers if provided
    cell_markers = json.loads(args.cell_markers) if args.cell_markers else None
    pixel_size_um = float(args.pixel_size_um) if args.pixel_size_um else 0.5

    result = analyze_cns_lesion_histology(
        image_path=args.image_path,
        output_dir=args.output,
        cell_markers=cell_markers,
        pixel_size_um=pixel_size_um
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'histology_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
