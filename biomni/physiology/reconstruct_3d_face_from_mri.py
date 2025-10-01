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
    deps = ['biomni', 'opencv-python', 'scikit-image', 'scipy', 'nibabel']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Reconstruct 3D Face from MRI'
    )
    parser.add_argument('--mri-file-path', required=True, help='Path to MRI NIfTI file of head and neck')
    parser.add_argument('--output-dir', default='./output', help='Directory for output files (default: ./output)')
    parser.add_argument('--subject-id', default='subject', help='Subject identifier (default: subject)')
    parser.add_argument('--threshold-value', type=int, default=300, help='Threshold value for segmentation (default: 300)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import reconstruct_3d_face_from_mri

    result = reconstruct_3d_face_from_mri(
        mri_file_path=args.mri_file_path,
        output_dir=args.output_dir,
        subject_id=args.subject_id,
        threshold_value=args.threshold_value
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, '3d_face_reconstruction_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
