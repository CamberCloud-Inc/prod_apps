#!/usr/bin/env python3
"""
Analyzes arsenic speciation in liquid samples using HPLC-ICP-MS technique.
"""

import sys
import json
import argparse
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
        description='Analyzes arsenic speciation in liquid samples using HPLC-ICP-MS technique.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import analyze_arsenic_speciation_hplc_icpms

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    sample_data = input_data.get('sample_data')
    sample_name = input_data.get('sample_name', 'Unknown Sample')
    calibration_data = input_data.get('calibration_data')

    # Call the function
    result = analyze_arsenic_speciation_hplc_icpms(
        sample_data=sample_data,
        sample_name=sample_name,
        calibration_data=calibration_data
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'arsenic_speciation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
