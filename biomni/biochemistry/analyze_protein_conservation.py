#!/usr/bin/env python3
"""
Analyze Protein Conservation

Perform multiple sequence alignment and phylogenetic analysis to identify conserved protein regions.
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
        description='Perform multiple sequence alignment and phylogenetic analysis'
    )
    parser.add_argument('input_file', help='JSON file with protein sequences')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_protein_conservation

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    protein_sequences = inputs['protein_sequences']
    output_dir = inputs.get('output_dir', './')

    result = analyze_protein_conservation(
        protein_sequences=protein_sequences,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'protein_conservation_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
