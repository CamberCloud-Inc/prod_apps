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
    parser.add_argument('input_file', help='Input JSON file with gc_data_file, tissue_type, sample_id')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_fatty_acid_composition_by_gc

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    gc_data_file = inputs['gc_data_file']
    tissue_type = inputs['tissue_type']
    sample_id = inputs['sample_id']
    output_directory = inputs.get('output_directory', './results')

    result = analyze_fatty_acid_composition_by_gc(
        gc_data_file=gc_data_file,
        tissue_type=tissue_type,
        sample_id=sample_id,
        output_directory=output_directory
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'fatty_acid_composition_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
