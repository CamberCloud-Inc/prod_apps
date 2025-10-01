#!/usr/bin/env python3
"""
Create visualization of segmentation results.
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Create visualization of segmentation results'
    )
    parser.add_argument('--original_mri', required=True, help='Path to the original MRI image file')
    parser.add_argument('--segmentation', required=True, help='Path to the segmentation mask file')
    parser.add_argument('--output_dir', default='./visualization_output', help='Directory for visualization output')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import create_segmentation_visualization

    result = create_segmentation_visualization(
        original_mri=args.original_mri,
        segmentation=args.segmentation,
        output_dir=args.output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'visualization_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "visualization_files": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
