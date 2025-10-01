#!/usr/bin/env python3
"""
Analyze Protease Kinetics

Analyze protease kinetics data from fluorogenic peptide cleavage assays.
"""

import sys
import json



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
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.biochemistry import analyze_protease_kinetics
    if len(sys.argv) != 2:
        print("Usage: analyze_protease_kinetics.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
