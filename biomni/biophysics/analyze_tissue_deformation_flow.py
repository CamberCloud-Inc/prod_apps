#!/usr/bin/env python3
"""
Analyze Tissue Deformation Flow

Quantify tissue deformation and flow dynamics from microscopy image sequence.
"""

import sys
import json
import numpy as np



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
    from biomni.tool.biophysics import analyze_tissue_deformation_flow
    if len(sys.argv) != 2:
        print("Usage: analyze_tissue_deformation_flow.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    image_sequence = inputs['image_sequence']
    output_dir = inputs.get('output_dir', 'results')
    pixel_scale = inputs.get('pixel_scale', 1.0)

    # Convert image_sequence to list if it's a path or list of paths
    if isinstance(image_sequence, str):
        # Single path - treat as directory or file pattern
        import glob
        image_sequence = sorted(glob.glob(image_sequence))

    result = analyze_tissue_deformation_flow(
        image_sequence=image_sequence,
        output_dir=output_dir,
        pixel_scale=pixel_scale
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
