#!/usr/bin/env python3
"""
Analyze RNA Secondary Structure Features

Calculate numeric values for various structural features of an RNA secondary structure.
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
        description='Calculate structural features of RNA secondary structure'
    )
    parser.add_argument('input_file', help='JSON file with RNA structure data')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_rna_secondary_structure_features

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    dot_bracket_structure = inputs['dot_bracket_structure']
    sequence = inputs.get('sequence')

    result = analyze_rna_secondary_structure_features(
        dot_bracket_structure=dot_bracket_structure,
        sequence=sequence
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'rna_structure_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
