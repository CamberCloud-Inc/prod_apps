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
    deps = ['biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyzes arsenic speciation in liquid samples using HPLC-ICP-MS technique.'
    )
    parser.add_argument('--sample-data', type=str, required=True, help='List of HPLC-ICP-MS measurement data points (JSON string)')
    parser.add_argument('--sample-name', type=str, default='Unknown Sample', help='Identifier for the sample being analyzed')
    parser.add_argument('--calibration-data', type=str, required=True, help='Calibration curve data for quantification (JSON string)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import analyze_arsenic_speciation_hplc_icpms

    # Parse JSON string parameters
    sample_data = json.loads(args.sample_data)
    calibration_data = json.loads(args.calibration_data)

    # Call the function
    result = analyze_arsenic_speciation_hplc_icpms(
        sample_data=sample_data,
        sample_name=args.sample_name,
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
