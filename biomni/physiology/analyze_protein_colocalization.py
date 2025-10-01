#!/usr/bin/env python3
"""
Analyze Protein Colocalization

Analyze colocalization between two fluorescently labeled proteins in microscopy images.
"""

import sys
import json
from biomni.tool.physiology import analyze_protein_colocalization



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
        print("Usage: analyze_protein_colocalization.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    channel1_path = inputs['channel1_path']
    channel2_path = inputs['channel2_path']
    output_dir = inputs.get('output_dir', './output')
    threshold_method = inputs.get('threshold_method', 'otsu')

    result = analyze_protein_colocalization(
        channel1_path=channel1_path,
        channel2_path=channel2_path,
        output_dir=output_dir,
        threshold_method=threshold_method
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
