#!/usr/bin/env python3
"""
Biomni Tool: Analyze Ebv Antibody Titers
Wraps: biomni.tool.immunology.analyze_ebv_antibody_titers
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
        description='Analyze Ebv Antibody Titers'
    )
    parser.add_argument('--sample_data', help='Dictionary containing sample information with OD readings (JSON dict)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import analyze_ebv_antibody_titers

    # Parse sample_data
    sample_data = json.loads(args.sample_data) if args.sample_data else None

    result = analyze_ebv_antibody_titers(
        sample_data=sample_data,
        output_dir=args.output
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'ebv_antibody_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
