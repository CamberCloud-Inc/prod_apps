#!/usr/bin/env python3
"""
Analyze Protease Kinetics

Analyze protease kinetics data from fluorogenic peptide cleavage assays.
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
        description='Analyze protease kinetics data from fluorogenic peptide cleavage assays'
    )
    parser.add_argument('input_file', help='JSON file with protease kinetics data')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_protease_kinetics

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    time_points = inputs['time_points']
    fluorescence_data = inputs['fluorescence_data']
    substrate_concentrations = inputs['substrate_concentrations']
    enzyme_concentration = inputs['enzyme_concentration']
    output_prefix = inputs.get('output_prefix', 'protease_kinetics')
    output_dir = inputs.get('output_dir', './')

    result = analyze_protease_kinetics(
        time_points=time_points,
        fluorescence_data=fluorescence_data,
        substrate_concentrations=substrate_concentrations,
        enzyme_concentration=enzyme_concentration,
        output_prefix=output_prefix,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'protease_kinetics_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
