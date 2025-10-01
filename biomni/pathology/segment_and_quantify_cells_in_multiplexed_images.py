#!/usr/bin/env python3
"""
Segment and Quantify Cells in Multiplexed Images

Segment cells and quantify protein expression levels from multichannel tissue images.
"""

import sys
import json



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
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.pathology import segment_and_quantify_cells_in_multiplexed_images
    if len(sys.argv) != 2:
        print("Usage: segment_and_quantify_cells_in_multiplexed_images.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
