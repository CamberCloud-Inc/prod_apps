#!/usr/bin/env python3
"""
Segment and Quantify Cells in Multiplexed Images

Segment cells and quantify protein expression levels from multichannel tissue images.
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
        description='Segment cells and quantify protein expression levels from multichannel tissue images'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.pathology import segment_and_quantify_cells_in_multiplexed_images

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    image_path = inputs['image_path']
    markers_list = inputs['markers_list']
    nuclear_channel_index = inputs.get('nuclear_channel_index', 0)
    output_dir = inputs.get('output_dir', './output')

    result = segment_and_quantify_cells_in_multiplexed_images(
        image_path=image_path,
        markers_list=markers_list,
        nuclear_channel_index=nuclear_channel_index,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
