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
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import segment_and_analyze_microbial_cells

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    image_path = input_data.get('image_path')
    output_dir = input_data.get('output_dir', './output')
    min_cell_size = input_data.get('min_cell_size', 50)
    max_cell_size = input_data.get('max_cell_size', 5000)

    # Call the function
    result = segment_and_analyze_microbial_cells(
        image_path=image_path,
        output_dir=output_dir,
        min_cell_size=min_cell_size,
        max_cell_size=max_cell_size
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cell_segmentation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
