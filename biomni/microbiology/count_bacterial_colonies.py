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
    parser.add_argument('--image-path', type=str, required=True, help='Path to the agar plate image file')
    parser.add_argument('--dilution-factor', type=int, default=1, help='Dilution factor used for the sample')
    parser.add_argument('--plate-area-cm2', type=float, default=65.0, help='Area of the agar plate in square centimeters')
    parser.add_argument('--output-dir', type=str, default='./output', help='Directory where results will be saved')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import count_bacterial_colonies

    # Call the function
    result = count_bacterial_colonies(
        image_path=args.image_path,
        dilution_factor=args.dilution_factor,
        plate_area_cm2=args.plate_area_cm2,
        output_dir=args.output_dir
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'colony_count_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
