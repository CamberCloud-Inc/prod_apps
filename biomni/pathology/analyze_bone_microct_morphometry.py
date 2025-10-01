#!/usr/bin/env python3
"""
Analyze Bone Micro-CT Morphometry

Analyze bone microarchitecture parameters from 3D micro-CT images.
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
        description='Analyze bone microarchitecture parameters from 3D micro-CT images'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.pathology import analyze_bone_microct_morphometry

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    input_file_path = inputs['input_file_path']
    output_dir = inputs.get('output_dir', './results')
    threshold_value = inputs.get('threshold_value', None)

    result = analyze_bone_microct_morphometry(
        input_file_path=input_file_path,
        output_dir=output_dir,
        threshold_value=threshold_value
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
