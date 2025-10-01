#!/usr/bin/env python3
"""
Reconstruct 3D Face from MRI

Generate a 3D model of facial anatomy from MRI scans of the head and neck.
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Reconstruct 3D Face from MRI'
    )
    parser.add_argument('input_file', help='Input JSON file with mri_file_path and optional parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import reconstruct_3d_face_from_mri

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    mri_file_path = inputs['mri_file_path']
    output_dir = inputs.get('output_dir', './output')
    subject_id = inputs.get('subject_id', 'subject')
    threshold_value = inputs.get('threshold_value', 300)

    result = reconstruct_3d_face_from_mri(
        mri_file_path=mri_file_path,
        output_dir=output_dir,
        subject_id=subject_id,
        threshold_value=threshold_value
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, '3d_face_reconstruction_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
