#!/usr/bin/env python3
"""Biomni Tool: Get Captured Plots
Wraps: biomni.tool.support_tools.get_captured_plots
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Get all captured plots from the biomni session'
    )
    parser.add_argument('input_file', help='JSON file with input data (can be empty dict)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Read input file (expected to be empty dict or minimal config)
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Import after dependencies are installed
    from biomni.tool.support_tools import get_captured_plots

    result = get_captured_plots()

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'captured_plots.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
