#!/usr/bin/env python3
"""
Calculate Brain ADC Map

Calculate Apparent Diffusion Coefficient (ADC) map from diffusion-weighted MRI data.
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
        description='Calculate Brain ADC Map'
    )
    parser.add_argument('--dwi-file-path', required=True, help='Path to diffusion-weighted imaging (DWI) NIfTI file')
    parser.add_argument('--b-values-file', required=True, help='File containing b-values (JSON array or CSV)')
    parser.add_argument('--output-path', default='adc_map.nii.gz', help='Output filename for ADC map (default: adc_map.nii.gz)')
    parser.add_argument('--mask-file-path', help='Optional brain mask file path')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import calculate_brain_adc_map

    # Load b_values from file
    with open(args.b_values_file, 'r') as f:
        if args.b_values_file.endswith('.json'):
            b_values = json.load(f)
        else:  # Assume CSV
            b_values = [float(line.strip()) for line in f if line.strip()]

    result = calculate_brain_adc_map(
        dwi_file_path=args.dwi_file_path,
        b_values=b_values,
        output_path=args.output_path,
        mask_file_path=args.mask_file_path
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'brain_adc_map_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
