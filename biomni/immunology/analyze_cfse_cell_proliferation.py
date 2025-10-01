#!/usr/bin/env python3
"""
Biomni Tool: Analyze Cfse Cell Proliferation
Wraps: biomni.tool.immunology.analyze_cfse_cell_proliferation
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Cfse Cell Proliferation'
    )
    parser.add_argument('--fcs_file_path', help='Path to FCS file containing CFSE data')
    parser.add_argument('--cfse_channel', help='Fluorescence channel for CFSE (default: FL1-A)')
    parser.add_argument('--lymphocyte_gate', help='Lymphocyte gating parameters (JSON dict, optional)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import analyze_cfse_cell_proliferation

    # Parse lymphocyte_gate if provided
    lymphocyte_gate = json.loads(args.lymphocyte_gate) if args.lymphocyte_gate else None
    cfse_channel = args.cfse_channel if args.cfse_channel else 'FL1-A'

    result = analyze_cfse_cell_proliferation(
        fcs_file_path=args.fcs_file_path,
        cfse_channel=cfse_channel,
        lymphocyte_gate=lymphocyte_gate
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'cfse_proliferation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
