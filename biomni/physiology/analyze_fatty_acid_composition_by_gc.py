#!/usr/bin/env python3
"""
Analyze Fatty Acid Composition by GC

Analyzes fatty acid composition in tissue samples using gas chromatography data.
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Fatty Acid Composition by GC'
    )
    parser.add_argument('--gc-data-file', required=True, help='Path to gas chromatography data file (CSV or TXT format)')
    parser.add_argument('--tissue-type', required=True, help='Type of tissue sample (e.g., brain, liver, adipose)')
    parser.add_argument('--sample-id', required=True, help='Unique identifier for the sample')
    parser.add_argument('--output-directory', default='./results', help='Directory for output files (default: ./results)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_fatty_acid_composition_by_gc

    result = analyze_fatty_acid_composition_by_gc(
        gc_data_file=args.gc_data_file,
        tissue_type=args.tissue_type,
        sample_id=args.sample_id,
        output_directory=args.output_directory
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fatty_acid_composition_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
