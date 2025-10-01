#!/usr/bin/env python3
"""
Quantify Corneal Nerve Fibers

Quantify immunofluorescence-labeled corneal nerve fibers.
"""

import sys
import json
from biomni.tool.pathology import quantify_corneal_nerve_fibers



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
    if len(sys.argv) != 2:
        print("Usage: quantify_corneal_nerve_fibers.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
