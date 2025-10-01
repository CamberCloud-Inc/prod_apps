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
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for captured plots file (default: ./)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.support_tools import get_captured_plots

    result = get_captured_plots()

    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, 'captured_plots.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
