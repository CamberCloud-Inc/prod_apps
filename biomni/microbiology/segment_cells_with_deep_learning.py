#!/usr/bin/env python3
"""
Segment cells in microscopy images using deep learning models.
"""

import sys
import json
import argparse
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
        description='Segment cells in microscopy images using deep learning models.'
    )
    parser.add_argument('--image-path', type=str, required=True, help='Path to microscopy image file')
    parser.add_argument('--model-type', type=str, default='cellpose', help='Deep learning model to use (cellpose, stardist, etc.)')
    parser.add_argument('--output-dir', type=str, default='./output', help='Directory where results will be saved')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import segment_cells_with_deep_learning

    # Call the function
    result = segment_cells_with_deep_learning(
        image_path=args.image_path,
        model_type=args.model_type,
        output_dir=args.output_dir
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'deep_learning_segmentation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
