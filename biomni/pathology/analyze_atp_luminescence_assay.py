#!/usr/bin/env python3
"""
Analyze ATP Luminescence Assay

Analyze luminescence-based ATP concentration.
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
        description='Analyze luminescence-based ATP concentration'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.pathology import analyze_atp_luminescence_assay

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    data_file = inputs['data_file']
    standard_curve_file = inputs['standard_curve_file']
    normalization_method = inputs.get('normalization_method', 'cell_count')
    normalization_data = inputs.get('normalization_data', None)

    result = analyze_atp_luminescence_assay(
        data_file=data_file,
        standard_curve_file=standard_curve_file,
        normalization_method=normalization_method,
        normalization_data=normalization_data
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
