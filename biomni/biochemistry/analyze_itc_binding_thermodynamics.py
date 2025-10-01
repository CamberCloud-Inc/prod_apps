#!/usr/bin/env python3
"""
Analyze ITC Binding Thermodynamics

Analyzes isothermal titration calorimetry (ITC) data to determine binding affinity and thermodynamic parameters.
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'scipy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze isothermal titration calorimetry (ITC) data'
    )
    parser.add_argument('input_file', help='JSON file with ITC data')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_itc_binding_thermodynamics

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    itc_data_path = inputs.get('itc_data_path')
    itc_data = inputs.get('itc_data')
    temperature = inputs.get('temperature', 298.15)
    protein_concentration = inputs.get('protein_concentration')
    ligand_concentration = inputs.get('ligand_concentration')

    result = analyze_itc_binding_thermodynamics(
        itc_data_path=itc_data_path,
        itc_data=itc_data,
        temperature=temperature,
        protein_concentration=protein_concentration,
        ligand_concentration=ligand_concentration
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'itc_analysis_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
