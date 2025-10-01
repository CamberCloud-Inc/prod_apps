#!/usr/bin/env python3
"""
Analyze Aortic Diameter and Geometry

Analyze aortic diameter and geometry from cardiovascular imaging.
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
        description='Analyze aortic diameter and geometry from cardiovascular imaging'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.pathology import analyze_aortic_diameter_and_geometry

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    image_path = inputs['image_path']
    output_dir = inputs.get('output_dir', './output')

    result = analyze_aortic_diameter_and_geometry(
        image_path=image_path,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
