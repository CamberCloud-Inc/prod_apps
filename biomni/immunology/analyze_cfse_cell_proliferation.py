#!/usr/bin/env python3
"""
Camber wrapper for analyze_cfse_cell_proliferation from biomni.tool.immunology
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
        description='Analyze CFSE cell proliferation from flow cytometry data'
    )
    parser.add_argument('input_file', help='JSON file with analysis parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    fcs_file_path = input_data['fcs_file_path']
    cfse_channel = input_data.get('cfse_channel', 'FL1-A')
    lymphocyte_gate = input_data.get('lymphocyte_gate', None)

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_cfse_cell_proliferation

    result = analyze_cfse_cell_proliferation(
        fcs_file_path=fcs_file_path,
        cfse_channel=cfse_channel,
        lymphocyte_gate=lymphocyte_gate
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cfse_proliferation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
