#!/usr/bin/env python3
"""
Count bacterial colonies from an image of agar plate using computer vision techniques.
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
        description='Count bacterial colonies from an image of agar plate using computer vision techniques.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import count_bacterial_colonies

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    image_path = input_data.get('image_path')
    dilution_factor = input_data.get('dilution_factor', 1)
    plate_area_cm2 = input_data.get('plate_area_cm2', 65.0)
    output_dir = input_data.get('output_dir', './output')

    # Call the function
    result = count_bacterial_colonies(
        image_path=image_path,
        dilution_factor=dilution_factor,
        plate_area_cm2=plate_area_cm2,
        output_dir=output_dir
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'colony_count_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
