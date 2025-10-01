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
    parser.add_argument('input_file', help='Input JSON file with dwi_file_path, b_values and optional parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import calculate_brain_adc_map

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    dwi_file_path = inputs['dwi_file_path']
    b_values = inputs['b_values']
    output_path = inputs.get('output_path', 'adc_map.nii.gz')
    mask_file_path = inputs.get('mask_file_path')

    result = calculate_brain_adc_map(
        dwi_file_path=dwi_file_path,
        b_values=b_values,
        output_path=output_path,
        mask_file_path=mask_file_path
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'brain_adc_map_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
