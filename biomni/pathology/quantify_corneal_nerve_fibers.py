#!/usr/bin/env python3
"""
Quantify Corneal Nerve Fibers

Quantify immunofluorescence-labeled corneal nerve fibers.
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
        description='Quantify immunofluorescence-labeled corneal nerve fibers'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.pathology import quantify_corneal_nerve_fibers

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    image_path = inputs['image_path']
    marker_type = inputs['marker_type']
    output_dir = inputs.get('output_dir', './output')
    threshold_method = inputs.get('threshold_method', 'otsu')

    result = quantify_corneal_nerve_fibers(
        image_path=image_path,
        marker_type=marker_type,
        output_dir=output_dir,
        threshold_method=threshold_method
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
