#!/usr/bin/env python3
"""
Wrapper for biomni.tool.pharmacology.analyze_fda_safety_signals
Analyzes FDA safety signals for drugs.
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
        description='Analyzes FDA safety signals for drugs'
    )
    parser.add_argument('--drug-list', required=True, help='List of drug names to analyze (JSON array format, e.g., ["Aspirin", "Ibuprofen"])')
    parser.add_argument('--comparison-period', help='Analysis period as two dates (JSON array format, e.g., ["2020-01-01", "2023-12-31"])')
    parser.add_argument('--signal-threshold', type=float, default=2.0, help='Statistical threshold for signal detection (default: 2.0)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Parse JSON parameters
    drug_list = json.loads(args.drug_list)

    # Parse comparison_period if provided
    comparison_period = None
    if args.comparison_period:
        comparison_period = tuple(json.loads(args.comparison_period))

    signal_threshold = args.signal_threshold

    # Import after dependencies are installed
    from biomni.tool.pharmacology import analyze_fda_safety_signals

    result = analyze_fda_safety_signals(
        drug_list=drug_list,
        comparison_period=comparison_period,
        signal_threshold=signal_threshold
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'safety_signals_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == "__main__":
    main()
