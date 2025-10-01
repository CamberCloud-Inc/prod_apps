#!/usr/bin/env python3
"""
Segment and analyze microbial cells in microscopy images using image processing techniques.
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
        description='Segment and analyze microbial cells in microscopy images using image processing techniques.'
    )
    parser.add_argument('--image-path', type=str, required=True, help='Path to microscopy image file')
    parser.add_argument('--output-dir', type=str, default='./output', help='Directory where results will be saved')
    parser.add_argument('--min-cell-size', type=int, default=50, help='Minimum cell size in pixels')
    parser.add_argument('--max-cell-size', type=int, default=5000, help='Maximum cell size in pixels')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import segment_and_analyze_microbial_cells

    # Call the function
    result = segment_and_analyze_microbial_cells(
        image_path=args.image_path,
        output_dir=args.output_dir,
        min_cell_size=args.min_cell_size,
        max_cell_size=args.max_cell_size
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cell_segmentation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
