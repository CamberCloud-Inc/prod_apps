#!/usr/bin/env python3
"""
Camber wrapper for analyze_ebv_antibody_titers from biomni.tool.immunology
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
        description='Analyze EBV antibody titers from ELISA data'
    )
    parser.add_argument('input_file', help='JSON file with sample data')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    sample_data = input_data['sample_data']

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_ebv_antibody_titers

    result = analyze_ebv_antibody_titers(
        sample_data=sample_data,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'ebv_antibody_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
