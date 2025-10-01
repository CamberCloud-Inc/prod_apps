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
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import create_segmentation_visualization

    with open(args.input_file, 'r') as f:
        config = json.load(f)

    original_mri = config['original_mri']
    segmentation = config['segmentation']
    output_dir = config.get('output_dir', './visualization_output')

    result = create_segmentation_visualization(
        original_mri=original_mri,
        segmentation=segmentation,
        output_dir=output_dir
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
